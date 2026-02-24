"""
Schopenhauer MCP Server - Model Context Protocol interface for AI agents.

This module provides an MCP server that allows AI agents to render professional
documents from Markdown and structured data.
"""

import os
from pathlib import Path
from typing import Any, Optional

from fastmcp import FastMCP

from will.render import render as do_render

# Create MCP server
mcp = FastMCP("Schopenhauer")


@mcp.tool()
def render_document(
    source: str,
    output_path: str,
    format: Optional[str] = None,
    template: Optional[str] = None,
    variables: Optional[dict[str, Any]] = None,
    pandoc_args: Optional[list[str]] = None,
) -> str:
    """
    Render a document from Markdown or structured data.

    Args:
        source: Markdown content or path to a .md/.yaml/.json file.
        output_path: Path where the generated document should be saved.
        format: Output format (docx, pdf, html, etc.). Inferred from output_path if not given.
        template: Optional template name or path to a .docx reference document.
        variables: Optional variables for template substitution.
        pandoc_args: Optional list of extra arguments to pass to Pandoc (e.g. ["--toc"]).
    """
    try:
        # If source is a path that exists, use it. Otherwise treat as raw markdown.
        if Path(source).suffix and not Path(source).exists():
            # Looks like a path but doesn't exist? 
            # If it's a multi-line string, it's definitely markdown.
            if "
" not in source:
                return f"Error: Source file not found: {source}"

        result_path = do_render(
            source=source,
            output=output_path,
            format=format,
            template=template,
            variables=variables,
            extra_args=pandoc_args,
        )
        return f"Successfully rendered document to: {result_path}"
    except Exception as e:
        return f"Error rendering document: {str(e)}"


@mcp.tool()
def list_available_templates() -> list[dict[str, str]]:
    """List all built-in document templates."""
    from will.templates import list_templates
    return list_templates()


if __name__ == "__main__":
    mcp.run()
