"""
Schopenhauer Styles - Design constants and styling utilities.

This module defines the visual identity of Schopenhauer documents,
including colors, fonts, spacing, and default styles.

The color scheme is inspired by deep philosophical contemplation -
rich burgundy/wine colors representing depth of thought.
"""

from dataclasses import dataclass
from enum import Enum

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Inches, Pt, RGBColor

# =============================================================================
# COLOR PALETTE - Burgundy/Wine theme (Schopenhauer's contemplative aesthetic)
# =============================================================================

class Colors(Enum):
    """Schopenhauer color palette - Deep, contemplative burgundy tones."""

    # Primary colors
    PRIMARY = "722F37"        # Burgundy/Wine - main brand color
    PRIMARY_DARK = "4A1C23"   # Dark burgundy - headings, emphasis
    PRIMARY_LIGHT = "A64D57"  # Light burgundy - accents

    # Secondary colors
    SECONDARY = "2C3E50"      # Dark slate - body text, professional
    SECONDARY_LIGHT = "34495E"  # Lighter slate

    # Accent colors
    ACCENT = "D4A574"         # Gold/bronze - highlights, call-outs
    ACCENT_LIGHT = "E8C9A0"   # Light gold

    # Semantic colors
    SUCCESS = "27AE60"        # Green - success, positive
    WARNING = "F39C12"        # Orange - warnings, attention
    DANGER = "C0392B"         # Red - errors, critical
    INFO = "3498DB"           # Blue - information

    # Neutral colors
    WHITE = "FFFFFF"
    BLACK = "000000"
    GRAY_100 = "F8F9FA"       # Lightest gray - backgrounds
    GRAY_200 = "E9ECEF"
    GRAY_300 = "DEE2E6"
    GRAY_400 = "CED4DA"
    GRAY_500 = "ADB5BD"       # Medium gray
    GRAY_600 = "6C757D"
    GRAY_700 = "495057"
    GRAY_800 = "343A40"
    GRAY_900 = "212529"       # Darkest gray

    @property
    def rgb(self) -> RGBColor:
        """Convert hex color to RGBColor object."""
        hex_color = self.value
        return RGBColor(
            int(hex_color[0:2], 16),
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16)
        )

    @classmethod
    def from_hex(cls, hex_color: str) -> RGBColor:
        """Convert any hex color string to RGBColor."""
        hex_color = hex_color.lstrip('#')
        return RGBColor(
            int(hex_color[0:2], 16),
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16)
        )


# Convenience access to colors
COLORS = Colors

# Brand colors dictionary for easy access
BRAND = {
    "primary": Colors.PRIMARY.value,
    "primary_dark": Colors.PRIMARY_DARK.value,
    "primary_light": Colors.PRIMARY_LIGHT.value,
    "secondary": Colors.SECONDARY.value,
    "accent": Colors.ACCENT.value,
    "success": Colors.SUCCESS.value,
    "warning": Colors.WARNING.value,
    "danger": Colors.DANGER.value,
    "info": Colors.INFO.value,
}


# =============================================================================
# TYPOGRAPHY - Font definitions
# =============================================================================

@dataclass
class FontSpec:
    """Font specification with family, size, and style options."""
    family: str
    size: int  # in points
    bold: bool = False
    italic: bool = False
    color: str = Colors.SECONDARY.value

    @property
    def size_pt(self) -> Pt:
        return Pt(self.size)

    @property
    def color_rgb(self) -> RGBColor:
        return Colors.from_hex(self.color)


class Fonts:
    """Font definitions for document elements."""

    # Heading fonts - Using Cambria for a classic, professional look
    TITLE = FontSpec("Cambria", 28, bold=True, color=Colors.PRIMARY_DARK.value)
    HEADING_1 = FontSpec("Cambria", 24, bold=True, color=Colors.PRIMARY_DARK.value)
    HEADING_2 = FontSpec("Cambria", 20, bold=True, color=Colors.PRIMARY.value)
    HEADING_3 = FontSpec("Cambria", 16, bold=True, color=Colors.PRIMARY.value)
    HEADING_4 = FontSpec("Cambria", 14, bold=True, color=Colors.SECONDARY.value)
    HEADING_5 = FontSpec("Cambria", 12, bold=True, color=Colors.SECONDARY.value)

    # Body fonts - Using Calibri for readability
    BODY = FontSpec("Calibri", 11, color=Colors.SECONDARY.value)
    BODY_LARGE = FontSpec("Calibri", 12, color=Colors.SECONDARY.value)
    BODY_SMALL = FontSpec("Calibri", 10, color=Colors.GRAY_600.value)

    # Special purpose fonts
    SUBTITLE = FontSpec("Calibri", 14, italic=True, color=Colors.GRAY_600.value)
    CAPTION = FontSpec("Calibri", 9, italic=True, color=Colors.GRAY_600.value)
    QUOTE = FontSpec("Georgia", 12, italic=True, color=Colors.GRAY_700.value)
    CODE = FontSpec("Consolas", 10, color=Colors.GRAY_800.value)

    # Table fonts
    TABLE_HEADER = FontSpec("Calibri", 11, bold=True, color=Colors.WHITE.value)
    TABLE_BODY = FontSpec("Calibri", 10, color=Colors.SECONDARY.value)

    # Footer/Header fonts
    HEADER = FontSpec("Calibri", 10, color=Colors.GRAY_500.value)
    FOOTER = FontSpec("Calibri", 9, color=Colors.GRAY_500.value)


FONTS = Fonts


# =============================================================================
# SPACING AND LAYOUT
# =============================================================================

class Margins:
    """Page margin presets."""

    NORMAL = {
        "top": Inches(1),
        "bottom": Inches(1),
        "left": Inches(1),
        "right": Inches(1),
    }

    NARROW = {
        "top": Inches(0.5),
        "bottom": Inches(0.5),
        "left": Inches(0.5),
        "right": Inches(0.5),
    }

    MODERATE = {
        "top": Inches(1),
        "bottom": Inches(1),
        "left": Inches(0.75),
        "right": Inches(0.75),
    }

    WIDE = {
        "top": Inches(1),
        "bottom": Inches(1),
        "left": Inches(1.5),
        "right": Inches(1.5),
    }

    MIRRORED = {
        "top": Inches(1),
        "bottom": Inches(1),
        "left": Inches(1.25),
        "right": Inches(1),
    }


MARGINS = Margins


class PageSizes:
    """Standard page size definitions."""

    LETTER = {"width": Inches(8.5), "height": Inches(11)}
    LEGAL = {"width": Inches(8.5), "height": Inches(14)}
    A4 = {"width": Cm(21), "height": Cm(29.7)}
    A5 = {"width": Cm(14.8), "height": Cm(21)}
    EXECUTIVE = {"width": Inches(7.25), "height": Inches(10.5)}


PAGE_SIZES = PageSizes


class Spacing:
    """Paragraph and element spacing."""

    # Paragraph spacing (in points)
    PARA_BEFORE = Pt(0)
    PARA_AFTER = Pt(8)
    PARA_AFTER_HEADING = Pt(6)

    # Line spacing
    LINE_SINGLE = 1.0
    LINE_1_15 = 1.15
    LINE_1_5 = 1.5
    LINE_DOUBLE = 2.0

    # Default line spacing
    LINE_DEFAULT = LINE_1_15

    # Indentation
    FIRST_LINE_INDENT = Inches(0.5)
    LIST_INDENT = Inches(0.25)
    QUOTE_INDENT = Inches(0.5)


SPACING = Spacing


# =============================================================================
# STYLE PRESETS
# =============================================================================

@dataclass
class StylePreset:
    """Complete style preset for document elements."""
    font: FontSpec
    alignment: WD_ALIGN_PARAGRAPH = WD_ALIGN_PARAGRAPH.LEFT
    space_before: Pt = Pt(0)
    space_after: Pt = Pt(8)
    line_spacing: float = 1.15
    first_line_indent: Inches = None
    left_indent: Inches = None


class Styles:
    """Pre-defined style presets for common document elements."""

    # Headings
    TITLE = StylePreset(
        font=Fonts.TITLE,
        alignment=WD_ALIGN_PARAGRAPH.CENTER,
        space_before=Pt(24),
        space_after=Pt(12),
    )

    HEADING_1 = StylePreset(
        font=Fonts.HEADING_1,
        space_before=Pt(24),
        space_after=Pt(6),
    )

    HEADING_2 = StylePreset(
        font=Fonts.HEADING_2,
        space_before=Pt(18),
        space_after=Pt(6),
    )

    HEADING_3 = StylePreset(
        font=Fonts.HEADING_3,
        space_before=Pt(12),
        space_after=Pt(4),
    )

    # Body styles
    NORMAL = StylePreset(
        font=Fonts.BODY,
        space_after=Pt(8),
        line_spacing=1.15,
    )

    BODY_INDENTED = StylePreset(
        font=Fonts.BODY,
        space_after=Pt(8),
        line_spacing=1.15,
        first_line_indent=Inches(0.5),
    )

    # Special styles
    QUOTE = StylePreset(
        font=Fonts.QUOTE,
        alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
        space_before=Pt(12),
        space_after=Pt(12),
        left_indent=Inches(0.5),
    )

    CAPTION = StylePreset(
        font=Fonts.CAPTION,
        alignment=WD_ALIGN_PARAGRAPH.CENTER,
        space_before=Pt(4),
        space_after=Pt(12),
    )

    # List styles
    BULLET = StylePreset(
        font=Fonts.BODY,
        space_after=Pt(4),
        left_indent=Inches(0.25),
    )

    NUMBERED = StylePreset(
        font=Fonts.BODY,
        space_after=Pt(4),
        left_indent=Inches(0.25),
    )


STYLES = Styles


# =============================================================================
# TABLE STYLES
# =============================================================================

class TableStyles:
    """Table styling presets."""

    @staticmethod
    def apply_header_style(cell, color: Colors = Colors.PRIMARY):
        """Apply header styling to a table cell."""
        from docx.oxml import parse_xml
        from docx.oxml.ns import nsdecls

        # Set background color
        shading = parse_xml(
            f'<w:shd {nsdecls("w")} w:fill="{color.value}" w:val="clear"/>'
        )
        cell._tc.get_or_add_tcPr().append(shading)

        # Style text
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
                run.font.color.rgb = Colors.WHITE.rgb
                run.font.name = Fonts.TABLE_HEADER.family
                run.font.size = Fonts.TABLE_HEADER.size_pt

    @staticmethod
    def apply_body_style(cell):
        """Apply body styling to a table cell."""
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.name = Fonts.TABLE_BODY.family
                run.font.size = Fonts.TABLE_BODY.size_pt
                run.font.color.rgb = Fonts.TABLE_BODY.color_rgb

    @staticmethod
    def apply_alternating_rows(table, even_color: str = Colors.GRAY_100.value):
        """Apply alternating row colors to a table."""
        from docx.oxml import parse_xml
        from docx.oxml.ns import nsdecls

        for i, row in enumerate(table.rows):
            if i > 0 and i % 2 == 0:  # Skip header row
                for cell in row.cells:
                    shading = parse_xml(
                        f'<w:shd {nsdecls("w")} w:fill="{even_color}" w:val="clear"/>'
                    )
                    cell._tc.get_or_add_tcPr().append(shading)


TABLE_STYLES = TableStyles


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB values to hex string."""
    return f"{r:02x}{g:02x}{b:02x}"


def lighten_color(hex_color: str, factor: float = 0.3) -> str:
    """Lighten a hex color by a factor (0-1)."""
    r, g, b = hex_to_rgb(hex_color)
    r = min(255, int(r + (255 - r) * factor))
    g = min(255, int(g + (255 - g) * factor))
    b = min(255, int(b + (255 - b) * factor))
    return rgb_to_hex(r, g, b)


def darken_color(hex_color: str, factor: float = 0.3) -> str:
    """Darken a hex color by a factor (0-1)."""
    r, g, b = hex_to_rgb(hex_color)
    r = max(0, int(r * (1 - factor)))
    g = max(0, int(g * (1 - factor)))
    b = max(0, int(b * (1 - factor)))
    return rgb_to_hex(r, g, b)
