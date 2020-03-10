import click
import re

from lxml import etree


namespaces = {'tei': 'http://www.tei-c.org/ns/1.0'}
footnote_counter = 1
annotation_counter = 1

def create_text_node(text):
    seg = etree.Element('{http://www.tei-c.org/ns/1.0}seg')
    seg.text = text
    return seg


def process_inline(inline, block):
    global footnote_counter, annotation_counter
    new_inline = None
    if inline.tag == '{http://www.tei-c.org/ns/1.0}emph':
        if re.match('\[[XIV]+\s*\]', inline.text):
            new_inline = etree.Element('{http://www.tei-c.org/ns/1.0}pb')
            new_inline.attrib['n'] = inline.text.strip()[1:-1]
            block.append(new_inline)
        else:
            new_inline = etree.Element('{http://www.tei-c.org/ns/1.0}foreign')
            hi = etree.Element('{http://www.tei-c.org/ns/1.0}hi')
            hi.attrib['style'] = 'font-style-italic'
            hi.text = inline.text
            new_inline.append(hi)
            block.append(new_inline)
        return
    elif inline.tag == '{http://www.tei-c.org/ns/1.0}foreign':
        new_inline = etree.Element(inline.tag)
    elif inline.tag == '{http://www.tei-c.org/ns/1.0}pb':
        new_inline = etree.Element('{http://www.tei-c.org/ns/1.0}pb')
        new_inline.attrib['n'] = inline.attrib['n']
        block.append(new_inline)
        return
    elif inline.tag == '{http://www.tei-c.org/ns/1.0}hi':
        new_inline = etree.Element('{http://www.tei-c.org/ns/1.0}hi')
        if 'rend' in inline.attrib:
            new_inline.attrib['style'] = 'letter-sparse'
    elif inline.tag == '{http://www.tei-c.org/ns/1.0}note':
        new_inline = etree.Element('{http://www.tei-c.org/ns/1.0}ref')
        new_inline.attrib['type'] = 'footnote'
        new_inline.attrib['target'] = '#footnote-{0}'.format(footnote_counter)
        new_inline.text = inline.attrib['n']
        block.append(new_inline)
        footnote = etree.Element('{http://www.tei-c.org/ns/1.0}note')
        footnote.attrib['type'] = 'footnote'
        footnote.attrib['{http://www.w3.org/XML/1998/namespace}id'] = 'footnote-{0}'.format(footnote_counter)
        if inline.text:
            footnote.append(create_text_node(inline.text))
        for child in inline:
            process_inline(child, footnote)
            if child.tail:
                footnote.append(create_text_node(child.tail))
        block.append(footnote)
        footnote_counter = footnote_counter + 1
        return
    elif inline.tag == '{http://www.tei-c.org/ns/1.0}choice':
        new_inline = etree.Element('{http://www.tei-c.org/ns/1.0}ref')
        new_inline.attrib['type'] = 'esv'
        new_inline.attrib['target'] = '#annotation-{0}'.format(annotation_counter)
        new_inline.text = inline.xpath('tei:corr/text()', namespaces=namespaces)[0]
        block.append(new_inline)
        annotation = etree.Element('{http://www.tei-c.org/ns/1.0}interp')
        annotation.attrib['type'] = 'esv'
        annotation.attrib['{http://www.w3.org/XML/1998/namespace}id'] = 'annotation-{0}'.format(annotation_counter)
        para = etree.Element('{http://www.tei-c.org/ns/1.0}p')
        lem = etree.Element('{http://www.tei-c.org/ns/1.0}lem')
        lem.text = inline.xpath('tei:corr/text()', namespaces=namespaces)[0]
        para.append(lem)
        para.append(inline.xpath('tei:sic', namespaces=namespaces)[0])
        annotation.append(para)
        block.append(annotation)
        annotation_counter = annotation_counter + 1
        return
    else:
        print(inline.tag)
    if new_inline is not None:
        new_inline.text = inline.text
        block.append(new_inline)


def process_block(block, blocks):
    new_block = etree.Element(block.tag)
    if 'rend' in block.attrib and block.attrib['rend'] == 'text-indent:0cm':
        new_block.attrib['style'] = 'no-indent'
    blocks.append(new_block)
    if block.text:
        new_block.append(create_text_node(block.text))
    for child in block:
        process_inline(child, new_block)
        if child.tail:
            new_block.append(create_text_node(child.tail))


def walk(node, blocks):
    for child in node:
        if child.tag == '{http://www.tei-c.org/ns/1.0}div':
            walk(child, blocks)
        else:
            process_block(child, blocks)


@click.command()
@click.argument('input', type=click.File(mode='rb'))
@click.argument('output', type=click.File(mode='wb'))
def transform_text(input, output):
    document = etree.parse(input).getroot()
    body = document.xpath('/tei:TEI/tei:text/tei:body', namespaces=namespaces)[0]
    blocks = []
    walk(body, blocks)
    body = etree.Element('{http://www.tei-c.org/ns/1.0}body')
    body.extend(blocks)
    output.write(etree.tostring(body, pretty_print=True).decode('utf-8').replace('ns0:', 'tei:').encode('utf-8'))

if __name__ == '__main__':
    transform_text()
