import click
import os
import re
import requests

from copy import deepcopy
from io import StringIO
from lxml import etree


def html_to_teis(text):
    while re.search('\s\s+', text):
        text = re.sub('\s\s+', ' ', text)
    text = text.replace('&', '&amp;')
    return text


def flatten_node(node, styles):
    text = []
    orig_styles = deepcopy(styles)
    if node.tag == 'b':
        if 'font-weight-bold' not in styles:
            styles.append('font-weight-bold')
    elif node.tag == 'font' and 'size' in node.attrib and node.attrib['size'] == '4':
        if 'font-size-large' not in styles:
            styles.append('font-size-large')
    if node.text:
        if styles:
            text.append('<tei:hi style="{0}">{1}</tei:hi>'.format(' '.join(styles), html_to_teis(node.text)))
        else:
            text.append('<tei:seg>{0}</tei:seg>'.format(html_to_teis(node.text)))
    for child in node:
        text.extend(flatten_node(child, deepcopy(styles)))
    if node.tail:
        if orig_styles:
            text.append('<tei:hi style="{0}">{1}</tei:hi>'.format(' '.join(orig_styles), html_to_teis(node.tail)))
        else:
            text.append('<tei:seg>{0}</tei:seg>'.format(html_to_teis(node.tail)))
    return text


def process_block(node):
    text = []
    if node.text:
        text.append('<tei:seg>{0}</tei:seg>'.format(html_to_teis(node.text)))
    for child in node:
        text.extend(flatten_node(child, []))
    return text


def extract_creation_date(content):
    content = content.replace('\n', ' ').replace('\r', ' ')
    match = re.search('Seite\s+angelegt\s+(?:(?:am|im)\s+)?([0-9]{1,2})\.\s*([0-9]{1,2})\.\s*([0-9]{2,4})', content)
    if match:
        year = match.group(3)
        if len(year) == 2:
            year = '20{0}'.format(year)
        month = match.group(2)
        if len(month) == 1:
            month = '0{0}'.format(month)
        day = match.group(1)
        if len(day) == 1:
            day = '0{0}'.format(day)
        return '{0}-{1}-{2}'.format(year, month, day)
    match = re.search('Seite\s+angelegt\s+(?:am|im)\s+([a-zA-Z]+)\.?\s*([0-9]{4})', content)
    if match:
        month = None
        if match.group(1) == 'Januar':
            month = '01'
        elif match.group(1) == 'Februar':
            month = '02'
        elif match.group(1) == 'April':
            month = '04'
        elif match.group(1) == 'Juli':
            month = '07'
        elif match.group(1) == 'September':
            month = '09'
        elif match.group(1) == 'Dezember':
            month = '12'
        else:
            print('--> ' + match.group(1))
        return '{0}-{1}'.format(match.group(2), month)
    match = re.search('Page\s+created\s+([0-9]{2})\.\s*([0-9]{2})\.\s*([0-9]{4})', content)
    if match:
        return '{0}-{1}-{2}'.format(match.group(3), match.group(2), match.group(1))


def extract_title(doc):
    titles = doc.xpath('//font[@size="4"]')
    if titles:
        return ''.join(titles[0].itertext())


def extract_author(content):
    content = content.replace('\n', ' ').replace('\r', ' ')
    match = re.search('Autor(?:in|en)?\s+der\s+Seite:\s*([a-zA-Z ]+)', content)
    if match:
        return match.group(1)
    match = re.search('Author\s+of\s+page:\s*([a-zA-Z ]+)', content)
    if match:
        return match.group(1)


def load_entry(href, target_dir):
    response = requests.get('https://projects.exeter.ac.uk/gutzkow/Gutzneu/gesamtausgabe/{0}'.format(href))
    if response.status_code == 200:
        slug = href[href.rfind('/') + 1:-4]
        print(slug)
        doc = etree.parse(StringIO(response.text), etree.HTMLParser())
        with open(os.path.join(target_dir, '{0}.tei'.format(slug)), 'w') as out_f:
            creation_date = extract_creation_date(response.text)
            title = extract_title(doc)
            author = extract_author(response.text)
            if not author:
                print('--> Blast')
            out_f.write('<tei:TEI xmlns:tei="http://www.tei-c.org/ns/1.0">\n')
            out_f.write('<tei:teiHeader>\n')
            out_f.write('<tei:fileDesc>\n')
            out_f.write('<tei:titleStmt>\n')
            out_f.write('<tei:title>{0}</tei:title>\n'.format(title))
            out_f.write('<tei:author>{0}</tei:author>\n'.format(author))
            out_f.write('<tei:respStmt xml:id="MarkMichaelHall">\n')
            out_f.write('<tei:resp>TEI transform</tei:resp>\n')
            out_f.write('<tei:name>Mark M Hall</tei:name>\n')
            out_f.write('</tei:respStmt>\n')
            out_f.write('</tei:titleStmt>\n')
            out_f.write('<tei:publicationStmt>\n')
            out_f.write('<tei:distributor>Editionsprojekt Karl Gutzkow</tei:distributor>\n')
            out_f.write('</tei:publicationStmt>\n')
            out_f.write('</tei:fileDesc>\n')
            out_f.write('<tei:encodingDesc>\n')
            out_f.write('<tei:classDecl>\n')
            out_f.write('<tei:taxonomy xml:id="gutzkow-taxonomy">\n')
            out_f.write('<tei:bibl>Gutzkow Gesamtausgabe</tei:bibl>\n')
            out_f.write('</tei:taxonomy>\n')
            out_f.write('</tei:classDecl>\n')
            out_f.write('</tei:encodingDesc>\n')
            out_f.write('<tei:sourceDesc>\n')
            out_f.write('<tei:bibl></tei:bibl>\n')
            out_f.write('</tei:sourceDesc>\n')
            out_f.write('<tei:profileDesc>\n')
            out_f.write('<tei:creation>\n')
            out_f.write('<tei:date when="{0}">{0}</tei:date>\n'.format(creation_date))
            out_f.write('</tei:creation>\n')
            out_f.write('<tei:textClass>\n')
            out_f.write('<tei:catRef target="#anhang #lexikon #{0}"/>\n'.format(slug))
            out_f.write('</tei:textClass>\n')
            out_f.write('</tei:profileDesc>\n')
            out_f.write('<tei:revisionDesc>\n')
            out_f.write('<tei:change when="2020-03-30" who="#MarkMichaelHall">Fassung 1.1: TEI Version</tei:change>\n');
            out_f.write('</tei:revisionDesc>\n')
            out_f.write('</tei:teiHeader>\n')
            out_f.write('<tei:text>\n')
            out_f.write('<tei:body>\n')
            for cell in doc.xpath('//td[@colspan="2"]'):
                ignore = False
                for node in cell.iterdescendants(tag=('p', 'h4', 'td')):
                    if node.tag != 'td' and not ignore:
                        if node.tag == 'p':
                            out_f.write('<tei:p>\n')
                        out_f.write('\n'.join(process_block(node)))
                        if node.tag == 'p':
                            out_f.write('</tei:p>\n')
                    else:
                        ignore = True
            out_f.write('</tei:body>\n')
            out_f.write('</tei:text>\n')
            out_f.write('<tei:interpGrp type="global">\n')
            out_f.write('<tei:p style="text-left"/>\n')
            out_f.write('</tei:interpGrp>\n')
            out_f.write('</tei:TEI>\n')


@click.command()
@click.argument('target-dir')
def load_lexikon(target_dir):
    response = requests.get('https://projects.exeter.ac.uk/gutzkow/Gutzneu/gesamtausgabe/lexikon.htm')
    if response.status_code == 200:
        doc = etree.parse(StringIO(response.text), etree.HTMLParser())
        select = doc.xpath('//select')[0]
        for option in select:
            if option.attrib['value'] != 'nothing':
                load_entry(option.attrib['value'], target_dir)


if __name__ == '__main__':
    load_lexikon()
