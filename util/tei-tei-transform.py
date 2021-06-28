import click
import re

from lxml import etree

ns = {'tei': 'http://www.tei-c.org/ns/1.0'}


def create_basic_structure() -> etree.ElementTree:
    """Create a basic TEI document."""
    tei = etree.Element('{http://www.tei-c.org/ns/1.0}TEI')
    return etree.ElementTree(tei)


def create_header(source: etree.ElementTree, target: etree.ElementTree):
    """Create the minimal TEI header structure."""
    title = etree.Element('{http://www.tei-c.org/ns/1.0}title',
                          text=source.xpath('tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title/text()',
                                            namespaces=ns)[0])
    author = etree.Element('{http://www.tei-c.org/ns/1.0}author',
                          text=source.xpath('tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:author/text()',
                                            namespaces=ns)[0])
    titleStmt = etree.Element('{http://www.tei-c.org/ns/1.0}titleStmt')
    titleStmt.append(title)
    titleStmt.append(author)
    fileDesc = etree.Element('{http://www.tei-c.org/ns/1.0}fileDesc')
    fileDesc.append(titleStmt)
    teiHeader = etree.Element('{http://www.tei-c.org/ns/1.0}teiHeader')
    teiHeader.append(fileDesc)
    target.getroot().append(teiHeader)


def process_block_element(node: etree.Element, parent: etree.Element, tag: str) -> etree.Element:
    """Process a block element, creating the required structure."""
    if node.text or len(node) > 0:
        block = etree.Element(tag)
        if node.text and node.text.strip():
            seg = etree.Element('{http://www.tei-c.org/ns/1.0}seg')
            seg.text = re.sub(r'\s+', ' ', node.text)
            block.append(seg)
        for child in node:
            process_body(child, block)
        parent.append(block)
        if node.tail and node.tail.strip():
            seg = etree.Element('{http://www.tei-c.org/ns/1.0}seg', text=node.tail)
            p = etree.Element('{http://www.tei-c.org/ns/1.0}p')
            p.append(seg)
            parent.append(p)
        return block


def process_inline_element(node: etree.Element, parent: etree.Element, tag: str) -> etree.Element:
    """Process an inline element, creating the required structure."""
    if node.text:
        inline = etree.Element(tag)
        if node.text:
            inline.text = re.sub(r'\s+', ' ', node.text)
        tail = None
        if node.tail:
            tail = etree.Element('{http://www.tei-c.org/ns/1.0}seg')
            tail.text = re.sub(r'\s+', ' ', node.tail)
        if parent.tag in ['{http://www.tei-c.org/ns/1.0}p', '{http://www.tei-c.org/ns/1.0}head', '{http://www.tei-c.org/ns/1.0}l']:
            parent.append(inline)
            if tail is not None:
                parent.append(tail)
        else:
            p = etree.Element('{http://www.tei-c.org/ns/1.0}p')
            p.append(inline)
            if tail is not None:
                p.append(tail)
            parent.append(p)
        return inline
    elif len(node) > 0:
        nodes = []
        for child in node:
            tmp = etree.Element('{http://www.tei-c.org/ns/1.0}p')
            process_body(child, tmp)
            for result in tmp:
                inline = etree.Element(tag)
                if result.tag == '{http://www.tei-c.org/ns/1.0}seg':
                    inline.text = result.text
                else:
                    inline.append(result)
                nodes.append(inline)
        if parent.tag in ['{http://www.tei-c.org/ns/1.0}p', '{http://www.tei-c.org/ns/1.0}head', '{http://www.tei-c.org/ns/1.0}l']:
            parent.extend(nodes)
        else:
            p = etree.Element('{http://www.tei-c.org/ns/1.0}p')
            p.extend(nodes)
            parent.append(p)


def process_body(node: etree.Element, parent: etree.Element):
    """Process the body of the text."""
    if node.tag == '{http://www.tei-c.org/ns/1.0}body':
        for child in node:
            process_body(child, parent)
    elif node.tag == '{http://www.tei-c.org/ns/1.0}div':
        for child in node:
            process_body(child, parent)
    elif node.tag == '{http://www.tei-c.org/ns/1.0}head':
        head = process_block_element(node, parent, '{http://www.tei-c.org/ns/1.0}head')
        if head is not None:
            head.attrib['type'] = 'level-1'
    elif node.tag == '{http://www.tei-c.org/ns/1.0}stage':
        stage = process_inline_element(node, parent, '{http://www.tei-c.org/ns/1.0}stage')
        if stage is not None:
            stage.attrib['type'] = node.attrib['type']
    elif node.tag == '{http://www.tei-c.org/ns/1.0}sp':
        process_block_element(node, parent, '{http://www.tei-c.org/ns/1.0}sp')
    elif node.tag == '{http://www.tei-c.org/ns/1.0}speaker':
        process_inline_element(node, parent, '{http://www.tei-c.org/ns/1.0}speaker')
    elif node.tag == '{http://www.tei-c.org/ns/1.0}lg':
        process_block_element(node, parent, '{http://www.tei-c.org/ns/1.0}lg')
    elif node.tag == '{http://www.tei-c.org/ns/1.0}l':
        process_block_element(node, parent, '{http://www.tei-c.org/ns/1.0}l')
    elif node.tag == '{http://www.tei-c.org/ns/1.0}p':
        process_block_element(node, parent, '{http://www.tei-c.org/ns/1.0}p')
    elif node.tag == '{http://www.tei-c.org/ns/1.0}foreign':
        process_inline_element(node, parent, '{http://www.tei-c.org/ns/1.0}foreign')
    elif node.tag == '{http://www.tei-c.org/ns/1.0}emph':
        hi = process_inline_element(node, parent, '{http://www.tei-c.org/ns/1.0}hi')
        if hi is not None:
            hi.attrib['style'] = 'font-style-italic'
    elif node.tag == '{http://www.tei-c.org/ns/1.0}add':
        pb = process_inline_element(node, parent, '{http://www.tei-c.org/ns/1.0}pb')
        if pb is not None:
            match = re.search(r'\[(.+)\]', pb.text)
            if match:
                pb.attrib['n'] = match.group(1)
                if pb.text.endswith(' '):
                    seg = etree.Element('{http://www.tei-c.org/ns/1.0}seg')
                    seg.text = ' '
                    if parent.tag in ['{http://www.tei-c.org/ns/1.0}p', '{http://www.tei-c.org/ns/1.0}head', '{http://www.tei-c.org/ns/1.0}l']:
                        parent.append(seg)
                    else:
                        p = etree.Element('{http://www.tei-c.org/ns/1.0}p')
                        p.append(seg)
                        parent.append(p)
                pb.text = None
            else:
                pb.tag = '{http://www.tei-c.org/ns/1.0}seg'

    elif node.tag == '{http://www.tei-c.org/ns/1.0}note':
        pass
    else:
        print(node.tag)


def create_body(source: etree.ElementTree, target: etree.ElementTree):
    """Create the body structure."""
    body = etree.Element('{http://www.tei-c.org/ns/1.0}body')
    process_body(source.xpath('tei:text/tei:body', namespaces=ns)[0], body)
    text = etree.Element('{http://www.tei-c.org/ns/1.0}text')
    text.append(body)
    target.getroot().append(text)


def create_apparatus(target: etree.ElementTree):
    """Create the basic apparatus structure."""
    interpGrp = etree.Element('{http://www.tei-c.org/ns/1.0}interpGrp')
    interpGrp.attrib['type'] = 'global'
    text = target.xpath('tei:text', namespaces=ns)[0]
    text.append(interpGrp)


@click.command()
@click.argument('src', type=click.File())
@click.argument('dest', type=click.File(mode='wb'))
def convert(src, dest):
    """Convert a TEI XML file into the DEE TEI XML structure."""
    source = etree.parse(src)
    target = create_basic_structure()
    create_header(source, target)
    create_body(source, target)
    create_apparatus(target)
    target.write(dest, pretty_print=True, xml_declaration=True, encoding='utf-8')


if __name__ == '__main__':
    convert()
