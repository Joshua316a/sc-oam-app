"""sc-oam-app — FastAPI application for OAM API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Version from single source of truth: _version.py
from _version import __version__

# Create app instance
app = FastAPI(
    title="sc-oam-app",
    version=__version__,
    description="Org Asset Manager API — headless engine for crafting, blueprints, warehouse & hangar management, replacing Tkinter UI with RESTful endpoints",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🎨 Branding: Health check endpoint
# Returns app name, version, and status for CI/CD and monitoring integrations
@app.get("/health", tags=["root"])
async def health_check():
    """Health check endpoint with branding information."""
    return {
        "status": "ok",
        "service": "sc-oam-app",
        "version": __version__,
        "name": "sc-oam-app",
    }

# API routes will be included from api.routes
from api.routes.blueprints import router
app.include_router(router, prefix="/api")

from api.routes.extraction import router as extraction_router
app.include_router(extraction_router, prefix="/api")

# ── Module imports (lazy) ─────────────────────────────────────────────
# These are imported on-demand to avoid blocking startup
# from modules.data_access import query_records, catalogue_family
# from modules.oam_categories import OAM_ITEM_CATEGORIES
# from modules.catalogue_builder import read_catalogue, build_blueprint_catalogue
# from modules.blueprint_pool import import_blueprint_pools
# from modules.log_analytics import GameLogStore
# from modules.dc_missions_mixin import resolve_bp_display_name

# ── API routes ─────────────────────────────────────────────────────────
from api.routes.auth import router as auth_router
app.include_router(auth_router, prefix="/api", tags=["auth"])

print("✓ sc-oam-app FastAPI instance created")
