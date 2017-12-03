<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" 
    xmlns:xhtml="http://www.w3.org/1999/xhtml"
    exclude-result-prefixes="xs" version="2.0">


    <xsl:template match="node() | @*">
        <xsl:copy>
            <xsl:apply-templates select="node() | @*"/>
        </xsl:copy>
    </xsl:template>

    <xsl:template
        match="xhtml:h2[@class='HwSectionTitle'] | xhtml:div[@class='HwContentNavigation'] | xhtml:div[@class='HwContentInformation'] | meta-data.collection[@type='Facets']"/>


    <xsl:template match="meta-data.simple-collection|prebuilt.head|prebuilt.legal|prebuilt.creditsfooter"/>
    <xsl:template match="prebuilt.disclaimer|prebuilt.copyright|prebuilt.navstack|h2"/>
    <xsl:template match="meta-data.collections |  meta-data.collection[@type='Lexicon'] | meta-data.collection[@type='Keywords'] | meta-data.collection[@type='Categories']"/>
    <xsl:template match="prebuilt.medialist|prebuilt.navigation|doc.sections| meta-data.credits | section.meta-data | @fingerprint-exact | @fingerprint | comment()"/>
    
    
    <xsl:template match="section.std[@type='References']"/>
    
    <xsl:template match="xhtml:div[@class='HwNavigationSection HwCreditsSection ']"/>
    <xsl:template match="//*[@class='HwSectionTitle']"/>
    <xsl:template match="xhtml:div[@class='HwCitations']"/>
    <xsl:template match="xhtml:div[@class='HwContentHeader']"/>
    <xsl:template match="xhtml:div[@class='HwContentTitle']"/>
    <xsl:template match="xhtml:div[@class='HwContentHeader']"/>
    <xsl:template match="xhtml:div[@class='HwCustom']"/>
    <xsl:template match="xhtml:div[@class='HwNavigationSection HwSectionReferences']"/>
    <xsl:template match="h2[@class='HwSectionTitle']"/>
    <xsl:template match="div[@class='HwNavigationSection HwSectionReferences']"/>
    
    <!-- xsl:template match ="xhtml:div[@class='HwContent']">
        <xsl:value-of select="."/>
    </xsl:template -->
    
    <!-- xsl:template match="xhtml:h3[starts-with(@class, 'HwSubSectionTitle')]"/ -->
    
    
   
    
    
    
   

</xsl:stylesheet>
