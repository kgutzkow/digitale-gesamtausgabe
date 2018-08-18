import click
import json
import re

from copy import deepcopy
from io import BytesIO
from lxml import etree


def display_element(element, styles):
    """Test whether the given element should be displayed."""
    if '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name' in element.attrib:
        style_name = element.attrib['{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name']
        if style_name in styles:
            if 'display' in styles[style_name]['text']:
                if styles[style_name]['text']['display'] == 'none':
                    return False
            return True
    return False


def attach_text(target, text, to_tail):
    """Attach `text` to the `target`. Checks whether there is already text there and if so, appends to that
    Can attach `to_tail` or to the main text."""
    if text:
        if to_tail:
            if target.tail:
                target.tail = '%s%s' % (target.tail, text)
            else:
                target.tail = text
        else:
            if target.text:
                target.text = '%s%s' % (target.text, text)
            else:
                target.text = text


def trim_hidden(element):
    """Trim elements from the DOM that are not visible."""
    idx = 0
    for child in element:
        if child.attrib['display'] == 'no':
            if child.tail:
                if idx > 0:
                    attach_text(element[idx - 1], child.tail, to_tail=True)
                else:
                    attach_text(element, child.tail, to_tail=False)
            element.remove(child)
        else:
            trim_hidden(child)
            idx = idx + 1
    if 'display' in element.attrib:
        del element.attrib['display']


def trim_empty(element):
    """Trim elements from the DOM that have no content."""
    for child in element:
        trim_empty(child)
    idx = 0
    for child in element:
        if len(child) == 0:
            if not child.text:
                if idx > 0:
                    attach_text(element[idx - 1], child.tail, to_tail=True)
                else:
                    attach_text(element, child.tail, to_tail=False)
                element.remove(child)
            elif not child.text.strip():
                if idx > 0:
                    attach_text(element[idx - 1], child.text, to_tail=True)
                    attach_text(element[idx - 1], child.tail, to_tail=True)
                else:
                    attach_text(element, child.text, to_tail=False)
                    attach_text(element, child.tail, to_tail=False)
                element.remove(child)
            else:
                idx = idx + 1
        else:
            idx = idx + 1

UNKNOWN_STYLES = []


def merge_styles(element, styles, extract_style_names, style_mappings):
    """Merge the style definitions into the element's style"""
    for child in element:
        merge_styles(child, styles, extract_style_names, style_mappings)
    if 'style' in element.attrib:
        style = styles[element.attrib['style']]
        del element.attrib['style']
        style_list = []
        for key, value in style['paragraph'].items():
            if key in extract_style_names:
                style_list.append((key, value))
        for key, value in style['text'].items():
            if key in extract_style_names:
                style_list.append((key, value))
        if style_list:
            style_list.sort(key=lambda i: i[0])
            style_desc = str(style_list)
            if style_desc not in style_mappings:
                style_mappings[style_desc] = 'style-%i' % len(style_mappings)
                UNKNOWN_STYLES.append((style_desc, style_mappings[style_desc]))
            if style_mappings[style_desc]:
                element.attrib['style'] = style_mappings[style_desc]


def strip_whitespace(element):
    """Strip unneeded whitespace."""
    if element.text is not None:
        element.text = element.text.strip()
    if element.tag == '{http://www.tei-c.org/ns/1.0}p' and element.tail is not None:
        element.tail = element.tail.strip()
    for child in element:
        strip_whitespace(child)


def simplify_tree(element, merge_single=True, merge_attributes=None):
    """Simplify the tree, merging together elements that have no distinction."""
    for child in element:
        simplify_tree(child, merge_single=merge_single, merge_attributes=merge_attributes)
    if len(element) == 1:
        if merge_single and not element.text:
            element.text = element[0].text
            if merge_attributes:
                for attrib_name in merge_attributes:
                    if attrib_name in element[0].attrib:
                        if attrib_name in element.attrib:
                            element.attrib[attrib_name] = '%s %s' % (element.attrib[attrib_name], element[0].attrib[attrib_name])
                        else:
                            element.attrib[attrib_name] = element[0].attrib[attrib_name]
            element.remove(element[0])
    else:
        idx = 0
        for child in element:
            if child.tag == '{http://www.tei-c.org/ns/1.0}span' and 'style' not in child.attrib:
                if idx > 0:
                    attach_text(element[idx - 1], child.text, to_tail=True)
                    attach_text(element[idx - 1], child.tail, to_tail=True)
                else:
                    attach_text(element, child.text, to_tail=False)
                    attach_text(element, child.tail, to_tail=False)
                element.remove(child)
            else:
                idx = idx + 1


def modify_elements(element, rules):
    """Relable heading elements."""
    for rule in rules:
        matches = None
        if 'tag' in rule['match'] and element.tag == rule['match']['tag']:
            matches = True
        if matches != False and 'attrs' in rule['match']:
            for match_attr in rule['match']['attrs']:
                if match_attr['name'] in element.attrib:
                    if match_attr['value'] == element.attrib[match_attr['name']]:
                        matches = True
                    else:
                        matches = False
                        break
                else:
                    matches = False
                    break
        if matches:
            if 'tag' in rule['action']:
                element.tag = rule['action']['tag']
            if 'attrs' in rule['action']:
                for key, value in rule['action']['attrs'].items():
                    if value is None and key in element.attrib:
                        del element.attrib[key]
                    elif value == 'text()':
                        element.attrib[key] = element.text
                    else:
                        element.attrib[key] = value
            if 'text' in rule['action']:
                element.text = rule['action']['text']
            if 'wrap' in rule['action']:
                wrapper = etree.Element(rule['action']['wrap']['tag'])
                if 'attrs' in rule['action']['wrap']:
                    for key, value in rule['action']['wrap']['attrs'].items():
                        wrapper.attrib[key] = value
                wrapper.tail = element.tail
                element.tail = None
                element.getparent().replace(element, wrapper)
                wrapper.append(element)
    for child in element:
        modify_elements(child, rules)


def apply_post_processing(root, styles, steps):
    """Apply the post-processing steps from the configuration."""
    for step in steps:
        if step['action'] == 'trim-hidden':
            trim_hidden(root)
        elif step['action'] == 'strip-whitespace':
            strip_whitespace(root)
        elif step['action'] == 'trim-empty':
            trim_empty(root)
        elif step['action'] == 'merge-styles':
            merge_styles(root, styles, **step['params'])
            if UNKNOWN_STYLES:
                print('==============')
                print('Unknown styles')
                for style_desc in UNKNOWN_STYLES:
                    print(style_desc)
                print('==============')
        elif step['action'] == 'simplify-tree':
            simplify_tree(root, **(step['params'] if 'params' in step else {}))
        elif step['action'] == 'modify-elements':
            modify_elements(root, **step['params'])


def apply_text_processing(text, steps):
    for step in steps:
        if step['action'] == 'regex-replace':
            text = re.sub(step['params']['regex'], step['params']['replace'], text)
    return text


@click.command()
@click.argument('input', type=click.File(mode='rb'))
@click.argument('config', type=click.File(mode='rb'))
@click.argument('output', type=click.File(mode='wb'))
def extract_text(input, config, output):
    """Extract the text from `input` using the configuration in `config` and write the resulting TEI body to `output`."""
    config = json.load(config)
    styles = {}
    style = {}
    in_body = False
    element_stack = []
    for event, element in etree.iterparse(input, events=('start', 'end')):
        if event == 'start':
            # Extract style definitions
            if element.tag == '{urn:oasis:names:tc:opendocument:xmlns:style:1.0}style':
                if '{urn:oasis:names:tc:opendocument:xmlns:style:1.0}parent-style-name' in element.attrib and element.attrib['{urn:oasis:names:tc:opendocument:xmlns:style:1.0}parent-style-name'] in styles:
                    style = deepcopy(styles[element.attrib['{urn:oasis:names:tc:opendocument:xmlns:style:1.0}parent-style-name']])
                else:
                    style = {'paragraph': {}, 'text': {}}
            elif element.tag == '{urn:oasis:names:tc:opendocument:xmlns:style:1.0}paragraph-properties':
                if style:
                    for key, value in element.attrib.items():
                        style['paragraph'][key[key.find('}') + 1:]] = value
            elif element.tag == '{urn:oasis:names:tc:opendocument:xmlns:style:1.0}text-properties':
                if style:
                    for key, value in element.attrib.items():
                        style['text'][key[key.find('}') + 1:]] = value
            # Text processing
            elif element.tag == '{urn:oasis:names:tc:opendocument:xmlns:office:1.0}body':
                in_body = True
                element_stack.append(etree.Element('{http://www.tei-c.org/ns/1.0}body', nsmap={'tei': 'http://www.tei-c.org/ns/1.0'}))
            elif in_body and element.tag == '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p':
                new_element = etree.Element('{http://www.tei-c.org/ns/1.0}p')
                new_element.attrib['display'] = 'yes' if display_element(element, styles) else 'no'
                if '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name' in element.attrib:
                    new_element.attrib['style'] = element.attrib['{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name']
                element_stack.append(new_element)
                if element.text:
                    element_stack[-1].text = element.text
            elif in_body and element.tag == '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}h':
                new_element = etree.Element('{http://www.tei-c.org/ns/1.0}p')
                new_element.attrib['display'] = 'yes' if display_element(element, styles) else 'no'
                if '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name' in element.attrib:
                    new_element.attrib['style'] = element.attrib['{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name']
                element_stack.append(new_element)
                if element.text:
                    element_stack[-1].text = element.text
            elif in_body and element.tag in ['{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span', '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}s', '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}soft-page-break', '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}tab']:
                new_element = etree.Element('{http://www.tei-c.org/ns/1.0}span')
                new_element.attrib['display'] = 'yes' if display_element(element, styles) else 'no'
                if '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name' in element.attrib:
                    new_element.attrib['style'] = element.attrib['{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name']
                element_stack.append(new_element)
                if element.text:
                    element_stack[-1].text = element.text
            elif in_body:
                print(element.tag)
        elif event == 'end':
            if element.tag == '{urn:oasis:names:tc:opendocument:xmlns:style:1.0}style':
                styles[element.attrib['{urn:oasis:names:tc:opendocument:xmlns:style:1.0}name']] = style
            elif element.tag == '{urn:oasis:names:tc:opendocument:xmlns:office:1.0}body':
                in_body = False
                root = element_stack.pop()
                apply_post_processing(root, styles, config['workflow'])
                buf = BytesIO(etree.tostring(root, xml_declaration=True, encoding="UTF-8"))
                text = buf.getvalue().decode('utf-8')
                text = apply_text_processing(text, config['post-process'])
                output.write(text.encode('utf-8'))
            elif in_body and element.tag == '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p':
                new_element = element_stack.pop()
                element_stack[-1].append(new_element)
            elif in_body and element.tag == '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}h':
                new_element = element_stack.pop()
                element_stack[-1].append(new_element)
            elif in_body and element.tag in ['{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span', '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}s', '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}soft-page-break', '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}tab']:
                new_element = element_stack.pop()
                element_stack[-1].append(new_element)
                if element.tail:
                    new_element.tail = element.tail
            element.clear()

if __name__ == '__main__':
    extract_text()
