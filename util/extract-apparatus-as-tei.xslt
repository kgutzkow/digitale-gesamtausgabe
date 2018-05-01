<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns="http://www.tei-c.org/ns/1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:guz="http://gutzkow.de" version="1.0">
  <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
  <xsl:strip-space elements="*"/>

  <!-- Ignore elements -->
  <xsl:template match="head">
  </xsl:template>

  <!-- Construct the root structure -->
  <xsl:template match="/">
    <TEI>
      <xsl:apply-templates/>
    </TEI>
  </xsl:template>

  <!-- Construct the main body text -->
  <xsl:template match="body">
    <text>
      <body typeof="Apparatus" about="">
        <xsl:apply-templates/>
      </body>
    </text>
  </xsl:template>

  <xsl:template match="div[@data-processing='boundary' and @data-boundary='kommentierung']">
    <xsl:apply-templates select="div"/>
  </xsl:template>

  <xsl:template match="div[@data-processing='boundary' and @data-boundary='einzel']">
    <xsl:apply-templates select="p"/>
  </xsl:template>

  <xsl:template match="div[@data-processing='boundary' and @data-boundary='einzel']/p">
    <note anchored="false">
      <xsl:attribute name="xml:id"><xsl:value-of select="a[@class='tex']/following-sibling::a[@name][1]/@name"/></xsl:attribute>
      <xsl:attribute name="target">#page-<xsl:value-of select="b"/></xsl:attribute>
      <title><xsl:value-of select="a[@class='tex']"/></title>
      <p><xsl:apply-templates select="i[position() &gt; 1]|text()"/></p>
    </note>
  </xsl:template>

  <xsl:template match="div[@data-processing='boundary' and @data-boundary='einzel']/p/i">
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="div[@data-processing='boundary' and @data-boundary='einzel']/p/i//b">
    <strong><xsl:apply-templates/></strong>
  </xsl:template>

  <xsl:template match="div[@data-processing='boundary' and @data-boundary='einzel']/p/i//a">
    <ref>
      <xsl:apply-templates/>
    </ref>
  </xsl:template>

  <xsl:template match="div[@data-processing='boundary' and @data-boundary='einzel']/p/i//i">
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="div">
  </xsl:template>

</xsl:stylesheet>
