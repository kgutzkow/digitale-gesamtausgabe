from lxml import etree
from pelican import signals
from pelican.readers import BaseReader

ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

READER_STYLESHEET = b'''<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:guz="http://gutzkow.de" version="1.0">
  <xsl:output method="xml" omit-xml-declaration="yes" indent="yes"/>
  <xsl:template match="tei:teiHeader"></xsl:template>
  <xsl:template match="tei:body">
    <xsl:apply-templates select="tei:div[@typeof='Story']"/>
  </xsl:template>
  <xsl:template match="tei:head[@type='main']">
    <h1><xsl:apply-templates/></h1>
  </xsl:template>
  <xsl:template match="tei:head[@type='sub']">
    <h2><xsl:apply-templates/></h2>
  </xsl:template>
  <xsl:template match="tei:p">
    <p><xsl:apply-templates/></p>
  </xsl:template>
  <xsl:template match="tei:pb">
    <span class="page-break"><xsl:value-of select="@n"/></span>
  </xsl:template>
  <xsl:template match="tei:ref[@type='annotation']">
    <xsl:apply-templates/>
  </xsl:template>
</xsl:stylesheet>'''

OVERVIEW_STYLESHEET = b'''<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:guz="http://gutzkow.de" version="1.0">
  <xsl:output method="xml" omit-xml-declaration="yes" indent="yes"/>
  <xsl:template match="tei:teiHeader"></xsl:template>
  <xsl:template match="tei:body">
    <xsl:apply-templates select="./tei:div[@typeof='Story']/tei:p[position() &lt;= 3]"/>
  </xsl:template>
  <xsl:template match="tei:p">
    <p><xsl:apply-templates/></p>
  </xsl:template>
</xsl:stylesheet>
'''

COMMENTS_STYLESHEET = b'''<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:guz="http://gutzkow.de" version="1.0">
  <xsl:output method="xml" omit-xml-declaration="yes" indent="yes"/>
  <xsl:template match="tei:teiHeader"></xsl:template>
  <xsl:template match="tei:body">
    <xsl:apply-templates select="./tei:div[@typeof='Apparatus']/tei:div[@type='comment']"/>
  </xsl:template>
  <xsl:template match="tei:p">
    <p><xsl:apply-templates/></p>
  </xsl:template>
</xsl:stylesheet>
'''

class NewReader(BaseReader):
    enabled = True
    file_extensions = ['tei']

    def read(self, filename):
        doc = etree.parse(filename)
        overview = etree.XSLT(etree.XML(OVERVIEW_STYLESHEET))
        reader = etree.XSLT(etree.XML(READER_STYLESHEET))
        comments = etree.XSLT(etree.XML(COMMENTS_STYLESHEET))
        metadata = {'title': str(doc.xpath('//tei:title/text()', namespaces=ns)[0]),
                    'bibl': str(doc.xpath('//tei:sourceDesc/tei:bibl/text()', namespaces=ns)[0]),
                    'date': str(doc.xpath('//tei:creation/tei:date/@when', namespaces=ns)[0]),
                    'taxonomy': [t[1:] for t in str(doc.xpath('//tei:catRef/@target', namespaces=ns)[0]).split(' ')],
                    'authors': [str(author) for author in doc.xpath('//tei:author/text()', namespaces=ns)],
                    'editors': [{'role': str(editor.xpath('./tei:resp/text()', namespaces=ns)[0]),
                                 'name': str(editor.xpath('./tei:name/text()', namespaces=ns)[0])}
                                for editor in doc.xpath('//tei:respStmt', namespaces=ns)],
                    'revisions': [{'revision': change.text,
                                   'date': change.attrib['when'],
                                   'name': doc.xpath("//tei:respStmt[@xml:id='%s']/tei:name/text()" % change.attrib['who'][1:],
                                                     namespaces=ns)}
                                  for change in doc.xpath('//tei:change', namespaces=ns)],
                    'summary': str(overview(doc)),
                    'comments': str(comments(doc)),
                    'template': 'tei-reader'}

        parsed = {}
        for key, value in metadata.items():
            parsed[key] = self.process_metadata(key, value)

        return str(reader(doc)), parsed

def add_reader(readers):
    readers.reader_classes['tei'] = NewReader

def register():
    signals.readers_init.connect(add_reader)
