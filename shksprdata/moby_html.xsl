<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>

<xsl:template match="/">
   <xsl:call-template name="play" />
</xsl:template>

<!--
<xsl:template match="/">
<html>
  <head>
    <title>Open Shakespeare - <xsl:value-of select="PLAY/TITLE" /></title>
    <link rel="stylesheet" href="http://m.okfn.org/okftext/css/okftext/text_basic.css" type="text/css" media="screen" charset="utf-8" />
  </head>
  <body>
   <xsl:call-template name="play" />
  </body>
</html>
</xsl:template>
-->

 <!--Template for Shakespeare play-->
<xsl:template name="play">

<xsl:for-each select="PLAY">
  <h2><xsl:value-of select="TITLE" /></h2> 
  <!-- Could be used to make a character list  
   <xsl:for-each select="PERSONAE/PERSONA">
       <p><xsl:value-of select="current()" /></p>
     </xsl:for-each>  -->
  <xsl:for-each select="ACT" >
    <h3 class="shkspr-act-title"><xsl:value-of select="TITLE" /></h3>
    <xsl:for-each select="SCENE" >
      <xsl:apply-templates />
    </xsl:for-each>
  </xsl:for-each>
</xsl:for-each>
</xsl:template>


<xsl:template match="SCENE/TITLE">
    <h4 class="shkspr-scene-title"><xsl:value-of select="." /></h4>
</xsl:template>

<xsl:template match="SPEECH">
  <div class="shkspr-speech">
  <p class="shkspr-speech-speaker"><xsl:value-of select="SPEAKER" /></p>
  <p class="shkspr-speech-body">
  <xsl:for-each select="LINE" >
    <xsl:apply-templates />
    <br />
  </xsl:for-each>
  </p>
  </div>
</xsl:template>

<xsl:template match="LINE/STAGEDIR">
  [<span class="shkspr-stagedir-inline"><xsl:value-of select="." /></span>]
</xsl:template>

<xsl:template match="STAGEDIR">
  <p class="shkspr-stagedir"><xsl:value-of select="." /></p>
</xsl:template>

</xsl:stylesheet>
