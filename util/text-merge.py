import click
import json
import re

from copy import deepcopy
from lxml import etree


@click.command()
@click.option('--header', '-h', type=click.File(mode='rb'))
@click.option('--text', '-t', type=click.File(mode='rb'), multiple=True)
@click.argument('output', type=click.File(mode='wb'))
def merge_text(header, text, output):
    document = etree.Element('{http://www.tei-c.org/ns/1.0}TEI', nsmap={'tei': 'http://www.tei-c.org/ns/1.0'})
    if header:
        document.append(etree.parse(header).getroot())
    textElement = etree.Element('{http://www.tei-c.org/ns/1.0}text')
    document.append(textElement)
    for source in text:
        textElement.append(etree.parse(source).getroot())
    output.write(etree.tostring(document, xml_declaration=True, pretty_print=True, encoding="UTF-8"))

if __name__ == '__main__':
    merge_text()
