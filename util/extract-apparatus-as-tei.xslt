<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns="http://www.tei-c.org/ns/1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:guz="http://gutzkow.de" version="1.0">
  <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
  <xsl:strip-space elements="*"/>

  <!-- Ignore elements -->
  <xsl:template match="head|div">
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

  <xsl:template match="div[@data-boundary='kommentierung']">
    <xsl:apply-templates select="div"/>
  </xsl:template>

  <!-- Process the Globalkommentar section -->
  <xsl:template match="div[@data-boundary='global']">
    <div type="comment">
      <xsl:apply-templates select="p"/>
    </div>
  </xsl:template>

  <xsl:template match="div[@data-boundary='global']/p[guz:filter_characters(text(), '')]">
    <p>
      <xsl:apply-templates select="i|text()"/>
    </p>
  </xsl:template>

  <xsl:template match="div[@data-boundary='global']//a[@name]">
    <anchor>
      <xsl:attribute name="xml:id"><xsl:value-of select="@name"/></xsl:attribute>
    </anchor>
  </xsl:template>

  <!-- Process the Einzelkommentare section -->
  <xsl:template match="div[@data-boundary='einzel']">
    <div type="annotations">
      <xsl:apply-templates select="p"/>
    </div>
  </xsl:template>

  <xsl:template match="div[@data-boundary='einzel']/p">
    <note anchored="false">
      <xsl:attribute name="xml:id"><xsl:value-of select="guz:non_empty(a[@class='tex']/following-sibling::a[@name][1]/@name, a[@class='tex']/preceding-sibling::a[@name][1]/@name)"/></xsl:attribute>
      <xsl:attribute name="target">#page-<xsl:value-of select="b"/></xsl:attribute>
      <title><xsl:value-of select="a[@class='tex']"/></title>
      <p><xsl:apply-templates select="i[position() &gt; 1]|text()"/></p>
    </note>
  </xsl:template>

  <!-- Einzelkommentare are wrapped in a <i> -->
  <xsl:template match="div[@data-boundary='einzel']/p/i">
    <xsl:apply-templates/>
  </xsl:template>

  <!-- Cross-reference transform -->
  <xsl:template match="a[@href]">
    <ref>
      <xsl:attribute name="target"><xsl:value-of select="guz:trim_crossref(@href)"/></xsl:attribute>
      <xsl:attribute name="type"><xsl:value-of select="guz:classify_crossref(@href)"/></xsl:attribute>
      <xsl:apply-templates/>
    </ref>
  </xsl:template>

  <xsl:template match="a[@class='pic']">
    <figure>
      <graphic>
        <xsl:attribute name="url"><xsl:value-of select="@href"/></xsl:attribute>
      </graphic>
      <head><xsl:value-of select="."/></head>
    </figure>
  </xsl:template>

  <!-- Emphasis transform -->
  <xsl:template match="div[@data-boundary='einzel']/p/i//b">
    <emph rend="strong"><xsl:apply-templates/></emph>
  </xsl:template>

  <xsl:template match="div[@data-boundary='einzel']/p/text()">
    <xsl:if test="guz:filter_characters(., ']')">
      <emph><xsl:value-of select="."/></emph>
    </xsl:if>
  </xsl:template>

  <xsl:template match="div[@data-boundary='einzel']/p/i/font[@face]">
    <emph><xsl:value-of select="."/></emph>
  </xsl:template>

  <!-- Pass-through nested <i> -->
  <xsl:template match="div[@data-boundary='einzel']/p/i//i">
    <xsl:apply-templates/>
  </xsl:template>

</xsl:stylesheet>
