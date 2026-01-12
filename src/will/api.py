"""
Schopenhauer REST API - FastAPI server for document generation.

This module provides a RESTful API for generating Word documents,
suitable for cloud deployment on GCP Cloud Run or similar platforms.

Usage:
    uvicorn will.api:app --host 0.0.0.0 --port 8000

Endpoints:
    GET  /health              - Health check
    GET  /templates           - List available templates
    POST /generate            - Generate document from JSON spec
    POST /generate-with-template - Generate with uploaded template
    POST /inspect             - Inspect uploaded template
    POST /batch/generate      - Batch generate multiple documents
"""

from datetime import datetime
from io import BytesIO
from typing import Any, Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field

from will import __version__
from will.core import WordDocument
from will.templates import list_templates, list_yaml_templates

# =============================================================================
# API MODELS
# =============================================================================

class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    version: str = __version__
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class TemplateInfo(BaseModel):
    """Template information."""
    name: str
    description: str
    page_size: str


class TemplatesResponse(BaseModel):
    """List of templates response."""
    templates: list[TemplateInfo]
    yaml_templates: list[str]


class SectionSpec(BaseModel):
    """Document section specification."""
    type: str = "content"
    title: Optional[str] = None
    subtitle: Optional[str] = None
    text: Optional[str] = None
    level: int = 2
    bullets: Optional[list[str]] = None
    numbered: Optional[list[str]] = None
    headers: Optional[list[str]] = None
    data: Optional[list[list[Any]]] = None
    column_widths: Optional[list[float]] = None
    image: Optional[str] = None
    path: Optional[str] = None
    width: Optional[float] = None
    height: Optional[float] = None
    caption: Optional[str] = None
    code: Optional[str] = None
    language: Optional[str] = None
    author: Optional[str] = None
    page_break: bool = False


class DocumentSpec(BaseModel):
    """Document specification for generation."""
    title: Optional[str] = None
    subtitle: Optional[str] = None
    author: Optional[str] = None
    template: Optional[str] = None
    page_size: str = "letter"
    margins: str = "normal"
    header: Optional[str] = None
    footer: Optional[str] = None
    table_of_contents: bool = False
    title_page_break: bool = True
    sections: list[SectionSpec] = Field(default_factory=list)
    placeholders: Optional[dict[str, str]] = None


class DocumentInfo(BaseModel):
    """Document information response."""
    title: str
    author: str
    created: str
    modified: str
    paragraphs: int
    tables: int
    sections: int
    word_count: int
    styles: list[str]
    placeholders: list[str]


class BatchItem(BaseModel):
    """Single item in a batch generation request."""
    spec: DocumentSpec
    filename: str


class BatchRequest(BaseModel):
    """Batch generation request."""
    items: list[BatchItem]


class ErrorResponse(BaseModel):
    """Error response."""
    error: str
    detail: Optional[str] = None


# =============================================================================
# API APPLICATION
# =============================================================================

app = FastAPI(
    title="Schopenhauer's Will API",
    description="A powerful REST API for generating Word documents from specifications.",
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# HEALTH ENDPOINT
# =============================================================================

@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Health check endpoint",
)
async def health():
    """
    Check API health status.

    Returns basic health information including version and timestamp.
    """
    return HealthResponse()


@app.get(
    "/",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Root endpoint",
)
async def root():
    """Root endpoint - returns health status."""
    return HealthResponse()


# =============================================================================
# TEMPLATE ENDPOINTS
# =============================================================================

@app.get(
    "/templates",
    response_model=TemplatesResponse,
    tags=["Templates"],
    summary="List available templates",
)
async def get_templates():
    """
    List all available document templates.

    Returns both document templates and YAML specification templates.
    """
    templates = [
        TemplateInfo(**t) for t in list_templates()
    ]
    yaml_templates = list_yaml_templates()

    return TemplatesResponse(
        templates=templates,
        yaml_templates=yaml_templates,
    )


@app.get(
    "/templates/{name}",
    response_model=TemplateInfo,
    tags=["Templates"],
    summary="Get template details",
)
async def get_template_info(name: str):
    """Get detailed information about a specific template."""
    from will.templates import get_template

    template = get_template(name)
    if not template:
        raise HTTPException(status_code=404, detail=f"Template not found: {name}")

    return TemplateInfo(
        name=template.name,
        description=template.description,
        page_size=template.page_size,
    )


# =============================================================================
# GENERATION ENDPOINTS
# =============================================================================

@app.post(
    "/generate",
    tags=["Generation"],
    summary="Generate document from specification",
    responses={
        200: {
            "content": {"application/vnd.openxmlformats-officedocument.wordprocessingml.document": {}},
            "description": "Generated Word document",
        },
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def generate_document(spec: DocumentSpec):
    """
    Generate a Word document from a JSON specification.

    The response is the binary content of the generated .docx file.
    """
    try:
        # Convert Pydantic model to dict
        spec_dict = spec.model_dump(exclude_none=True)

        # Convert sections
        if "sections" in spec_dict:
            spec_dict["sections"] = [
                {k: v for k, v in s.items() if v is not None}
                for s in spec_dict["sections"]
            ]

        # Create document
        doc = WordDocument.from_spec(spec_dict)

        # Apply placeholder replacements
        if spec.placeholders:
            doc.replace_placeholders(spec.placeholders)

        # Generate bytes
        doc_bytes = doc.to_bytes()

        # Return as streaming response
        filename = f"{spec.title or 'document'}.docx".replace(" ", "_")
        return StreamingResponse(
            BytesIO(doc_bytes),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post(
    "/generate-with-template",
    tags=["Generation"],
    summary="Generate document with uploaded template",
    responses={
        200: {
            "content": {"application/vnd.openxmlformats-officedocument.wordprocessingml.document": {}},
            "description": "Generated Word document",
        },
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def generate_with_template(
    template: UploadFile = File(...),
    spec: str = Form(...),
):
    """
    Generate a Word document using an uploaded template file.

    The template is a .docx file that provides base styling and placeholders.
    The spec is a JSON string with the document specification.
    """
    import json
    import os
    import tempfile

    try:
        # Parse spec JSON
        spec_dict = json.loads(spec)

        # Save template to temp file
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
            tmp.write(await template.read())
            tmp_path = tmp.name

        try:
            # Create document from template
            spec_dict["template"] = tmp_path
            doc = WordDocument.from_spec(spec_dict)

            # Apply placeholder replacements
            if "placeholders" in spec_dict:
                doc.replace_placeholders(spec_dict["placeholders"])

            # Generate bytes
            doc_bytes = doc.to_bytes()

        finally:
            # Clean up temp file
            os.unlink(tmp_path)

        # Return as streaming response
        filename = f"{spec_dict.get('title', 'document')}.docx".replace(" ", "_")
        return StreamingResponse(
            BytesIO(doc_bytes),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
            },
        )

    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON in spec: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# INSPECTION ENDPOINTS
# =============================================================================

@app.post(
    "/inspect",
    response_model=DocumentInfo,
    tags=["Inspection"],
    summary="Inspect uploaded document or template",
)
async def inspect_document(
    template: UploadFile = File(...),
):
    """
    Inspect an uploaded Word document or template.

    Returns information about the document including placeholders,
    styles, and statistics.
    """
    import os
    import tempfile

    try:
        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
            tmp.write(await template.read())
            tmp_path = tmp.name

        try:
            doc = WordDocument(template=tmp_path)
            info = doc.get_info()

        finally:
            os.unlink(tmp_path)

        return DocumentInfo(**info)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# BATCH ENDPOINTS
# =============================================================================

@app.post(
    "/batch/generate",
    tags=["Batch"],
    summary="Batch generate multiple documents",
    responses={
        200: {
            "content": {"application/zip": {}},
            "description": "ZIP archive containing generated documents",
        },
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def batch_generate(request: BatchRequest):
    """
    Generate multiple documents in a single request.

    Returns a ZIP archive containing all generated documents.
    """
    import zipfile

    try:
        # Create ZIP in memory
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for item in request.items:
                # Convert spec to dict
                spec_dict = item.spec.model_dump(exclude_none=True)

                # Convert sections
                if "sections" in spec_dict:
                    spec_dict["sections"] = [
                        {k: v for k, v in s.items() if v is not None}
                        for s in spec_dict["sections"]
                    ]

                # Create document
                doc = WordDocument.from_spec(spec_dict)

                # Apply placeholders
                if item.spec.placeholders:
                    doc.replace_placeholders(item.spec.placeholders)

                # Add to ZIP
                doc_bytes = doc.to_bytes()
                filename = item.filename
                if not filename.endswith('.docx'):
                    filename += '.docx'
                zip_file.writestr(filename, doc_bytes)

        zip_buffer.seek(0)

        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={
                "Content-Disposition": 'attachment; filename="documents.zip"',
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# PLACEHOLDER ENDPOINTS
# =============================================================================

@app.post(
    "/replace",
    tags=["Utilities"],
    summary="Replace placeholders in uploaded document",
    responses={
        200: {
            "content": {"application/vnd.openxmlformats-officedocument.wordprocessingml.document": {}},
            "description": "Document with replaced placeholders",
        },
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def replace_placeholders(
    document: UploadFile = File(...),
    replacements: str = Form(...),
):
    """
    Replace {{PLACEHOLDERS}} in an uploaded document.

    The replacements parameter should be a JSON object mapping
    placeholder names to values.
    """
    import json
    import os
    import tempfile

    try:
        # Parse replacements
        repl_dict = json.loads(replacements)

        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
            tmp.write(await document.read())
            tmp_path = tmp.name

        try:
            doc = WordDocument(template=tmp_path)
            count = doc.replace_placeholders(repl_dict)
            doc_bytes = doc.to_bytes()

        finally:
            os.unlink(tmp_path)

        return StreamingResponse(
            BytesIO(doc_bytes),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition": 'attachment; filename="document.docx"',
                "X-Replacements-Made": str(count),
            },
        )

    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle unexpected exceptions."""
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)},
    )


# =============================================================================
# STARTUP/SHUTDOWN
# =============================================================================

@app.on_event("startup")
async def startup_event():
    """Application startup handler."""
    print(f"Schopenhauer's Will API v{__version__} starting...")
    print("Documentation available at /docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown handler."""
    print("Shutting down...")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
