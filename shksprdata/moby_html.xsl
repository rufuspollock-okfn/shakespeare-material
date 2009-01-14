<?xml version="1.0" encoding="ISO-8859-1"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>
<xsl:template match="/">

<html>
<head>


<title>Open Shakespeare - <xsl:value-of select="PLAY/TITLE" /></title>
</head>
<body>
   <xsl:call-template name="play" />
<!-- We'll need to add in other templates for other forms of TEI and add in the templates -->
</body>
</html>
</xsl:template>

 <!--Template for Shakespeare play-->
<xsl:template name="play">

<xsl:for-each select="PLAY">
   <h2><xsl:value-of select="TITLE" /></h2> 
   <!-- Could be used to make a character list  
    <xsl:for-each select="PERSONAE/PERSONA">
        <p><xsl:value-of select="current()" /></p>
      </xsl:for-each>  -->
   <xsl:for-each select="ACT" >
      <h4><xsl:value-of select="TITLE" /></h4>
      <xsl:for-each select="SCENE" >
          <h5><xsl:value-of select="TITLE" /></h5>
              <xsl:for-each select="SPEECH" >
                <p><xsl:value-of select="SPEAKER" /></p>
                <p>
                <xsl:for-each select="LINE" >
                  <xsl:value-of select="current()" /><br />
                </xsl:for-each>
                </p>
              </xsl:for-each>
      </xsl:for-each>
   </xsl:for-each>
</xsl:for-each>

</xsl:template>
</xsl:stylesheet>