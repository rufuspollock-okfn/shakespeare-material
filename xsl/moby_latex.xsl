<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:es="http://openshakespeare.org/functions"
  >
<xsl:output method="text" encoding="UTF-8"/>


<xsl:template match="/">
<xsl:apply-templates select="//PERSONAE/*" />

\DramPer

\vspace{5 em}

{\large <xsl:value-of select="//PLAY//SCNDESCR" />}

<xsl:apply-templates select="//ACT" />
</xsl:template>


<xsl:template match="PERSONAE/TITLE" />

<xsl:template match="PGROUP">
\begin{CharacterGroup}{<xsl:value-of select="GRPDESCR" />}
<xsl:apply-templates select="PERSONA" />\end{CharacterGroup}

</xsl:template>

<xsl:template match="PGROUP/PERSONA">  \GCharacter{<xsl:value-of select="current()" />}{<xsl:value-of select="current()" />}{<xsl:value-of select="es:norm_name(string(.))" />}
</xsl:template>

<xsl:template match="PERSONA">  \Character[<xsl:value-of select="current()" />]{<xsl:value-of select="current()" />}{<xsl:value-of select="es:norm_name(string(.))" />}
</xsl:template>

<xsl:template match="ACT">
\act

<xsl:apply-templates select="SCENE" />
</xsl:template>

<!-- do nothing for ACT or SCENE TITLE -->
<xsl:template match="ACT//TITLE" />

<xsl:template match="SCENE">
<!-- 
\Scene{<xsl:value-of select="TITLE" />}
-->
\scene

<xsl:value-of select="TITLE" />
<xsl:apply-templates />
</xsl:template>

<xsl:template match="STAGEDIR">
\StageDir{<xsl:value-of select="." />}
</xsl:template>

<xsl:template match="SPEECH/STAGEDIR">
\direct{<xsl:value-of select="current" />}
</xsl:template>

<xsl:template match="LINE/STAGEDIR">
[<xsl:value-of select="." />]
</xsl:template>

<xsl:template match="SPEECH">
\begin{drama*}
<!-- \<xsl:value-of select="es:norm_name(string(SPEAKER))" />speaks -->
\speaker{<xsl:value-of select="SPEAKER" />}
<xsl:for-each select="LINE">
  <xsl:apply-templates />\\
</xsl:for-each>
\end{drama*}
</xsl:template>

</xsl:stylesheet>
