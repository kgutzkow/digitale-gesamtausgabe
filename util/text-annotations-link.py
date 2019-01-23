import click
import re

from copy import deepcopy
from lxml import etree


def textContent(node):
    if node.text:
        return node.text
    else:
        return ''.join([textContent(child) for child in node])


def setContent(node, text):
    if len(node) == 0:
        node.text = text
    else:
        setContent(node[0], text)


def link_annotation(annotation, text_body):
    range = annotation.xpath('tei:citedRange[@type="word-range"]', namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
    if range:
        matched = False
        range = range[0]
        range_regexp = range.text.replace('\\', '\\\\').replace('[', '\\[').replace(']', '\\]').replace('.', '\\.') \
            .replace('(', '\\(').replace(')', '\\)').replace('\\[\\.\\.\\.\\]', '.+')
        for block in text_body:
            block_text = textContent(block)
            if re.fullmatch(range_regexp, block_text):
                # Simple case where the range matches exactly the content of one block
                matched = True
                for child in block:
                    if child.tag == '{http://www.tei-c.org/ns/1.0}pb':
                        # Page-breaks are never part of the annotation
                        pass
                    elif child.tag == '{http://www.tei-c.org/ns/1.0}seg':
                        child.tag = '{http://www.tei-c.org/ns/1.0}ref'
                        child.attrib['target'] = '#' + annotation.attrib['{http://www.w3.org/XML/1998/namespace}id']
                    else:
                        ref = etree.Element('{http://www.tei-c.org/ns/1.0}ref')
                        ref.attrib['target'] = '#' + annotation.attrib['{http://www.w3.org/XML/1998/namespace}id']
                        block.replace(child, ref)
                        ref.append(child)
            elif re.search(range_regexp, block_text):
                matched = True
                if len(block) == 1:
                    # Range matches part of the block, but there is only one element in the block
                    match = re.search(range_regexp, block_text)
                    if match.start() == 0:
                        # Range matches at the beginning of the block
                        setContent(block[0], block_text[match.end():])
                        ref = etree.Element('{http://www.tei-c.org/ns/1.0}ref')
                        ref.attrib['target'] = '#' + annotation.attrib['{http://www.w3.org/XML/1998/namespace}id']
                        ref.text = match.group(0)
                        block.insert(0, ref)
                    elif match.end() == len(block_text):
                        # Range matches at the end of the bloc
                        setContent(block[0], block_text[:match.start()])
                        ref = etree.Element('{http://www.tei-c.org/ns/1.0}ref')
                        ref.attrib['target'] = '#' + annotation.attrib['{http://www.w3.org/XML/1998/namespace}id']
                        ref.text = match.group(0)
                        block.append(ref)
                    else:
                        # Range matches in the middle of the block
                        suffix = deepcopy(block[0])
                        setContent(block[0], block_text[:match.start()])
                        ref = etree.Element('{http://www.tei-c.org/ns/1.0}ref')
                        ref.attrib['target'] = '#' + annotation.attrib['{http://www.w3.org/XML/1998/namespace}id']
                        ref.text = match.group(0)
                        block.append(ref)
                        setContent(suffix, block_text[match.end():])
                        block.append(suffix)
                else:
                    # Range matches part of a block with multiple elements
                    in_single = False
                    for idx, child in enumerate(list(block)):
                        if re.search(range_regexp, textContent(child)):
                            # Range matches completely within one element
                            in_single = True
                            child_text = textContent(child)
                            match = re.search(range_regexp, child_text)
                            if match.start() == 0:
                                # Range matches at the beginning of the element
                                setContent(child, child_text[match.end():])
                                ref = etree.Element('{http://www.tei-c.org/ns/1.0}ref')
                                ref.attrib['target'] = '#' + annotation.attrib['{http://www.w3.org/XML/1998/namespace}id']
                                ref.text = match.group(0)
                                block.insert(idx, ref)
                            elif match.end() == len(block_text):
                                # Range matches at the end of the element
                                setContent(child, child_text[:match.start()])
                                ref = etree.Element('{http://www.tei-c.org/ns/1.0}ref')
                                ref.attrib['target'] = '#' + annotation.attrib['{http://www.w3.org/XML/1998/namespace}id']
                                ref.text = match.group(0)
                                block.insert(idx + 1, ref)
                            else:
                                # Range matches in the middle of the element
                                suffix = deepcopy(child)
                                setContent(child, child_text[:match.start()])
                                ref = etree.Element('{http://www.tei-c.org/ns/1.0}ref')
                                ref.attrib['target'] = '#' + annotation.attrib['{http://www.w3.org/XML/1998/namespace}id']
                                ref.text = match.group(0)
                                block.insert(idx + 1, ref)
                                setContent(suffix, child_text[match.end():])
                                block.insert(idx + 2, suffix)
                            break
                    if not in_single:
                        # Range splits across multiple elements
                        match = re.search(range_regexp, block_text)
                        new_children = []
                        offset = 0
                        for child in list(block):
                            child_text = textContent(child)
                            if child_text:
                                if offset + len(child_text) < match.start():
                                    # Element is completely before the start of the range
                                    new_children.append(child)
                                    print('Needs testing [before start]')
                                if offset <= match.start() < offset + len(child_text):
                                    # Element contains the start of the range
                                    if match.start() - offset == 0:
                                        if child.tag == '{http://www.tei-c.org/ns/1.0}seg':
                                            child.tag = '{http://www.tei-c.org/ns/1.0}ref'
                                            child.attrib['target'] = '#' + annotation.attrib['{http://www.w3.org/XML/1998/namespace}id']
                                            new_children.append(child)
                                        else:
                                            ref = etree.Element('{http://www.tei-c.org/ns/1.0}ref')
                                            ref.attrib['target'] = '#' + annotation.attrib['{http://www.w3.org/XML/1998/namespace}id']
                                            ref.append(child)
                                            new_children.append(ref)
                                    else:
                                        setContent(child, child_text[:match.start() - offset])
                                        new_children.append(child)
                                        ref = etree.Element('{http://www.tei-c.org/ns/1.0}ref')
                                        ref.attrib['target'] = '#' + annotation.attrib['{http://www.w3.org/XML/1998/namespace}id']
                                        ref.append(deepcopy(child))
                                        setContent(ref, child_text[match.start() - offset:])
                                        new_children.append(ref)
                                elif offset <= match.end() < offset + len(child_text):
                                    # Element contains the end of the range
                                    if match.end() - offset == len(child_text):
                                        if child.tag == '{http://www.tei-c.org/ns/1.0}seg':
                                            child.tag = '{http://www.tei-c.org/ns/1.0}ref'
                                            child.attrib['target'] = '#' + annotation.attrib['{http://www.w3.org/XML/1998/namespace}id']
                                            new_children.append(child)
                                        else:
                                            ref = etree.Element('{http://www.tei-c.org/ns/1.0}ref')
                                            ref.attrib['target'] = '#' + annotation.attrib['{http://www.w3.org/XML/1998/namespace}id']
                                            ref.append(child)
                                            new_children.append(ref)
                                    else:
                                        ref = etree.Element('{http://www.tei-c.org/ns/1.0}ref')
                                        ref.attrib['target'] = '#' + annotation.attrib['{http://www.w3.org/XML/1998/namespace}id']
                                        ref.append(deepcopy(child))
                                        setContent(ref, child_text[:match.end() - offset])
                                        new_children.append(ref)
                                        setContent(child, child_text[match.end() - offset:])
                                        new_children.append(child)
                                elif match.end() < offset:
                                    # Element is completely after the end of the range
                                    new_children.append(child)
                                    print('Needs testing [after end]')
                                else:
                                    # Element is inside the range
                                    if child.tag == '{http://www.tei-c.org/ns/1.0}seg':
                                        child.tag = '{http://www.tei-c.org/ns/1.0}ref'
                                        child.attrib['target'] = '#' + annotation.attrib['{http://www.w3.org/XML/1998/namespace}id']
                                        new_children.append(child)
                                    else:
                                        ref = etree.Element('{http://www.tei-c.org/ns/1.0}ref')
                                        ref.attrib['target'] = '#' + annotation.attrib['{http://www.w3.org/XML/1998/namespace}id']
                                        ref.append(child)
                                        new_children.append(ref)
                                    print('Needs testing [in middle]')
                            else:
                                new_children.append(child)
                            offset = offset + len(child_text)
                            block.remove(child)
                        for child in new_children:
                            block.append(child)
        if not matched:
            print('Failed to find: ' + range.text)


@click.command()
@click.argument('input', type=click.File(mode='rb'))
@click.argument('output', type=click.File(mode='wb'))
def link_annotations(input, output):
    parser = etree.XMLParser(remove_blank_text=True)
    document = etree.parse(input, parser).getroot()
    text_body = document.xpath('tei:text/tei:body', namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
    if text_body:
        text_body = text_body[0]
    individual_annotations = document.xpath('tei:text/tei:interpGrp[@type="individual"]', namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
    if individual_annotations:
        individual_annotations = individual_annotations[0]
    for annotation in individual_annotations:
        link_annotation(annotation, text_body)
    output.write(etree.tostring(document, xml_declaration=True, pretty_print=True, encoding="UTF-8"))

if __name__ == '__main__':
    link_annotations()
