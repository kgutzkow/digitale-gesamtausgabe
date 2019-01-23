import click
import json
import re

from copy import deepcopy
from io import BytesIO
from lxml import etree


NS = {'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
      }
SAVE_IT = None
SEQUENCES = {}

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


def strip_whitespace(doc):
    """Strip unneeded whitespace."""
    for element in doc:
        if element[0].text and not element[0].text.strip():
            element.remove(element[0])
        if len(element) > 0 and element[-1].text and not element[-1].text.strip():
            element.remove(element[-1])
        if len(element) > 0:
            if element[0].text:
                while element[0].text.startswith(' '):
                    element[0].text = element[0].text[1:]
            if element[-1].text:
                while element[-1].text.endswith(' '):
                    element[-1].text = element[-1].text[:-1]
        else:
            doc.remove(element)


def simplify_tree(element):
    """Simplify the tree, merging together elements that have no distinction."""
    for child in element:
        simplify_tree(child)
    if element.tag in ['{http://www.tei-c.org/ns/1.0}head', '{http://www.tei-c.org/ns/1.0}p'] and len(element) > 1:
        idx = 1
        while idx < len(element):
            style_1 = element[idx].attrib['style'] if 'style' in element[idx].attrib else None
            style_2 = element[idx - 1].attrib['style'] if 'style' in element[idx - 1].attrib else None
            type_1 = element[idx].attrib['type'] if 'type' in element[idx].attrib else None
            type_2 = element[idx - 1].attrib['type'] if 'type' in element[idx - 1].attrib else None
            if element[idx].tag == element[idx - 1].tag and style_1 == style_2 and type_1 == type_2:
                attach_text(element[idx - 1], element[idx].text, to_tail=False)
                element.remove(element[idx])
            else:
                idx = idx + 1


def modify_elements(element, rules):
    """Relable heading elements."""
    for rule in rules:
        matches = None
        if 'tag' in rule['match']:
            matches = element.tag == rule['match']['tag']
        if matches != False and 'attrs' in rule['match']:
            for match_attr in rule['match']['attrs']:
                if match_attr['name'] in element.attrib:
                    if 'value' not in match_attr or match_attr['value'] == element.attrib[match_attr['name']]:
                        matches = True
                    else:
                        matches = False
                        break
                else:
                    matches = False
                    break
        if matches != False and 'text' in rule['match']:
            matches = element.text == rule['match']['text']
        if matches:
            if 'tag' in rule['action']:
                element.tag = rule['action']['tag']
            if 'attrs' in rule['action']:
                for key, value in rule['action']['attrs'].items():
                    if value is None:
                        if key in element.attrib:
                            del element.attrib[key]
                    elif value == 'text()':
                        element.attrib[key] = element.text
                    elif value.startswith("seq('") and value.endswith("')"):
                        seq_name = value[5:-2]
                        if seq_name not in SEQUENCES:
                            SEQUENCES[seq_name] = 1
                        element.attrib[key] = '%s%i' % (seq_name, SEQUENCES[seq_name])
                        SEQUENCES[seq_name] = SEQUENCES[seq_name] + 1
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
            if 'delete' in rule['action']:
                if len(element.getparent()) == 1:
                    element.getparent().getparent().remove(element.getparent())
                else:
                    element.getparent().remove(element)
            break
    for child in element:
        modify_elements(child, rules)


def extract_word_range(element):
    if element.tag == '{http://www.tei-c.org/ns/1.0}interp':
        new_children = []
        for child in list(element):
            if child.tag == '{http://www.tei-c.org/ns/1.0}span' and ']' in child.text.replace('[...]', '{{ellipsis}}'):
                text = child.text.replace('[...]', '{{ellipsis}}')
                text_range = etree.Element('{http://www.tei-c.org/ns/1.0}citedRange')
                text_range.attrib['type'] = 'word-range'
                text_range.text = text[:text.find(']')].replace('{{ellipsis}}', '[...]')
                new_children.append(text_range)
                child.text = text[text.find(']') + 1:]
                new_children.append(child)
            else:
                new_children.append(child)
            element.remove(child)
        for child in new_children:
            element.append(child)
    else:
        for child in element:
            extract_word_range(child)


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
        elif step['action'] == 'extract-word-range':
            extract_word_range(root)


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
    global SAVE_IT
    config = json.load(config)
    doc = etree.parse(input)
    styles = {}
    # Extract style definitions
    for xpath in ['/office:document/office:styles', '/office:document/office:automatic-styles']:
        for element in doc.xpath(xpath, namespaces=NS)[0]:
            if element.tag == '{urn:oasis:names:tc:opendocument:xmlns:style:1.0}style':
                if '{urn:oasis:names:tc:opendocument:xmlns:style:1.0}parent-style-name' in element.attrib and element.attrib['{urn:oasis:names:tc:opendocument:xmlns:style:1.0}parent-style-name'] in styles:
                    style = deepcopy(styles[element.attrib['{urn:oasis:names:tc:opendocument:xmlns:style:1.0}parent-style-name']])
                else:
                    style = {'paragraph': {}, 'text': {}}
                for child in element:
                    if child.tag == '{urn:oasis:names:tc:opendocument:xmlns:style:1.0}paragraph-properties':
                        for key, value in child.attrib.items():
                            style['paragraph'][key[key.find('}') + 1:]] = value
                    elif child.tag == '{urn:oasis:names:tc:opendocument:xmlns:style:1.0}text-properties':
                        for key, value in child.attrib.items():
                            style['text'][key[key.find('}') + 1:]] = value
                styles[element.attrib['{urn:oasis:names:tc:opendocument:xmlns:style:1.0}name']] = style
    # Build text body structure
    body = etree.Element('{http://www.tei-c.org/ns/1.0}body', nsmap={'tei': 'http://www.tei-c.org/ns/1.0'})
    for element in doc.xpath('/office:document/office:body/office:text/*', namespaces=NS):
        if element.tag in ['{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p', '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}h']:
            new_element = etree.Element('{http://www.tei-c.org/ns/1.0}p')
            new_element.attrib['display'] = 'yes' if display_element(element, styles) else 'no'
            if '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name' in element.attrib:
                new_element.attrib['style'] = element.attrib['{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name']
            if element.text:
                text_element = etree.Element('{http://www.tei-c.org/ns/1.0}span')
                text_element.text = element.text
                text_element.attrib['display'] = 'yes'
                new_element.append(text_element)
            for child in element:
                child_element = etree.Element('{http://www.tei-c.org/ns/1.0}span')
                child_element.attrib['display'] = 'yes' if display_element(child, styles) else 'no'
                if '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name' in child.attrib:
                    child_element.attrib['style'] = child.attrib['{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name']
                if child.text:
                    child_element.text = child.text
                new_element.append(child_element)
                if len(child) > 0:
                    for sub_child in child:
                        if sub_child.tag in ['{urn:oasis:names:tc:opendocument:xmlns:text:1.0}s', '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}tab']:
                            if child_element.text and sub_child.tail:
                                child_element.text = '%s%s' % (child_element.text,sub_child.tail)
                            elif sub_child.tail:
                                child_element.text = sub_child.tail
                        else:
                            child_element = etree.Element('{http://www.tei-c.org/ns/1.0}span')
                            child_element.attrib['display'] = 'yes' if display_element(sub_child, styles) else 'no'
                            if '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name' in sub_child.attrib:
                                child_element.attrib['style'] = sub_child.attrib['{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name']
                            if sub_child.text:
                                child_element.text = sub_child.text
                            new_element.append(child_element)
                            if sub_child.tail:
                                text_element = etree.Element('{http://www.tei-c.org/ns/1.0}span')
                                text_element.text = sub_child.tail
                                text_element.attrib['display'] = 'yes' if display_element(child, styles) else 'no'
                                new_element.append(text_element)
                if child.tail:
                    text_element = etree.Element('{http://www.tei-c.org/ns/1.0}span')
                    text_element.text = child.tail
                    text_element.attrib['display'] = 'yes'
                    new_element.append(text_element)
                    if child.text and 'VARbegrabe' in child.text:
                        SAVE_IT = text_element
            body.append(new_element)

    apply_post_processing(body, styles, config['workflow'])
    buf = BytesIO(etree.tostring(body, pretty_print=True, xml_declaration=True, encoding="UTF-8"))
    text = buf.getvalue().decode('utf-8')
    text = apply_text_processing(text, config['post-process'])
    output.write(text.encode('utf-8'))


if __name__ == '__main__':
    extract_text()
