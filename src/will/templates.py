"""
Schopenhauer Templates - Built-in document templates and template utilities.

This module provides pre-configured templates for common document types
and utilities for working with custom templates.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional


@dataclass
class TemplateConfig:
    """Configuration for a document template."""
    name: str
    description: str
    page_size: str = "letter"
    orientation: str = "portrait"
    margins: str = "normal"
    font_body: str = "Calibri"
    font_heading: str = "Cambria"
    primary_color: str = "722F37"  # Burgundy
    secondary_color: str = "2C3E50"  # Dark slate
    accent_color: str = "D4A574"  # Gold
    include_header: bool = False
    header_text: str = ""
    include_footer: bool = True
    include_page_numbers: bool = True
    footer_text: str = ""
    line_spacing: float = 1.15
    first_line_indent: float = 0.0
    sections: list[dict[str, Any]] = field(default_factory=list)


# =============================================================================
# BUILT-IN TEMPLATES
# =============================================================================

BUILTIN_TEMPLATES: dict[str, TemplateConfig] = {
    "default": TemplateConfig(
        name="default",
        description="Clean, professional default template",
        page_size="letter",
        margins="normal",
        include_footer=True,
        include_page_numbers=True,
    ),

    "report": TemplateConfig(
        name="report",
        description="Business report with header and footer",
        page_size="letter",
        margins="moderate",
        include_header=True,
        header_text="{{TITLE}}",
        include_footer=True,
        include_page_numbers=True,
        footer_text="{{AUTHOR}} - {{DATE}}",
        line_spacing=1.15,
    ),

    "memo": TemplateConfig(
        name="memo",
        description="Internal memo format",
        page_size="letter",
        margins="normal",
        include_header=False,
        include_footer=False,
        line_spacing=1.0,
        sections=[
            {"type": "heading", "title": "MEMORANDUM", "level": 0},
            {"type": "content", "text": "TO: {{TO}}"},
            {"type": "content", "text": "FROM: {{FROM}}"},
            {"type": "content", "text": "DATE: {{DATE}}"},
            {"type": "content", "text": "RE: {{SUBJECT}}"},
            {"type": "horizontal_line"},
        ],
    ),

    "letter": TemplateConfig(
        name="letter",
        description="Formal business letter",
        page_size="letter",
        margins="normal",
        include_header=False,
        include_footer=False,
        line_spacing=1.0,
        sections=[
            {"type": "content", "text": "{{SENDER_ADDRESS}}"},
            {"type": "content", "text": ""},
            {"type": "content", "text": "{{DATE}}"},
            {"type": "content", "text": ""},
            {"type": "content", "text": "{{RECIPIENT_NAME}}"},
            {"type": "content", "text": "{{RECIPIENT_ADDRESS}}"},
            {"type": "content", "text": ""},
            {"type": "content", "text": "Dear {{RECIPIENT_NAME}}:"},
        ],
    ),

    "academic": TemplateConfig(
        name="academic",
        description="Academic paper format (APA-style)",
        page_size="letter",
        margins="normal",
        font_body="Times New Roman",
        font_heading="Times New Roman",
        include_header=True,
        header_text="{{RUNNING_HEAD}}",
        include_footer=True,
        include_page_numbers=True,
        line_spacing=2.0,
        first_line_indent=0.5,
    ),

    "proposal": TemplateConfig(
        name="proposal",
        description="Project proposal template",
        page_size="letter",
        margins="moderate",
        include_header=True,
        header_text="{{COMPANY}} - Proposal",
        include_footer=True,
        include_page_numbers=True,
        footer_text="Confidential",
        sections=[
            {"type": "heading", "title": "{{TITLE}}", "level": 0},
            {"type": "content", "text": "Prepared for: {{CLIENT}}"},
            {"type": "content", "text": "Prepared by: {{AUTHOR}}"},
            {"type": "content", "text": "Date: {{DATE}}"},
            {"type": "page_break"},
        ],
    ),

    "manual": TemplateConfig(
        name="manual",
        description="Technical documentation / user manual",
        page_size="letter",
        margins="moderate",
        include_header=True,
        header_text="{{PRODUCT_NAME}} - User Manual",
        include_footer=True,
        include_page_numbers=True,
        footer_text="Version {{VERSION}}",
    ),

    "contract": TemplateConfig(
        name="contract",
        description="Legal contract format",
        page_size="letter",
        margins="normal",
        font_body="Times New Roman",
        include_header=False,
        include_footer=True,
        include_page_numbers=True,
        footer_text="Page {{PAGE}} of {{TOTAL_PAGES}}",
        line_spacing=1.5,
    ),

    "resume": TemplateConfig(
        name="resume",
        description="Professional resume/CV template",
        page_size="letter",
        margins="narrow",
        include_header=False,
        include_footer=False,
        line_spacing=1.0,
    ),

    "newsletter": TemplateConfig(
        name="newsletter",
        description="Company newsletter format",
        page_size="letter",
        margins="narrow",
        include_header=True,
        header_text="{{NEWSLETTER_NAME}} - {{ISSUE_DATE}}",
        include_footer=True,
        include_page_numbers=True,
    ),

    "minutes": TemplateConfig(
        name="minutes",
        description="Meeting minutes template",
        page_size="letter",
        margins="normal",
        include_header=False,
        include_footer=True,
        include_page_numbers=True,
        sections=[
            {"type": "heading", "title": "Meeting Minutes", "level": 0},
            {"type": "content", "text": "Date: {{DATE}}"},
            {"type": "content", "text": "Time: {{TIME}}"},
            {"type": "content", "text": "Location: {{LOCATION}}"},
            {"type": "content", "text": "Attendees: {{ATTENDEES}}"},
            {"type": "horizontal_line"},
        ],
    ),

    "invoice": TemplateConfig(
        name="invoice",
        description="Business invoice template",
        page_size="letter",
        margins="normal",
        include_header=False,
        include_footer=True,
        footer_text="Thank you for your business!",
    ),

    "a4": TemplateConfig(
        name="a4",
        description="A4 page size (European standard)",
        page_size="a4",
        margins="normal",
        include_footer=True,
        include_page_numbers=True,
    ),

    "a4-narrow": TemplateConfig(
        name="a4-narrow",
        description="A4 page size with narrow margins",
        page_size="a4",
        margins="narrow",
        include_footer=True,
        include_page_numbers=True,
    ),

    "legal": TemplateConfig(
        name="legal",
        description="Legal page size",
        page_size="legal",
        margins="normal",
        font_body="Times New Roman",
        include_footer=True,
        include_page_numbers=True,
        line_spacing=1.5,
    ),
}


# =============================================================================
# TEMPLATE FUNCTIONS
# =============================================================================

def get_template(name: str) -> Optional[TemplateConfig]:
    """
    Get a built-in template by name.

    Args:
        name: Template name.

    Returns:
        TemplateConfig or None if not found.
    """
    return BUILTIN_TEMPLATES.get(name.lower())


def list_templates() -> list[dict[str, str]]:
    """
    List all available built-in templates.

    Returns:
        List of template info dictionaries.
    """
    return [
        {
            "name": config.name,
            "description": config.description,
            "page_size": config.page_size,
        }
        for config in BUILTIN_TEMPLATES.values()
    ]


def get_template_names() -> list[str]:
    """
    Get list of all template names.

    Returns:
        List of template names.
    """
    return list(BUILTIN_TEMPLATES.keys())


def apply_template(doc, template_name: str) -> bool:
    """
    Apply a template configuration to a document.

    Args:
        doc: WordDocument instance.
        template_name: Name of the template to apply.

    Returns:
        True if template was applied, False if not found.
    """
    config = get_template(template_name)
    if not config:
        return False

    # Apply page settings
    doc.set_page_size(preset=config.page_size, orientation=config.orientation)
    doc.set_margins(preset=config.margins)

    # Apply header/footer
    if config.include_header and config.header_text:
        doc.set_header(config.header_text)

    if config.include_footer:
        doc.set_footer(
            text=config.footer_text,
            include_page_numbers=config.include_page_numbers,
        )

    # Apply initial sections
    for section in config.sections:
        doc._process_section(section)

    return True


def create_custom_template(
    name: str,
    description: str = "",
    **kwargs
) -> TemplateConfig:
    """
    Create a custom template configuration.

    Args:
        name: Template name.
        description: Template description.
        **kwargs: Additional template settings.

    Returns:
        TemplateConfig instance.
    """
    return TemplateConfig(
        name=name,
        description=description,
        **kwargs
    )


# =============================================================================
# YAML SPEC TEMPLATES
# =============================================================================

YAML_TEMPLATES = {
    "blank": """# Schopenhauer Document Specification
# Blank template - customize as needed

title: Document Title
subtitle: Optional Subtitle
author: Your Name

# Page setup
page_size: letter  # letter, legal, a4, a5
margins: normal    # normal, narrow, moderate, wide

# Header/Footer
header: ""
footer: ""

# Content sections
sections: []
""",

    "report": """# Schopenhauer Document Specification
# Business Report Template

title: Quarterly Report
subtitle: Q4 2024 Results
author: Jane Smith

page_size: letter
margins: moderate

header: "{{COMPANY_NAME}} - Confidential"
footer: "Prepared by {{AUTHOR}}"

table_of_contents: true
title_page_break: true

sections:
  - type: section
    title: Executive Summary
    page_break: false

  - type: content
    text: |
      This report summarizes the key findings and results
      for the fourth quarter of 2024.

  - type: section
    title: Key Metrics
    page_break: true

  - type: table
    title: Performance Summary
    headers:
      - Metric
      - Q3 2024
      - Q4 2024
      - Change
    data:
      - [Revenue, "$1.2M", "$1.5M", "+25%"]
      - [Users, "10,000", "15,000", "+50%"]
      - [NPS Score, "72", "78", "+6"]

  - type: section
    title: Analysis
    page_break: true

  - type: content
    bullets:
      - Revenue increased by 25% quarter-over-quarter
      - User acquisition exceeded targets
      - Customer satisfaction improved significantly

  - type: section
    title: Next Steps
    page_break: true

  - type: content
    numbered:
      - Continue marketing initiatives
      - Expand product features
      - Focus on customer retention
""",

    "memo": """# Schopenhauer Document Specification
# Internal Memo Template

title: Internal Memorandum

page_size: letter
margins: normal

sections:
  - type: content
    text: "TO: {{RECIPIENT}}"

  - type: content
    text: "FROM: {{SENDER}}"

  - type: content
    text: "DATE: {{DATE}}"

  - type: content
    text: "RE: {{SUBJECT}}"

  - type: horizontal_line

  - type: content
    text: |
      [Your memo content goes here]
""",

    "proposal": """# Schopenhauer Document Specification
# Project Proposal Template

title: Project Proposal
subtitle: "{{PROJECT_NAME}}"
author: "{{COMPANY_NAME}}"

page_size: letter
margins: moderate

header: "Proposal - {{CLIENT_NAME}}"
footer: "Confidential"

table_of_contents: true

sections:
  - type: section
    title: Introduction
    page_break: true

  - type: content
    text: |
      Thank you for the opportunity to present this proposal.
      We are excited about the possibility of working with {{CLIENT_NAME}}.

  - type: section
    title: Project Overview
    page_break: true

  - type: content
    title: Objectives
    bullets:
      - Objective 1
      - Objective 2
      - Objective 3

  - type: section
    title: Scope of Work
    page_break: true

  - type: content
    text: The following deliverables are included in this proposal.

  - type: table
    title: Deliverables
    headers:
      - Item
      - Description
      - Timeline
    data:
      - [Phase 1, "Discovery and Planning", "2 weeks"]
      - [Phase 2, "Design and Development", "6 weeks"]
      - [Phase 3, "Testing and Launch", "2 weeks"]

  - type: section
    title: Investment
    page_break: true

  - type: table
    title: Pricing
    headers:
      - Service
      - Cost
    data:
      - [Phase 1, "$X,XXX"]
      - [Phase 2, "$XX,XXX"]
      - [Phase 3, "$X,XXX"]
      - ["**Total**", "**$XX,XXX**"]

  - type: section
    title: Next Steps
    page_break: true

  - type: content
    numbered:
      - Review this proposal
      - Schedule a follow-up call
      - Sign agreement and begin work
""",

    "meeting-minutes": """# Schopenhauer Document Specification
# Meeting Minutes Template

title: Meeting Minutes

page_size: letter
margins: normal

sections:
  - type: table
    headers:
      - Field
      - Value
    data:
      - [Meeting Title, "{{MEETING_TITLE}}"]
      - [Date, "{{DATE}}"]
      - [Time, "{{TIME}}"]
      - [Location, "{{LOCATION}}"]
      - [Facilitator, "{{FACILITATOR}}"]

  - type: heading
    title: Attendees
    level: 2

  - type: content
    bullets:
      - Attendee 1
      - Attendee 2
      - Attendee 3

  - type: heading
    title: Agenda Items
    level: 2

  - type: content
    numbered:
      - Item 1
      - Item 2
      - Item 3

  - type: heading
    title: Discussion Notes
    level: 2

  - type: content
    text: "[Meeting discussion notes]"

  - type: heading
    title: Action Items
    level: 2

  - type: table
    headers:
      - Action
      - Owner
      - Due Date
    data:
      - [Action item 1, "Owner 1", "Date"]
      - [Action item 2, "Owner 2", "Date"]

  - type: heading
    title: Next Meeting
    level: 2

  - type: content
    text: "Date: {{NEXT_MEETING_DATE}}"
""",

    "documentation": """# Schopenhauer Document Specification
# Technical Documentation Template

title: Product Documentation
subtitle: User Guide
author: Technical Writing Team

page_size: letter
margins: moderate

header: "{{PRODUCT_NAME}} Documentation"
footer: "Version {{VERSION}}"

table_of_contents: true

sections:
  - type: section
    title: Introduction
    page_break: true

  - type: content
    text: |
      Welcome to the {{PRODUCT_NAME}} documentation.
      This guide will help you get started and make the most of the product.

  - type: section
    title: Getting Started
    page_break: true

  - type: content
    title: Prerequisites
    level: 2

  - type: content
    bullets:
      - Requirement 1
      - Requirement 2
      - Requirement 3

  - type: content
    title: Installation
    level: 2

  - type: code
    language: bash
    text: |
      pip install {{PRODUCT_NAME}}

  - type: section
    title: Configuration
    page_break: true

  - type: content
    text: Configure the product using the following settings.

  - type: table
    title: Configuration Options
    headers:
      - Option
      - Default
      - Description
    data:
      - [option1, "value1", "Description of option1"]
      - [option2, "value2", "Description of option2"]

  - type: section
    title: Usage
    page_break: true

  - type: content
    title: Basic Usage
    level: 2

  - type: content
    text: Here is how to use the basic features.

  - type: code
    language: python
    text: |
      from product import Client
      client = Client()
      result = client.do_something()

  - type: section
    title: Troubleshooting
    page_break: true

  - type: content
    text: Common issues and their solutions.

  - type: table
    headers:
      - Issue
      - Solution
    data:
      - [Problem 1, "Solution 1"]
      - [Problem 2, "Solution 2"]
""",
}


def get_yaml_template(name: str) -> Optional[str]:
    """
    Get a YAML template by name.

    Args:
        name: Template name.

    Returns:
        YAML template string or None.
    """
    return YAML_TEMPLATES.get(name.lower())


def list_yaml_templates() -> list[str]:
    """
    List available YAML templates.

    Returns:
        List of template names.
    """
    return list(YAML_TEMPLATES.keys())


def save_yaml_template(name: str, output_path: str) -> bool:
    """
    Save a YAML template to a file.

    Args:
        name: Template name.
        output_path: Output file path.

    Returns:
        True if saved successfully.
    """
    template = get_yaml_template(name)
    if not template:
        return False

    Path(output_path).write_text(template, encoding='utf-8')
    return True
