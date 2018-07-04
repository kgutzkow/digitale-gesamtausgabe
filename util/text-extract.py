import click

from copy import deepcopy
from lxml import etree


def display_element(element, styles):
    if '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name' in element.attrib:
        style_name = element.attrib['{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name']
        if style_name in styles:
            if 'display' in styles[style_name]['text']:
                if styles[style_name]['text']['display'] == 'none':
                    return False
            return True
    return False


def trim_hidden(element):
    for child in element:
        if child.attrib['display'] == 'no':
            if child.tail:
                if element.text:
                    element.text = '%s%s' % (element.text, child.tail)
                else:
                    element.text = child.tail
            element.remove(child)
        else:
            trim_hidden(child)

def trim_empty(element):
    for child in element:
        trim_empty(child)
        if len(child) == 0 and not child.text:
            if child.tail:
                if element.text:
                    element.text = '%s%s' % (element.text, child.tail)
                else:
                    element.text = child.tail
            element.remove(child)


@click.command()
@click.argument('input', type=click.File(mode='rb'))
@click.argument('output', type=click.File(mode='wb'))
def extract_text(input, output):
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
                element_stack.append(etree.Element('text'))
            elif in_body and element.tag == '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p':
                new_element = etree.Element('p')
                new_element.attrib['display'] = 'yes' if display_element(element, styles) else 'no'
                element_stack.append(new_element)
                if element.text:
                    element_stack[-1].text = element.text
            elif in_body and element.tag == '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}h':
                new_element = etree.Element('h')
                new_element.attrib['display'] = 'yes' if display_element(element, styles) else 'no'
                element_stack.append(new_element)
                if element.text:
                    element_stack[-1].text = element.text
            elif in_body and element.tag == '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span':
                element_stack.append(etree.Element('span'))
                element_stack[-1].attrib['display'] = 'yes' if display_element(element, styles) else 'no'
                if element.text:
                    element_stack[-1].text = element.text
            else:
                print(element.tag)
        elif event == 'end':
            if element.tag == '{urn:oasis:names:tc:opendocument:xmlns:style:1.0}style':
                styles[element.attrib['{urn:oasis:names:tc:opendocument:xmlns:style:1.0}name']] = style
            elif element.tag == '{urn:oasis:names:tc:opendocument:xmlns:office:1.0}body':
                in_body = False
                root = element_stack.pop()
                trim_hidden(root)
                trim_empty(root)
                output.write(etree.tostring(root, pretty_print=True))
            elif in_body and element.tag == '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p':
                new_element = element_stack.pop()
                element_stack[-1].append(new_element)
            elif in_body and element.tag == '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}h':
                new_element = element_stack.pop()
                element_stack[-1].append(new_element)
            elif in_body and element.tag == '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}span':
                new_element = element_stack.pop()
                element_stack[-1].append(new_element)
                if element.tail:
                    new_element.tail = element.tail
            element.clear()

if __name__ == '__main__':
    extract_text()
