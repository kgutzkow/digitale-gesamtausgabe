import json
import os
import re

from lxml import etree
from pelican import signals
from pelican.readers import BaseReader

ns = {'tei': 'http://www.tei-c.org/ns/1.0',
      'gutz': 'https://gutzkow.de/ns/1.0'}

gutzkowNS = etree.FunctionNamespace(ns['gutz'])


@gutzkowNS('ordered-distinct-values')
def ordered_distinct_values(context, input):
    result = []
    for element in input:
        if element not in result:
            result.append(element)
    return result


READER_STYLESHEET = b'''<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" version="1.0">
  <xsl:output method="xml" omit-xml-declaration="yes" indent="yes"/>
  <xsl:template match="tei:TEI">
    <xsl:apply-templates select="tei:text/tei:body"/>
  </xsl:template>
  <xsl:template match="tei:body">
    <div class="text">
      <xsl:apply-templates/>
    </div>
  </xsl:template>
  <xsl:template match="tei:head[@type='level-1']">
    <h1>
      <xsl:copy-of select="@xml:id"/>
      <xsl:copy-of select="@class"/>
      <xsl:copy-of select="@data-heading-id"/>
      <xsl:apply-templates select="tei:seg | tei:hi | tei:foreign | tei:pb | tei:ref"/>
    </h1>
  </xsl:template>
  <xsl:template match="tei:head[@type='level-2']">
    <h2>
      <xsl:copy-of select="@xml:id"/>
      <xsl:copy-of select="@class"/>
      <xsl:copy-of select="@data-heading-id"/>
      <xsl:apply-templates select="tei:seg | tei:hi | tei:foreign | tei:pb | tei:ref"/>
    </h2>
  </xsl:template>
  <xsl:template match="tei:head[@type='level-3']">
    <h3>
      <xsl:copy-of select="@xml:id"/>
      <xsl:copy-of select="@class"/>
      <xsl:copy-of select="@data-heading-id"/>
      <xsl:apply-templates select="tei:seg | tei:hi | tei:foreign | tei:pb | tei:ref"/>
    </h3>
  </xsl:template>
  <xsl:template match="tei:p">
    <p>
      <xsl:if test="@xml:id">
        <xsl:attribute name="id">
          <xsl:value-of select="@xml:id"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:if test="@class">
        <xsl:attribute name="class">
          <xsl:value-of select="@style"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:apply-templates select="tei:seg | tei:hi | tei:foreign | tei:pb | tei:ref"/>
    </p>
  </xsl:template>
  <xsl:template match="tei:lg">
    <div>
      <xsl:if test="@xml:id">
        <xsl:attribute name="id">
          <xsl:value-of select="@xml:id"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:attribute name="class">line-group</xsl:attribute>
      <xsl:apply-templates select="tei:l"/>
    </div>
  </xsl:template>
  <xsl:template match="tei:l">
    <div>
      <xsl:if test="@xml:id">
        <xsl:attribute name="id">
          <xsl:value-of select="@xml:id"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:attribute name="class">line</xsl:attribute>
      <xsl:apply-templates select="tei:seg | tei:hi | tei:foreign | tei:pb | tei:ref"/>
    </div>
  </xsl:template>
  <xsl:template match="tei:seg">
      <xsl:apply-templates select="tei:seg | tei:hi | tei:foreign | tei:pb | tei:ref | text()"/>
  </xsl:template>
  <xsl:template match="tei:hi">
      <span><xsl:attribute name="class"><xsl:value-of select="@style"/></xsl:attribute><xsl:apply-templates select="tei:seg | tei:hi | tei:foreign | tei:pb | tei:ref | text()"/></span>
  </xsl:template>
  <xsl:template match="tei:foreign">
      <span class="foreign-language"><xsl:apply-templates select="tei:seg | tei:hi | tei:foreign | tei:pb | tei:ref | text()"/></span>
  </xsl:template>
  <xsl:template match="tei:pb">
      <span class="page-break"><xsl:value-of select="@n"/></span>
  </xsl:template>
  <xsl:template match="tei:ref">
      <a>
        <xsl:attribute name="data-annotation-target">
          <xsl:value-of select="@target"/>
        </xsl:attribute>
        <xsl:apply-templates select="tei:seg | tei:hi | tei:foreign | tei:pb | tei:ref | text()"/>
      </a>
  </xsl:template>
</xsl:stylesheet>
'''

GLOBAL_COMMENT_STYLESHEET = b'''<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" version="1.0">
  <xsl:output method="xml" omit-xml-declaration="yes" indent="yes"/>
  <xsl:template match="tei:TEI">
    <xsl:apply-templates select="tei:text/tei:interpGrp[@type='global']"/>
  </xsl:template>
  <xsl:template match="tei:body">
    <xsl:apply-templates/>
  </xsl:template>
  <xsl:template match="tei:head[@type='level-1']">
    <h1>
      <xsl:copy-of select="@xml:id"/>
      <xsl:copy-of select="@class"/>
      <xsl:copy-of select="@data-heading-id"/>
      <xsl:apply-templates select="tei:seg | tei:hi | tei:foreign | tei:pb | tei:ref"/>
    </h1>
  </xsl:template>
  <xsl:template match="tei:head[@type='level-2']">
    <h2>
      <xsl:copy-of select="@xml:id"/>
      <xsl:copy-of select="@class"/>
      <xsl:copy-of select="@data-heading-id"/>
      <xsl:apply-templates select="tei:seg | tei:hi | tei:foreign | tei:pb | tei:ref"/>
    </h2>
  </xsl:template>
  <xsl:template match="tei:head[@type='level-3']">
    <h3>
      <xsl:copy-of select="@xml:id"/>
      <xsl:copy-of select="@class"/>
      <xsl:copy-of select="@data-heading-id"/>
      <xsl:apply-templates select="tei:seg | tei:hi | tei:foreign | tei:pb | tei:ref"/>
    </h3>
  </xsl:template>
  <xsl:template match="tei:p">
    <p>
      <xsl:if test="@xml:id">
        <xsl:attribute name="id">
          <xsl:value-of select="@xml:id"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:if test="@class">
        <xsl:attribute name="class">
          <xsl:value-of select="@style"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:apply-templates select="tei:seg | tei:hi | tei:foreign | tei:pb | tei:ref"/>
    </p>
  </xsl:template>
  <xsl:template match="tei:list[@type='sources']">
    <ul class="sources">
      <xsl:apply-templates select="tei:item"/>
    </ul>
  </xsl:template>
  <xsl:template match="tei:item">
    <li>
      <span><xsl:value-of select="@data-source-id"/></span>
      <xsl:apply-templates select="tei:seg | tei:hi | tei:foreign | tei:pb | tei:ref"/>
    </li>
  </xsl:template>
  <xsl:template match="tei:seg">
      <xsl:apply-templates select="tei:seg | tei:hi | tei:foreign | tei:pb | tei:ref | text()"/>
  </xsl:template>
  <xsl:template match="tei:hi">
      <span><xsl:attribute name="class"><xsl:value-of select="@style"/></xsl:attribute><xsl:apply-templates select="tei:seg | tei:hi | tei:foreign | tei:pb | tei:ref | text()"/></span>
  </xsl:template>
  <xsl:template match="tei:foreign">
      <span class="foreign-language"><xsl:apply-templates select="tei:seg | tei:hi | tei:foreign | tei:pb | tei:ref | text()"/></span>
  </xsl:template>
  <xsl:template match="tei:pb">
      <span class="page-break"><xsl:value-of select="@n"/></span>
  </xsl:template>
  <xsl:template match="tei:ref">
      <a>
        <xsl:attribute name="data-annotation-target">
          <xsl:value-of select="@target"/>
        </xsl:attribute>
        <xsl:apply-templates select="tei:seg | tei:hi | tei:foreign | tei:pb | tei:ref | text()"/>
      </a>
  </xsl:template>
</xsl:stylesheet>
'''

NAV_STYLESHEET = b'''<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:gutz="https://gutzkow.de/ns/1.0" version="1.0">
  <xsl:output method="text"/>
  <xsl:template match="tei:TEI">
    <xsl:apply-templates select="tei:text/tei:body"/>
  </xsl:template>
  <xsl:template match="tei:body">
    <xsl:text>{"data":[</xsl:text>
    <xsl:for-each select="gutz:ordered-distinct-values(tei:head/@data-heading-id)">
      <xsl:text>{"type":"heading","id":"</xsl:text>
      <xsl:value-of select="."/>
      <xsl:text>","attributes":{"labels":[</xsl:text>
      <xsl:for-each select="//tei:body/tei:head[@data-heading-id=current()]">
        <xsl:text>{"level":"</xsl:text>
        <xsl:if test="@type='level-1'">
          <xsl:text>1</xsl:text>
        </xsl:if>
        <xsl:if test="@type='level-2'">
          <xsl:text>2</xsl:text>
        </xsl:if>
        <xsl:if test="@type='level-3'">
          <xsl:text>3</xsl:text>
        </xsl:if>
        <xsl:text>","text":"</xsl:text>
        <xsl:apply-templates select="tei:seg | tei:hi | tei:foreign | tei:pb | tei:ref"/>
        <xsl:text>"}</xsl:text>
        <xsl:if test="position() != last()">
          <xsl:text>,</xsl:text>
        </xsl:if>
      </xsl:for-each>
      <xsl:text>]}}</xsl:text>
      <xsl:if test="position() != last()">
        <xsl:text>,</xsl:text>
      </xsl:if>
    </xsl:for-each>
    <xsl:text>]}</xsl:text>
  </xsl:template>
  <xsl:template match="tei:seg | tei:hi | tei:foreign | tei:pb | tei:ref">
    <xsl:value-of select="."/>
  </xsl:template>
</xsl:stylesheet>
'''

ANNOTATION_STYLESHEET = b'''<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" version="1.0">
  <xsl:output method="text"/>
  <xsl:template match="tei:TEI">
    <xsl:text>{"data":[</xsl:text>
    <xsl:apply-templates select="tei:text/tei:interpGrp[@type='individual']"/>
    <xsl:text>]}</xsl:text>
  </xsl:template>
  <xsl:template match="tei:interpGrp">
    <xsl:for-each select="tei:interp">
      <xsl:text>{"type":"annotations","id":"</xsl:text>
      <xsl:value-of select="@xml:id"/>
      <xsl:text>","attributes":{"title":"&amp;lt;span class=\\"page-line-ref\\"&amp;gt;</xsl:text>
      <xsl:value-of select="tei:p/tei:citedRange[@type='page-line-ref']/text()"/>
      <xsl:text>&amp;lt;/span&amp;gt;&amp;lt;span class=\\"word-range\\"&amp;gt;</xsl:text>
      <xsl:value-of select="tei:p/tei:citedRange[@type='word-range']/text()"/>
      <xsl:text>&amp;lt;/span&amp;gt;","content":"</xsl:text>
      <xsl:apply-templates select="tei:p/tei:seg | tei:p/tei:hi | tei:p/tei:foreign | tei:p/tei:ref | tei:p/tei:q"/>
      <xsl:text>"}}</xsl:text>
      <xsl:if test="position() != last()">
        <xsl:text>,</xsl:text>
      </xsl:if>
    </xsl:for-each>
  </xsl:template>
  <xsl:template match="tei:seg | tei:hi | tei:ref">
    <xsl:value-of select="."/>
  </xsl:template>
  <xsl:template match="tei:foreign">
    <xsl:text>&amp;lt;span class=\\"foreign-language\\"&amp;gt;</xsl:text>
    <xsl:value-of select="."/>
    <xsl:text>&amp;lt;/span&amp;gt;</xsl:text>
  </xsl:template>
  <xsl:template match="tei:q">
    <xsl:text>&amp;lt;span class=\\"quote\\"&amp;gt;</xsl:text>
    <xsl:value-of select="."/>
    <xsl:text>&amp;lt;/span&amp;gt;</xsl:text>
  </xsl:template>
</xsl:stylesheet>
'''

OVERVIEW_STYLESHEET = b'''<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" version="1.0">
  <xsl:output method="xml" omit-xml-declaration="yes" indent="yes"/>
  <xsl:template match="tei:TEI">
    <xsl:apply-templates select="tei:text/tei:body"/>
  </xsl:template>
  <xsl:template match="tei:body">
    <div>
      <xsl:apply-templates select="tei:p[position() &lt;= 1]"/>
    </div>
  </xsl:template>
  <xsl:template match="tei:p">
    <xsl:apply-templates select="tei:seg | tei:hi | tei:foreign | tei:pb | tei:ref"/>
  </xsl:template>
  <xsl:template match="tei:seg">
      <xsl:apply-templates select="tei:seg | tei:hi | tei:foreign | tei:pb | tei:ref | text()"/>
  </xsl:template>
  <xsl:template match="tei:hi">
      <span><xsl:attribute name="class"><xsl:value-of select="@style"/></xsl:attribute><xsl:apply-templates select="tei:seg | tei:hi | tei:foreign | tei:pb | tei:ref | text()"/></span>
  </xsl:template>
  <xsl:template match="tei:foreign">
      <span class="foreign-language"><xsl:apply-templates select="tei:seg | tei:hi | tei:foreign | tei:pb | tei:ref | text()"/></span>
  </xsl:template>
  <xsl:template match="tei:pb">
      <span class="page-break"><xsl:value-of select="@n"/></span>
  </xsl:template>
  <xsl:template match="tei:ref">
      <a>
        <xsl:attribute name="data-annotation-target">
          <xsl:value-of select="@target"/>
        </xsl:attribute>
        <xsl:apply-templates select="tei:seg | tei:hi | tei:foreign | tei:pb | tei:ref | text()"/>
      </a>
  </xsl:template>
</xsl:stylesheet>
'''

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


def title_letter(text):
    """Slightly smarter title letter extraction that ignores common articles/prefixes."""
    if text.lower().startswith('der ') or text.lower().startswith('die ') or text.lower().startswith('das ')\
            or text.lower().startswith('zur ') or text.lower().startswith('vom ') or text.lower().startswith('ein '):
        if text[4] != '"':
            return text[4].upper()
        else:
            return text[5].upper()
    elif text.lower().startswith('eine '):
        return text[5].upper()
    elif text.lower().startswith('['):
        return title_letter(text[1:])
    else:
        return text[0].upper()


class TeiDocumentReader(BaseReader):
    """Reader that converts Gutzkow TEI into the structure needed for Pelican and the HTML needed for the
    TEI Reader using a series of XSLT transformations."""
    enabled = True
    file_extensions = ['tei']

    def strip_ns(self, text):
        return re.sub(' xmlns:tei="' + ns['tei'].replace('.', '\\.') + '"', '', text)


    def read(self, filename):
        doc = etree.parse(filename)
        overview = etree.XSLT(etree.XML(OVERVIEW_STYLESHEET))
        reader = etree.XSLT(etree.XML(READER_STYLESHEET))
        nav = etree.XSLT(etree.XML(NAV_STYLESHEET))
        annotation = etree.XSLT(etree.XML(ANNOTATION_STYLESHEET))
        global_comment = etree.XSLT(etree.XML(GLOBAL_COMMENT_STYLESHEET))
        metadata = {'title': str(doc.xpath('//tei:title/text()', namespaces=ns)[0]),
                    'bibl': str(doc.xpath('//tei:sourceDesc/tei:bibl/text()', namespaces=ns)[0]),
                    'date': str(doc.xpath('//tei:creation/tei:date/@when', namespaces=ns)[0]),
                    'year': str(doc.xpath('//tei:creation/tei:date/@when', namespaces=ns)[0])[0:4],
                    'month': MONTH_MAPPING[str(doc.xpath('//tei:creation/tei:date/@when', namespaces=ns)[0])[5:7]],
                    'title-letter': title_letter(str(doc.xpath('//tei:title/text()', namespaces=ns)[0])),
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
                                  for change in doc.xpath('//tei:change', namespaces=ns)],
                    'summary': self.strip_ns(str(overview(doc))),
                    'nav': str(nav(doc)),
                    'annotation': json.loads(self.strip_ns(str(annotation(doc)))),
                    'global_comment': self.strip_ns(str(global_comment(doc))),
                    'template': 'tei-reader'}
        if '<div>' in metadata['summary'] and '</div>' in metadata['summary']:
            summary = metadata['summary']
            summary = summary[summary.find('<div>') + 5:summary.find('</div>')]
            if len(summary) > 900:
                short_summary = []
                length = 0
                for word in summary.split():
                    if length + len(word) > 800:
                        break
                    short_summary.append(word)
                    length = length + len(word)
                short_summary.append('...')
                summary = ' '.join(short_summary)
            metadata['summary'] = summary
        metadata['slug'] = metadata['taxonomy'].split(',')[-1].strip()
        # Link the pdf if it has the same filename as the TEI file
        if os.path.exists(filename.replace('.tei', '.pdf')):
            metadata['pdf'] = '%s.pdf' % metadata['slug']

        parsed = {}
        for key, value in metadata.items():
            parsed[key] = self.process_metadata(key, value)

        return str(reader(doc)), parsed

def add_reader(readers):
    readers.reader_classes['tei'] = TeiDocumentReader

def register():
    signals.readers_init.connect(add_reader)
