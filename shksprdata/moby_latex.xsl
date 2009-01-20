<?xml version="1.0" encoding="ISO-8859-1"?>
<!--
Could target plain LaTeX but preference is to use a pre-existing package:

  * dramatist: fairly recent, good docs and reasonably sophisticated.
    * <http://tug.ctan.org/cgi-bin/ctanPackageInformation.py?id=dramatist>
    * <http://www.tug.org/texlive/Contents/live/texmf-dist/doc/latex/dramatist/>
  
  * play: slightly more recent and usable as both class and package had
    problems getting act/scene etc working
    * <http://www.ctan.org/tex-archive/macros/latex/contrib/play/>
  
  * plari: Looks old and v. basic (also a class not a package)
    * <http://www.ctan.org/tex-archive/macros/latex/contrib/plari/>
  
  * drama: old (1996) and no longer updated.
    * <http://www.ctan.org/tex-archive/macros/latex/contrib/frankenstein/unsupported/drama.pdf>

  * xmlplay: specifically for Bosak Shakespeare and uses play
    * <http://www.ctan.org/tex-archive/help/Catalogue/entries/xmlplay.html>

Can get many of these on Ubuntu/Debian by installing:

    texlive-humanities
    texlive-latex-extra

Also relevant for general layout:

  * memoir pacakge.
  * verse
-->

<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:es="http://openshakespeare.org/functions"
  >
<xsl:output method="text" encoding="UTF-8"/>
<xsl:template match="/">
\documentclass{book}
\usepackage{verse}
\usepackage{dramatist}

\title{<xsl:value-of select="PLAY/TITLE" />}
\author{by William Shakespeare\\[5em]
  The Open Shakespeare Edition
} 

\begin{document}
\begin{titlepage}
\maketitle
\end{titlepage}

\tableofcontents

<xsl:apply-templates select="//PERSONAE/*" />

\DramPer

\vspace{5 em}

{\large <xsl:value-of select="//PLAY//SCNDESCR" />}

<xsl:apply-templates select="//ACT" />
\end{document}
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

<xsl:template match="SPEECH">
\begin{drama*}
<!-- \<xsl:value-of select="es:norm_name(string(SPEAKER))" />speaks -->
\speaker{<xsl:value-of select="SPEAKER" />}
<xsl:for-each select="LINE">
  <xsl:value-of select="." />\\
</xsl:for-each>
\end{drama*}
</xsl:template>

</xsl:stylesheet>
