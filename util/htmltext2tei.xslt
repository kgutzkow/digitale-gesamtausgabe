<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns="http://www.tei-c.org/ns/1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:guz="http://gutzkow.de" version="1.0">
  <xsl:output method="xml" indent="yes"/>

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
        <bibl>Die Sterbecassirer. Bambocciade. In: Novellen von Karl Gutzkow. Bd 1, Hamburg: Hoffmann und Campe, 1834, S. 107-128. (Rasch 2.4.1.3)</bibl>
      </sourceDesc>
      <revisionDesc>
        <change when="1999-05" who="#GertVonhoff">Erstfassung</change>
        <change when="1999-08" who="#GertVonhoff">Fassung 1.2 in Berlin</change>
        <change when="2000-02" who="#GertVonhoff">Fassung 1.3 in Wittenberg</change>
        <change when="2000-06" who="#GertVonhoff">Fassung 1.5 in Birmingham: erste Testnetzfassung</change>
        <change when="2000-12" who="#GertVonhoff">Fassung 1.6 in Birmingham/Münster: EKG geprüft</change>
        <change when="2001-08" who="#GertVonhoff">Fassung 1.7 in Münster/Exeter: Seitenzählung umgestellt auf Novellenband</change>
        <change when="2002-10-15" who="#GertVonhoff">Fassung 1.7a: Kopf- und Fussbereich für neues Websitelayout angepasst</change>
        <change when="2018-04-25" who="#MarkHall">Fassung 1.8: Auf TEI umgestellt</change>
      </revisionDesc>
    </teiHeader>
  </xsl:template>

  <xsl:template match="title">
    <titleStmt>
      <title><xsl:value-of select="."/></title>
      <author>Karl Gutzkow</author>
      <respStmt xml:id="GertVonhoff">
        <resp>Digital edition</resp>
        <name>Gert Vonhoff</name>
      </respStmt>
      <respStmt xml:id="MarkMichaelHall">
        <resp>TEI transform</resp>
        <name>Mark M Hall</name>
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
