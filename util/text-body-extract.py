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


def simplify_tree(element):
    """Simplify the tree, merging together elements that have no distinction."""
    for child in element:
        simplify_tree(child)
    if len(element) == 1:
        if not element.text:
            element.text = element[0].text
            if 'style' in element[0].attrib:
                if 'style' in element.attrib:
                    element.attrib['style'] = '%s %s' % (element.attrib['style'], element[0].attrib['style'])
                else:
                    element.attrib['style'] = element[0].attrib['style']
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


def relabel_styles(element, relabels):
    """Re-label styles based on the rules in the configuration."""
    for child in element:
        relabel_styles(child, relabels)
    if 'style' in element.attrib:
        # Extract from children
        if len(element) > 0 and not element.text:
            shared_styles = None
            shared_tag = element[0].tag
            for child in element:
                if child.tag != shared_tag or child.tail is not None:
                    shared_styles = []
                    break
                if shared_styles is None:
                    if 'style' in child.attrib:
                        shared_styles = set(child.attrib['style'].split(' '))
                    else:
                        shared_styles = []
                        break
                else:
                    if 'style' in child.attrib:
                        shared_styles = shared_styles.intersection(set(child.attrib['style'].split(' ')))
                    else:
                        shared_styles = []
                        break
            if shared_styles:
                if 'style' in element.attrib:
                    element.attrib['style'] = '%s %s' % (element.attrib['style'], ' '.join(shared_styles))
                else:
                    element.attrib['style'] = ' '.join(shared_styles)
                for child in element:
                    child.attrib['style'] = ' '.join([cls for cls in child.attrib['style'].split() if cls not in shared_styles])
                    if not child.attrib['style']:
                        del child.attrib['style']
        # Manually specified relabels
        if element.attrib['style'] in relabels:
            element.attrib['style'] = relabels[element.attrib['style']]
        # Page number relabels
        if 'font-style-italic' in element.attrib['style'] and len(element) == 0:
            if re.search('\[[0-9MCVXI]+\]', element.text):
                element.attrib['style'] = element.attrib['style'].replace('font-style-italic', 'page-number')


def relabel_elements(element):
    """Relable heading elements."""
    if element.tag == '{http://www.tei-c.org/ns/1.0}p' and 'style' in element.attrib and element.attrib['style'] == 'heading':
        element.tag = '{http://www.tei-c.org/ns/1.0}head'
        element.attrib['style'] = 'main'
    elif element.tag == '{http://www.tei-c.org/ns/1.0}p' and 'style' in element.attrib and element.attrib['style'] == 'sub-heading':
        element.tag = '{http://www.tei-c.org/ns/1.0}head'
        element.attrib['style'] = 'sub'
    for child in element:
        relabel_elements(child)


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
                trim_hidden(root)
                strip_whitespace(root)
                trim_empty(root)
                merge_styles(root, styles, config['styles']['extract-styles'], config['styles']['style-name-mappings'])
                simplify_tree(root)
                relabel_styles(root, config['styles']['style-relabels'])
                simplify_tree(root)
                relabel_elements(root)
                if UNKNOWN_STYLES:
                    print('==============')
                    print('Unknown styles')
                    for style_desc in UNKNOWN_STYLES:
                        print(style_desc)
                    print('==============')
                buf = BytesIO(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8"))
                text = buf.getvalue().decode('utf-8')
                # Fix some white-space issues
                text = re.sub('([a-z])<tei:span', '\g<1> <tei:span', text)
                text = re.sub('</tei:span>([a-z])', '</tei:span> \g<1>', text)
                text = re.sub('(-<tei:span style="page-number">\[[0-9XVI]+\]</tei:span>) ([a-z])', '\g<1>\g<2>', text)
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
