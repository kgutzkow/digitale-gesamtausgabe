import click

from lxml import etree


def matches(range, block):
    range = range.split(' ')
    child_idx = 0
    while child_idx < len(block):
        child = block[child_idx]
        child_idx = child_idx + 1
    return False

def link_annotation(annotation, text_body):
    range = annotation.xpath('tei:citedRange[@type="word-range"]', namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
    if range:
        range = range[0]
        for block in text_body:
            if matches(range.text, block):
                pass


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
