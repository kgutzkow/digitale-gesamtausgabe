<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns="http://www.tei-c.org/ns/1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:guz="http://gutzkow.de" version="1.0">
  <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
  <xsl:strip-space elements="*"/>

  <!-- Ignore elements -->
  <xsl:template match="script|a[@name]">
  </xsl:template>

  <!-- Construct the root structure -->
  <xsl:template match="/">
    <TEI>
      <xsl:apply-templates/>
    </TEI>
  </xsl:template>

  <!-- Construct the document header -->
  <xsl:template match="head">
    <teiHeader>
      <fileDesc>
        <xsl:apply-templates/>
        <publicationStmt>
          <distributor>Editionsprojekt Karl Gutzkow</distributor>
        </publicationStmt>
      </fileDesc>
      <sourceDesc>
        <bibl></bibl>
      </sourceDesc>
      <revisionDesc>
      </revisionDesc>
    </teiHeader>
  </xsl:template>

  <xsl:template match="title">
    <titleStmt>
      <title><xsl:value-of select="."/></title>
      <author>Karl Gutzkow</author>
      <respStmt xml:id="PLACEHOLDER">
        <resp></resp>
        <name></name>
      </respStmt>
    </titleStmt>
  </xsl:template>

  <!-- Construct the main body text -->
  <xsl:template match="body">
    <text>
      <body>
        <xsl:apply-templates/>
      </body>
    </text>
  </xsl:template>

  <!-- Construct the main text elements -->
  <xsl:template match="h2">
    <head type="main"><xsl:apply-templates/></head>
  </xsl:template>

  <xsl:template match="h3">
    <head type="sub"><xsl:apply-templates/></head>
  </xsl:template>

  <xsl:template match="p">
    <p><xsl:apply-templates/></p>
  </xsl:template>

  <!-- Construct page numbers -->
  <xsl:template match="i">
    <pb>
      <xsl:attribute name="n">
        <xsl:value-of select="guz:trim_pagenumber(text())"/>
      </xsl:attribute>
    </pb>
  </xsl:template>

  <!-- Construct links to the Einzelstellenerläuterung -->
  <xsl:template match="a[@class='erl']">
    <ref>
      <xsl:attribute name="target">
        <xsl:value-of select="guz:trim_crossref(@href)"/>
      </xsl:attribute>
      <xsl:attribute name="type">annotation</xsl:attribute>
      <xsl:apply-templates/>
    </ref>
  </xsl:template>

  <!-- Construct links to the spelling variants -->
  <xsl:template match="a[@class='var']">
    <ref>
      <xsl:attribute name="target">
        <xsl:value-of select="./preceding-sibling::a[1]/@name"/>
      </xsl:attribute>
      <xsl:attribute name="type">spelling-variation</xsl:attribute>
      <xsl:apply-templates/>
    </ref>
  </xsl:template>

</xsl:stylesheet>
