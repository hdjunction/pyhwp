<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:import href="hwp5css-common.xsl" />
    <xsl:output method="text" media-type="text/css" encoding="utf-8" indent="no" />

    <xsl:template match="/">
        <xsl:apply-templates select="/" mode="css-rule" />
    </xsl:template>

    <xsl:template match="/" mode="css-rule">
        <xsl:call-template name="css-rule">
            <xsl:with-param name="selector">@page</xsl:with-param>
            <xsl:with-param name="declarations">
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">margin</xsl:with-param>
                    <xsl:with-param name="value">0</xsl:with-param>
                </xsl:call-template>
            </xsl:with-param>
        </xsl:call-template>
        <xsl:call-template name="css-rule">
            <xsl:with-param name="selector">body</xsl:with-param>
            <xsl:with-param name="declarations">
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">padding</xsl:with-param>
                    <xsl:with-param name="value">0</xsl:with-param>
                </xsl:call-template>
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">margin</xsl:with-param>
                    <xsl:with-param name="value">0</xsl:with-param>
                </xsl:call-template>
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">line-height</xsl:with-param>
                    <xsl:with-param name="value">1</xsl:with-param>
                </xsl:call-template>
            </xsl:with-param>
        </xsl:call-template>
        <xsl:call-template name="css-rule">
            <xsl:with-param name="selector">.Paper</xsl:with-param>
            <xsl:with-param name="declarations">
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">overflow</xsl:with-param>
                    <xsl:with-param name="value">hidden</xsl:with-param>
                </xsl:call-template>
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">margin</xsl:with-param>
                    <xsl:with-param name="value">0 auto</xsl:with-param>
                </xsl:call-template>
            </xsl:with-param>
        </xsl:call-template>
        <xsl:call-template name="css-rule">
            <xsl:with-param name="selector">.TableCell</xsl:with-param>
            <xsl:with-param name="declarations">
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">position</xsl:with-param>
                    <xsl:with-param name="value">relative</xsl:with-param>
                </xsl:call-template>
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">padding</xsl:with-param>
                    <xsl:with-param name="value">0</xsl:with-param>
                </xsl:call-template>
            </xsl:with-param>
        </xsl:call-template>
        <xsl:call-template name="css-rule">
            <xsl:with-param name="selector">.Cell</xsl:with-param>
            <xsl:with-param name="declarations">
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">box-sizing</xsl:with-param>
                    <xsl:with-param name="value">border-box</xsl:with-param>
                </xsl:call-template>
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">height</xsl:with-param>
                    <xsl:with-param name="value">100%</xsl:with-param>
                </xsl:call-template>
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">border-color</xsl:with-param>
                    <xsl:with-param name="value">transparent !important</xsl:with-param>
                </xsl:call-template>
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">vertical-align</xsl:with-param>
                    <xsl:with-param name="value">inherit</xsl:with-param>
                </xsl:call-template>
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">line-height</xsl:with-param>
                    <xsl:with-param name="value">0</xsl:with-param>
                </xsl:call-template>
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">letter-spacing</xsl:with-param>
                    <xsl:with-param name="value">-1em</xsl:with-param>
                </xsl:call-template>
            </xsl:with-param>
        </xsl:call-template>
        <xsl:call-template name="css-rule">
            <xsl:with-param name="selector">.CellBody</xsl:with-param>
            <xsl:with-param name="declarations">
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">display</xsl:with-param>
                    <xsl:with-param name="value">inline-block</xsl:with-param>
                </xsl:call-template>
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">width</xsl:with-param>
                    <xsl:with-param name="value">100%</xsl:with-param>
                </xsl:call-template>
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">vertical-align</xsl:with-param>
                    <xsl:with-param name="value">inherit</xsl:with-param>
                </xsl:call-template>
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">line-height</xsl:with-param>
                    <xsl:with-param name="value">1</xsl:with-param>
                </xsl:call-template>
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">letter-spacing</xsl:with-param>
                    <xsl:with-param name="value">0</xsl:with-param>
                </xsl:call-template>
            </xsl:with-param>
        </xsl:call-template>
        <xsl:call-template name="css-rule">
            <xsl:with-param name="selector">.CellAlign</xsl:with-param>
            <xsl:with-param name="declarations">
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">display</xsl:with-param>
                    <xsl:with-param name="value">inline-block</xsl:with-param>
                </xsl:call-template>
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">height</xsl:with-param>
                    <xsl:with-param name="value">100%</xsl:with-param>
                </xsl:call-template>
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">vertical-align</xsl:with-param>
                    <xsl:with-param name="value">middle</xsl:with-param>
                </xsl:call-template>
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">pointer-events</xsl:with-param>
                    <xsl:with-param name="value">none</xsl:with-param>
                </xsl:call-template>
            </xsl:with-param>
        </xsl:call-template>
        <xsl:call-template name="css-rule">
            <xsl:with-param name="selector">.CellStyleBefore, .CellStyleAfter</xsl:with-param>
            <xsl:with-param name="declarations">
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">position</xsl:with-param>
                    <xsl:with-param name="value">absolute</xsl:with-param>
                </xsl:call-template>
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">width</xsl:with-param>
                    <xsl:with-param name="value">100%</xsl:with-param>
                </xsl:call-template>
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">height</xsl:with-param>
                    <xsl:with-param name="value">100%</xsl:with-param>
                </xsl:call-template>
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">background</xsl:with-param>
                    <xsl:with-param name="value">none !important</xsl:with-param>
                </xsl:call-template>
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">pointer-events</xsl:with-param>
                    <xsl:with-param name="value">none</xsl:with-param>
                </xsl:call-template>
            </xsl:with-param>
        </xsl:call-template>
        <xsl:call-template name="css-rule">
            <xsl:with-param name="selector">.CellStyleBefore</xsl:with-param>
            <xsl:with-param name="declarations">
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">top</xsl:with-param>
                    <xsl:with-param name="value">0</xsl:with-param>
                </xsl:call-template>
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">left</xsl:with-param>
                    <xsl:with-param name="value">0</xsl:with-param>
                </xsl:call-template>
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">border-bottom</xsl:with-param>
                    <xsl:with-param name="value">0 !important</xsl:with-param>
                </xsl:call-template>
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">border-right</xsl:with-param>
                    <xsl:with-param name="value">0 !important</xsl:with-param>
                </xsl:call-template>
            </xsl:with-param>
        </xsl:call-template>
        <xsl:call-template name="css-rule">
            <xsl:with-param name="selector">.CellStyleAfter</xsl:with-param>
            <xsl:with-param name="declarations">
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">bottom</xsl:with-param>
                    <xsl:with-param name="value">-1px</xsl:with-param>
                </xsl:call-template>
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">right</xsl:with-param>
                    <xsl:with-param name="value">-1px</xsl:with-param>
                </xsl:call-template>
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">border-top</xsl:with-param>
                    <xsl:with-param name="value">0 !important</xsl:with-param>
                </xsl:call-template>
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">border-left</xsl:with-param>
                    <xsl:with-param name="value">0 !important</xsl:with-param>
                </xsl:call-template>
            </xsl:with-param>
        </xsl:call-template>
        <xsl:apply-templates select="HwpDoc/DocInfo/IdMappings" mode="css-rule" />
        <xsl:call-template name="css-rule">
            <xsl:with-param name="selector">.Normal</xsl:with-param>
            <xsl:with-param name="declarations">
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">min-height</xsl:with-param>
                    <xsl:with-param name="value">0.5mm</xsl:with-param>
                </xsl:call-template>
                <xsl:call-template name="css-declaration">
                    <xsl:with-param name="property">line-height</xsl:with-param>
                    <xsl:with-param name="value">1</xsl:with-param>
                </xsl:call-template>
            </xsl:with-param>
        </xsl:call-template>
    </xsl:template>
</xsl:stylesheet>
