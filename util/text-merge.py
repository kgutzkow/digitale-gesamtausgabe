import click
import json
import re

from copy import deepcopy
from lxml import etree


@click.command()
@click.argument('header', type=click.File(mode='rb'))
@click.argument('body', type=click.File(mode='rb'))
@click.argument('output', type=click.File(mode='wb'))
@click.option('--individual-annotations', type=click.File(mode='rb'))
def merge_text(header, body, output, individual_annotations):
    header = etree.parse(header).getroot()
    body = etree.parse(body).getroot()
    document = etree.Element('{http://www.tei-c.org/ns/1.0}TEI', nsmap={'tei': 'http://www.tei-c.org/ns/1.0'})
    document.append(header)
    text = etree.Element('{http://www.tei-c.org/ns/1.0}text')
    document.append(text)
    text.append(body)
    if individual_annotations:
        text.append(etree.parse(individual_annotations).getroot())
    output.write(etree.tostring(document, xml_declaration=True, pretty_print=True, encoding="UTF-8"))

if __name__ == '__main__':
    merge_text()
