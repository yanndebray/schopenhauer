"""
Schopenhauer CLI - The 'will' command-line interface.

This module provides the CLI for creating and manipulating Word documents.

Usage:
    will create -o report.docx --title "My Report"
    will generate spec.yaml -o output.docx
    will inspect template.docx
    will new -o document.docx
    will add document.docx --title "New Section"
    will replace document.docx KEY=VALUE
    will template list
    will cloud generate spec.yaml
"""

import json
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from will import __version__
from will.core import WordDocument
from will.document import create_document
from will.styles import BRAND
from will.templates import (
    get_template,
    get_template_names,
    get_yaml_template,
    list_templates,
    list_yaml_templates,
    save_yaml_template,
)

# Create console with safe defaults for Windows
console = Console(force_terminal=True, safe_box=True, legacy_windows=True)


# =============================================================================
# CLI GROUP
# =============================================================================


@click.group(invoke_without_command=True)
@click.option("--version", "-v", is_flag=True, help="Show version and exit.")
@click.pass_context
def main(ctx, version):
    """
    Schopenhauer's Will - A powerful Word document generator.

    Generate professional Word documents from YAML/JSON specifications
    or create them interactively.

    \b
    Examples:
        will create -o report.docx --title "Annual Report"
        will generate spec.yaml -o output.docx
        will template init report -o spec.yaml
        will cloud generate spec.yaml -o output.docx
    """
    if version:
        console.print(f"[bold]Schopenhauer's Will[/bold] version [cyan]{__version__}[/cyan]")
        console.print(
            f"Primary color: [bold #{BRAND['primary']}]Burgundy[/bold #{BRAND['primary']}]"
        )
        ctx.exit()

    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())


# =============================================================================
# CREATE COMMAND
# =============================================================================


@main.command()
@click.option("--output", "-o", required=True, help="Output file path (.docx)")
@click.option("--title", "-t", help="Document title")
@click.option("--subtitle", "-s", help="Document subtitle")
@click.option("--author", "-a", help="Document author")
@click.option("--template", help="Template file (.docx) or built-in template name")
@click.option(
    "--page-size",
    type=click.Choice(["letter", "legal", "a4", "a5"]),
    default="letter",
    help="Page size",
)
@click.option(
    "--margins",
    type=click.Choice(["normal", "narrow", "moderate", "wide"]),
    default="normal",
    help="Page margins",
)
@click.option("--header", help="Header text")
@click.option("--footer", help="Footer text")
@click.option(
    "--page-numbers/--no-page-numbers", default=True, help="Include page numbers in footer"
)
def create(
    output: str,
    title: Optional[str],
    subtitle: Optional[str],
    author: Optional[str],
    template: Optional[str],
    page_size: str,
    margins: str,
    header: Optional[str],
    footer: Optional[str],
    page_numbers: bool,
):
    """
    Create a new Word document.

    \b
    Examples:
        will create -o report.docx --title "My Report"
        will create -o letter.docx --template letter --title "Business Letter"
        will create -o doc.docx -t "Title" -a "Author" --page-size a4
    """
    try:
        # Check if template is a file path or built-in name
        template_path = None
        if template:
            if Path(template).exists():
                template_path = template
            elif template not in get_template_names():
                console.print(
                    f"[yellow]Warning: Template '{template}' not found, using default[/yellow]"
                )

        doc = WordDocument(template=template_path, title=title, author=author)

        # Apply page settings
        doc.set_page_size(preset=page_size)
        doc.set_margins(preset=margins)

        # Apply built-in template if specified
        if template and template in get_template_names():
            from will.templates import apply_template

            apply_template(doc, template)

        # Add title
        if title:
            doc.add_title(title, subtitle)
            doc.add_page_break()

        # Set header/footer
        if header:
            doc.set_header(header)

        doc.set_footer(footer or "", include_page_numbers=page_numbers)

        # Save
        doc.save(output)

        console.print(f"[green]Created document:[/green] {output}")

        # Show document info
        info = doc.get_info()
        table = Table(show_header=False, box=None)
        table.add_column("Property", style="dim")
        table.add_column("Value")
        table.add_row("Title", info["title"] or "(none)")
        table.add_row("Author", info["author"] or "(none)")
        table.add_row("Page Size", page_size)
        table.add_row("Margins", margins)
        console.print(table)

    except Exception as e:
        console.print(f"[red]Error creating document:[/red] {e}")
        sys.exit(1)


# =============================================================================
# GENERATE COMMAND
# =============================================================================


@main.command()
@click.argument("spec_file", type=click.Path(exists=True))
@click.option("--output", "-o", required=True, help="Output file path (.docx)")
@click.option("--template", "-t", help="Optional template file (.docx)")
@click.option("--var", "-V", multiple=True, help="Variable substitution (KEY=VALUE)")
def generate(
    spec_file: str,
    output: str,
    template: Optional[str],
    var: tuple,
):
    """
    Generate a Word document from a YAML or JSON specification.

    \b
    Examples:
        will generate report.yaml -o report.docx
        will generate spec.json -o doc.docx --template base.docx
        will generate spec.yaml -o doc.docx -V AUTHOR="John" -V DATE="2024"
    """
    try:
        spec_path = Path(spec_file)

        click.echo("Generating document...")

        # Load spec
        if spec_path.suffix.lower() in [".yaml", ".yml"]:
            import yaml

            with open(spec_path, encoding="utf-8") as f:
                spec = yaml.safe_load(f)
        else:
            with open(spec_path, encoding="utf-8") as f:
                spec = json.load(f)

        # Apply template override
        if template:
            spec["template"] = template

        # Create document from spec
        doc = WordDocument.from_spec(spec)

        # Apply variable substitutions
        if var:
            replacements = {}
            for v in var:
                if "=" in v:
                    key, value = v.split("=", 1)
                    replacements[key] = value
            if replacements:
                doc.replace_placeholders(replacements)

        # Save
        doc.save(output)

        click.echo(click.style(f"Generated document: {output}", fg="green"))

        # Show summary
        info = doc.get_info()
        click.echo(f"  Paragraphs: {info['paragraphs']}")
        click.echo(f"  Tables: {info['tables']}")
        click.echo(f"  Word count: {info['word_count']}")

    except Exception as e:
        click.echo(click.style(f"Error generating document: {e}", fg="red"), err=True)
        sys.exit(1)


# =============================================================================
# INSPECT COMMAND
# =============================================================================


@main.command()
@click.argument("document", type=click.Path(exists=True))
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
@click.option("--placeholders", "-p", is_flag=True, help="Show only placeholders")
@click.option("--styles", "-s", is_flag=True, help="Show available styles")
def inspect(
    document: str,
    as_json: bool,
    placeholders: bool,
    styles: bool,
):
    """
    Inspect a Word document or template.

    \b
    Examples:
        will inspect template.docx
        will inspect report.docx --json
        will inspect template.docx --placeholders
    """
    try:
        doc = WordDocument(template=document)
        info = doc.get_info()

        if as_json:
            console.print_json(data=info)
            return

        if placeholders:
            if info["placeholders"]:
                console.print("[bold]Placeholders found:[/bold]")
                for p in info["placeholders"]:
                    console.print(f"  {{{{[cyan]{p}[/cyan]}}}}")
            else:
                console.print("[dim]No placeholders found[/dim]")
            return

        if styles:
            console.print("[bold]Available styles:[/bold]")
            for style in info["styles"]:
                console.print(f"  {style}")
            return

        # Full inspection
        console.print(Panel(f"[bold]Document: {document}[/bold]"))

        table = Table(show_header=True, header_style="bold")
        table.add_column("Property")
        table.add_column("Value")

        table.add_row("Title", info["title"] or "(none)")
        table.add_row("Author", info["author"] or "(none)")
        table.add_row("Created", info["created"] or "(unknown)")
        table.add_row("Modified", info["modified"] or "(unknown)")
        table.add_row("Paragraphs", str(info["paragraphs"]))
        table.add_row("Tables", str(info["tables"]))
        table.add_row("Sections", str(info["sections"]))
        table.add_row("Word Count", str(info["word_count"]))

        console.print(table)

        if info["placeholders"]:
            console.print("\n[bold]Placeholders:[/bold]")
            for p in info["placeholders"]:
                console.print(f"  {{{{[cyan]{p}[/cyan]}}}}")

    except Exception as e:
        console.print(f"[red]Error inspecting document:[/red] {e}")
        sys.exit(1)


# =============================================================================
# NEW COMMAND (Interactive)
# =============================================================================


@main.command()
@click.option("--output", "-o", required=True, help="Output file path (.docx)")
@click.option("--template", "-t", help="Template to use")
def new(output: str, template: Optional[str]):
    """
    Interactively create a new document.

    \b
    Examples:
        will new -o document.docx
        will new -o report.docx --template report
    """
    try:
        console.print("[bold]Create New Document[/bold]\n")

        # Get title
        title = click.prompt("Document title", default="Untitled Document")

        # Get subtitle
        subtitle = click.prompt("Subtitle (optional)", default="", show_default=False)
        subtitle = subtitle if subtitle else None

        # Get author
        author = click.prompt("Author", default="")
        author = author if author else None

        # Choose template if not specified
        if not template:
            console.print("\n[bold]Available templates:[/bold]")
            templates = list_templates()
            for i, t in enumerate(templates, 1):
                console.print(f"  {i}. {t['name']} - {t['description']}")

            choice = click.prompt(
                "\nSelect template (number or name)", default="default", show_default=True
            )

            try:
                idx = int(choice) - 1
                if 0 <= idx < len(templates):
                    template = templates[idx]["name"]
            except ValueError:
                template = choice

        # Create document
        builder = create_document(title=title, subtitle=subtitle, author=author)

        # Apply template settings
        if template:
            builder.with_template(template)

        # Interactive content addition
        console.print("\n[bold]Add content (type 'done' to finish):[/bold]")

        while True:
            content_type = click.prompt(
                "\nContent type",
                type=click.Choice(["heading", "paragraph", "bullets", "table", "done"]),
                default="done",
            )

            if content_type == "done":
                break

            if content_type == "heading":
                text = click.prompt("Heading text")
                level = click.prompt("Level (1-5)", type=int, default=1)
                builder.add_heading(text, level=level)

            elif content_type == "paragraph":
                text = click.prompt("Paragraph text")
                builder.add_paragraph(text)

            elif content_type == "bullets":
                console.print("Enter bullet points (empty line to finish):")
                items = []
                while True:
                    item = click.prompt("  -", default="", show_default=False)
                    if not item:
                        break
                    items.append(item)
                if items:
                    builder.add_bullets(items)

            elif content_type == "table":
                cols = click.prompt("Number of columns", type=int, default=2)
                headers = []
                console.print("Enter column headers:")
                for i in range(cols):
                    h = click.prompt(f"  Column {i+1}")
                    headers.append(h)

                rows = click.prompt("Number of rows", type=int, default=2)
                data = []
                console.print("Enter table data:")
                for r in range(rows):
                    row = []
                    for c in range(cols):
                        cell = click.prompt(f"  Row {r+1}, Col {c+1}")
                        row.append(cell)
                    data.append(row)

                builder.add_table(data, headers=headers)

        # Save
        builder.save(output)
        console.print(f"\n[green]Created document:[/green] {output}")

    except click.Abort:
        console.print("\n[yellow]Cancelled[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


# =============================================================================
# ADD COMMAND
# =============================================================================


@main.command()
@click.argument("document", type=click.Path(exists=True))
@click.option("--output", "-o", help="Output file (defaults to overwrite input)")
@click.option("--heading", "-h", help="Add a heading")
@click.option("--level", "-l", type=int, default=1, help="Heading level (1-5)")
@click.option("--paragraph", "-p", help="Add a paragraph")
@click.option("--bullets", "-b", multiple=True, help="Add bullet points")
@click.option("--page-break", is_flag=True, help="Add a page break")
@click.option("--image", "-i", type=click.Path(exists=True), help="Add an image")
@click.option("--caption", help="Image caption")
def add(
    document: str,
    output: Optional[str],
    heading: Optional[str],
    level: int,
    paragraph: Optional[str],
    bullets: tuple,
    page_break: bool,
    image: Optional[str],
    caption: Optional[str],
):
    """
    Add content to an existing document.

    \b
    Examples:
        will add report.docx --heading "New Section" --level 1
        will add report.docx --paragraph "Additional text here."
        will add report.docx -b "Point 1" -b "Point 2" -b "Point 3"
        will add report.docx --image chart.png --caption "Figure 1"
    """
    try:
        doc = WordDocument(template=document)
        output_path = output or document

        if page_break:
            doc.add_page_break()

        if heading:
            doc.add_heading(heading, level=level)

        if paragraph:
            doc.add_paragraph(paragraph)

        if bullets:
            doc.add_bullets(list(bullets))

        if image:
            doc.add_image(image, caption=caption)

        doc.save(output_path)
        console.print(f"[green]Updated document:[/green] {output_path}")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


# =============================================================================
# REPLACE COMMAND
# =============================================================================


@main.command()
@click.argument("document", type=click.Path(exists=True))
@click.argument("replacements", nargs=-1)
@click.option("--output", "-o", help="Output file (defaults to overwrite input)")
@click.option("--list", "-l", "list_only", is_flag=True, help="List placeholders only")
def replace(
    document: str,
    replacements: tuple,
    output: Optional[str],
    list_only: bool,
):
    """
    Replace {{PLACEHOLDERS}} in a document.

    \b
    Examples:
        will replace template.docx NAME="John Doe" DATE="2024-01-15"
        will replace template.docx --list
        will replace template.docx COMPANY="Acme Corp" -o output.docx
    """
    try:
        doc = WordDocument(template=document)

        if list_only:
            placeholders = doc.get_placeholders()
            if placeholders:
                console.print("[bold]Placeholders found:[/bold]")
                for p in placeholders:
                    console.print(f"  {{{{[cyan]{p}[/cyan]}}}}")
            else:
                console.print("[dim]No placeholders found[/dim]")
            return

        if not replacements:
            console.print("[yellow]No replacements specified. Use KEY=VALUE format.[/yellow]")
            console.print("Use --list to see available placeholders.")
            return

        # Parse replacements
        repl_dict = {}
        for r in replacements:
            if "=" in r:
                key, value = r.split("=", 1)
                repl_dict[key] = value
            else:
                console.print(f"[yellow]Skipping invalid format: {r} (use KEY=VALUE)[/yellow]")

        if repl_dict:
            count = doc.replace_placeholders(repl_dict)
            output_path = output or document
            doc.save(output_path)
            console.print(f"[green]Replaced {count} placeholder(s) in:[/green] {output_path}")
        else:
            console.print("[yellow]No valid replacements to make[/yellow]")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


# =============================================================================
# TEMPLATE COMMAND GROUP
# =============================================================================


@main.group()
def template():
    """
    Manage document templates.

    \b
    Commands:
        list     List available templates
        info     Show template details
        init     Create a YAML spec from a template
    """
    pass


@template.command("list")
@click.option("--yaml", "yaml_templates", is_flag=True, help="List YAML templates instead")
def template_list(yaml_templates: bool):
    """List available templates."""
    if yaml_templates:
        console.print("[bold]Available YAML Templates:[/bold]\n")
        for name in list_yaml_templates():
            console.print(f"  [cyan]{name}[/cyan]")
    else:
        console.print("[bold]Available Document Templates:[/bold]\n")
        table = Table(show_header=True, header_style="bold")
        table.add_column("Name")
        table.add_column("Description")
        table.add_column("Page Size")

        for t in list_templates():
            table.add_row(t["name"], t["description"], t["page_size"])

        console.print(table)


@template.command("info")
@click.argument("name")
def template_info(name: str):
    """Show details about a template."""
    t = get_template(name)
    if not t:
        console.print(f"[red]Template not found:[/red] {name}")
        sys.exit(1)

    console.print(Panel(f"[bold]Template: {t.name}[/bold]"))

    table = Table(show_header=False, box=None)
    table.add_column("Property", style="dim")
    table.add_column("Value")

    table.add_row("Description", t.description)
    table.add_row("Page Size", t.page_size)
    table.add_row("Orientation", t.orientation)
    table.add_row("Margins", t.margins)
    table.add_row("Body Font", t.font_body)
    table.add_row("Heading Font", t.font_heading)
    table.add_row("Primary Color", f"#{t.primary_color}")
    table.add_row("Include Header", str(t.include_header))
    table.add_row("Include Footer", str(t.include_footer))
    table.add_row("Page Numbers", str(t.include_page_numbers))

    console.print(table)


@template.command("init")
@click.argument("name")
@click.option("--output", "-o", required=True, help="Output YAML file path")
def template_init(name: str, output: str):
    """Create a YAML spec file from a template."""
    yaml_content = get_yaml_template(name)
    if not yaml_content:
        console.print(f"[red]YAML template not found:[/red] {name}")
        console.print("\nAvailable templates:")
        for t in list_yaml_templates():
            console.print(f"  {t}")
        sys.exit(1)

    save_yaml_template(name, output)
    console.print(f"[green]Created YAML spec:[/green] {output}")
    console.print("\nEdit this file and run:")
    console.print(f"  will generate {output} -o document.docx")


# =============================================================================
# CLOUD COMMAND GROUP
# =============================================================================


@main.group()
def cloud():
    """
    Cloud API commands for remote document generation.

    \b
    Commands:
        health     Check API health
        generate   Generate document via cloud API
        inspect    Inspect template via cloud API
    """
    pass


@cloud.command("health")
@click.option("--url", "-u", default="http://localhost:8000", help="API base URL")
def cloud_health(url: str):
    """Check cloud API health status."""
    try:
        import httpx

        with httpx.Client() as client:
            response = client.get(f"{url}/health", timeout=10)
            response.raise_for_status()
            data = response.json()

        console.print("[green]API is healthy[/green]")
        table = Table(show_header=False, box=None)
        for key, value in data.items():
            table.add_row(key, str(value))
        console.print(table)

    except Exception as e:
        console.print(f"[red]API health check failed:[/red] {e}")
        sys.exit(1)


@cloud.command("generate")
@click.argument("spec_file", type=click.Path(exists=True))
@click.option("--output", "-o", required=True, help="Output file path")
@click.option("--url", "-u", default="http://localhost:8000", help="API base URL")
@click.option("--template", "-t", type=click.Path(exists=True), help="Template file")
def cloud_generate(
    spec_file: str,
    output: str,
    url: str,
    template: Optional[str],
):
    """Generate document via cloud API."""
    try:
        import httpx
        import yaml

        # Load spec
        spec_path = Path(spec_file)
        if spec_path.suffix.lower() in [".yaml", ".yml"]:
            with open(spec_path, encoding="utf-8") as f:
                spec = yaml.safe_load(f)
        else:
            with open(spec_path, encoding="utf-8") as f:
                spec = json.load(f)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Generating via cloud API...", total=None)

            with httpx.Client() as client:
                if template:
                    # Use multipart form data with template
                    with open(template, "rb") as f:
                        files = {"template": f}
                        data = {"spec": json.dumps(spec)}
                        response = client.post(
                            f"{url}/generate-with-template",
                            files=files,
                            data=data,
                            timeout=60,
                        )
                else:
                    # JSON only
                    response = client.post(
                        f"{url}/generate",
                        json=spec,
                        timeout=60,
                    )

                response.raise_for_status()

            # Save response
            with open(output, "wb") as f:
                f.write(response.content)

            progress.update(task, completed=True)

        console.print(f"[green]Generated document:[/green] {output}")

    except Exception as e:
        console.print(f"[red]Cloud generation failed:[/red] {e}")
        sys.exit(1)


@cloud.command("inspect")
@click.argument("template", type=click.Path(exists=True))
@click.option("--url", "-u", default="http://localhost:8000", help="API base URL")
def cloud_inspect(template: str, url: str):
    """Inspect template via cloud API."""
    try:
        import httpx

        with httpx.Client() as client:
            with open(template, "rb") as f:
                files = {"template": f}
                response = client.post(
                    f"{url}/inspect",
                    files=files,
                    timeout=30,
                )
            response.raise_for_status()
            data = response.json()

        console.print(Panel(f"[bold]Template: {template}[/bold]"))
        console.print_json(data=data)

    except Exception as e:
        console.print(f"[red]Cloud inspection failed:[/red] {e}")
        sys.exit(1)


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()
