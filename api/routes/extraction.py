"""Extraction API Endpoints for sc-oam-app.

Handles the Data.p4k extraction pipeline that creates reference databases
from the original Tkinter OAM game data. Provides both synchronous and
background extraction options.
"""

from fastapi import APIRouter, Body, HTTPException, BackgroundTasks
from pydantic import BaseModel
from pathlib import Path
from typing import Dict, Any

from api.services.extraction import run_extraction_pipeline, main_cli
from api.services.rsi_auth import create_rsi_auth_manager

router = APIRouter(prefix="/extraction", tags=["extraction"])


# ─── Request Models ──────────────────────────────────────────────────────

class ExtractionRun(BaseModel):
    """Request body for running the extraction pipeline."""
    input_folder: Path = Body(
        ...,
        description="Folder containing .p4k files to extract",
        json_schema_extra={"example": "./legacy_data/p4k"},
    )
    output_db: Path = Body(
        ...,
        description="Base path for output databases (e.g., ./database)",
        json_schema_extra={"example": "./database"},
    )
    overwrite: bool = Body(
        False,
        description="Whether to overwrite existing databases",
        json_schema_extra={"example": False},
    )


class ExtractionStatus(BaseModel):
    """Status of an extraction operation."""
    status: str
    message: str
    p4k_files_scanned: int = 0
    records_extracted: Dict[str, int] = {}
    databases_created: Dict[str, str] = {}


# ─── Extraction Endpoints ──────────────────────────────────────────────

@router.post(
    "/run",
    summary="Run Data.p4k extraction pipeline",
    description="""
    Run the extraction pipeline to parse .p4k archive files from the original
    Tkinter OAM and create reference SQLite databases.
    
    This is the migration path from the old OAM application. The extracted
    databases can then be used by the sc-oam-app API.
    
    The operation runs synchronously and returns results immediately.
    """,
    response_model=ExtractionStatus,
)
async def run_extraction(
    payload: ExtractionRun,
    background_tasks: BackgroundTasks,
) -> ExtractionStatus:
    """Run the extraction pipeline synchronously.
    
    Args:
        payload: Contains input_folder, output_db, and overwrite flag
        background_tasks: FastAPI background tasks (included for future async support)
    
    Returns:
        ExtractionStatus with results of the extraction pipeline
    """
    # Run the pipeline synchronously (no background tasks needed for synchronous version)
    result = run_extraction_pipeline(
        input_folder=payload.input_folder,
        output_db_path=payload.output_db,
        overwrite=payload.overwrite,
    )
    
    return ExtractionStatus(
        status=result["status"],
        message=result.get("message", ""),
        p4k_files_scanned=result.get("p4k_files_scanned", 0),
        records_extracted=result.get("records_extracted", {}),
        databases_created=result.get("databases_created", {}),
    )


@router.post(
    "/trigger",
    summary="Trigger extraction pipeline (background)",
    description="""
    Trigger the extraction pipeline in the background.
    
    This endpoint returns immediately and the extraction runs as a background task.
    Useful for UI flows where the user wants to continue working while
    the extraction completes.
    
    Note: For full implementation, integrate with a task queue like Celery.
    Currently runs synchronously for simplicity.
    """,
    response_model=ExtractionStatus,
)
async def trigger_extraction(
    payload: ExtractionRun,
    background_tasks: BackgroundTasks,
) -> ExtractionStatus:
    """Trigger extraction in background (currently synchronous for simplicity)."""
    # For now, run synchronously; in production, offload to Celery/Redis
    result = run_extraction_pipeline(
        input_folder=payload.input_folder,
        output_db_path=payload.output_db,
        overwrite=payload.overwrite,
    )
    
    return ExtractionStatus(
        status=result["status"],
        message=result.get("message", ""),
        p4k_files_scanned=result.get("p4k_files_scanned", 0),
        records_extracted=result.get("records_extracted", {}),
        databases_created=result.get("databases_created", {}),
    )


@router.get(
    "/status/{task_id}",
    summary="Check extraction task status",
    description="""
    Check the status of a background extraction task.
    
    Currently a placeholder; in production with Celery/Redis this would query
    the task queue for progress. Currently always returns 'completed' if
    the associated extraction run endpoint was called.
    """,
    response_model=Dict[str, str],
)
async def check_extraction_status(
    task_id: str,
) -> Dict[str, str]:
    """Placeholder for background task status checking."""
    return {
        "status": "completed",
        "message": "Extraction task completed (synchronous mode)",
    }


@router.get(
    "/health",
    summary="Extraction service health check",
    description="Verify the extraction service is operational.",
)
async def extraction_health() -> Dict[str, str]:
    """Health check for the extraction service."""
    return {
        "status": "healthy",
        "service": "extraction-pipeline",
        "message": "Extraction pipeline API operational",
    }


# ─── Legacy CLI Integration ────────────────────────────────────────────

@router.post(
    "/cli",
    summary="Run extraction via CLI (legacy)",
    description="""
    Run the extraction pipeline via CLI arguments (legacy/compatibility endpoint).
    
    Provides backwards compatibility for the original Tkinter OAM extraction
    workflow. For new usage, prefer /api/extraction/run.
    """,
    response_model=ExtractionStatus,
)
async def run_extraction_cli(
    input_folder: Path = Body(..., description="Folder containing .p4k files"),
    output_db: Path = Body(..., description="Base path for output databases"),
    overwrite: bool = Body(False, description="Overwrite existing databases"),
) -> ExtractionStatus:
    """Run extraction via CLI-style arguments through the API."""
    result = run_extraction_pipeline(
        input_folder=input_folder,
        output_db_path=output_db,
        overwrite=overwrite,
    )
    
    return ExtractionStatus(
        status=result["status"],
        message=result.get("message", ""),
        p4k_files_scanned=result.get("p4k_files_scanned", 0),
        records_extracted=result.get("records_extracted", {}),
        databases_created=result.get("databases_created", {}),
    )