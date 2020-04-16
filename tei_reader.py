import json
import os
import re

from lxml import etree
from pelican import signals
from pelican.readers import BaseReader

ns = {'tei': 'http://www.tei-c.org/ns/1.0',
      'gutz': 'https://gutzkow.de/ns/1.0'}


MONTH_MAPPING = {
    '01': (1, 'Januar'),
    '02': (2, 'Februar'),
    '03': (3, 'März'),
    '04': (4, 'April'),
    '05': (5, 'Mai'),
    '06': (6, 'Juni'),
    '07': (7, 'Juli'),
    '08': (8, 'August'),
    '09': (9, 'September'),
    '10': (10, 'Oktober'),
    '11': (11, 'November'),
    '12': (12, 'Dezember'),
    '': (13, '')
}


class TeiDocumentReader(BaseReader):
    """Reader that converts Gutzkow TEI into the structure needed for Pelican and the HTML needed for the
    TEI Reader using a series of XSLT transformations."""
    enabled = True
    file_extensions = ['tei']

    def strip_ns(self, text):
        return re.sub(' xmlns:tei="' + ns['tei'].replace('.', '\\.') + '"', '', text)


    def read(self, filename):
        doc = etree.parse(filename)
        metadata = {'title': str(doc.xpath('//tei:title/text()', namespaces=ns)[0]),
                    'date': str(doc.xpath('//tei:creation/tei:date/@when', namespaces=ns)[0]),
                    'year': str(doc.xpath('//tei:creation/tei:date/@when', namespaces=ns)[0])[0:4],
                    'month': MONTH_MAPPING[str(doc.xpath('//tei:creation/tei:date/@when', namespaces=ns)[0])[5:7]],
                    'title-letter': str(doc.xpath('//tei:title/text()', namespaces=ns)[0])[0].upper(),
                    'taxonomy': ', '.join([t[1:] for t in str(doc.xpath('//tei:catRef/@target', namespaces=ns)[0]).split(' ')]),
                    'authors': [str(author) for author in doc.xpath('//tei:author/text()', namespaces=ns)],
                    'editors': [{'role': str(editor.xpath('./tei:resp/text()', namespaces=ns)[0]),
                                 'name': str(editor.xpath('./tei:name/text()', namespaces=ns)[0])}
                                for editor in doc.xpath('//tei:respStmt', namespaces=ns)],
                    'revisions': [{'revision': change.text,
                                   'date': change.attrib['when'],
                                   'name': [str(doc.xpath("//tei:respStmt[@xml:id='%s']/tei:name/text()" % resp[1:],
                                                          namespaces=ns)[0])
                                            for resp in change.attrib['who'].split(' ')]}
                                  for change in doc.xpath('//tei:change', namespaces=ns)
                                  if 'when' in change and 'who' in change and change.text],
                    'extract': '',
                    'template': 'tei-document'}
        if doc.xpath('//tei:sourceDesc/tei:bibl/text()', namespaces=ns):
            metadata['bibl'] = str(doc.xpath('//tei:sourceDesc/tei:bibl/text()', namespaces=ns)[0])
        metadata['slug'] = metadata['taxonomy'].split(',')[-1].strip()
        extracts = doc.xpath('//tei:body/*[@data-extract="true"]', namespaces=ns)
        if len(extracts) == 0:
            extracts = doc.xpath('//tei:body/tei:p', namespaces=ns)
        if len(extracts) > 0:
            metadata['extract'] = ''.join(['<p>{0}</p>'.format(''.join(node.itertext())) for node in extracts[:2]])
        # Link the pdf if it has the same filename as the TEI file
        if os.path.exists(filename.replace('.tei', '.pdf')):
            metadata['pdf'] = '%s.pdf' % metadata['slug']

        parsed = {}
        for key, value in metadata.items():
            parsed[key] = self.process_metadata(key, value)

        return etree.tostring(doc).decode('utf-8'), parsed

def add_reader(readers):
    readers.reader_classes['tei'] = TeiDocumentReader

def register():
    signals.readers_init.connect(add_reader)
