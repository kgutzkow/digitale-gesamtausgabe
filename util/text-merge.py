import click
import json
import re

from copy import deepcopy
from lxml import etree


@click.command()
@click.argument('header', type=click.File(mode='rb'))
@click.argument('body', type=click.File(mode='rb'))
@click.argument('output', type=click.File(mode='wb'))
def merge_text(header, body, output):
    header = etree.parse(header).getroot()
    body = etree.parse(body).getroot()
    document = etree.Element('{http://www.tei-c.org/ns/1.0}TEI', nsmap={'tei': 'http://www.tei-c.org/ns/1.0'})
    document.append(header)
    text = etree.Element('{http://www.tei-c.org/ns/1.0}text')
    document.append(text)
    text.append(body)
    output.write(etree.tostring(document, pretty_print=True,xml_declaration=True, encoding="UTF-8"))

if __name__ == '__main__':
    merge_text()
