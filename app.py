"""sc-oam-app — FastAPI application for OAM API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create app instance
app = FastAPI(
    title="OAM API",
    description="Org Asset Manager API — headless engine for crafting, blueprints, warehouse & hangar management",
    version="0.1.0",
    description="API separation layer for Org Asset Manager, replacing Tkinter UI with RESTful endpoints",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health", tags=["root"])
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "OAM API", "version": "0.1.0"}

# API routes will be included from api.routes
# from api.routes import router
# app.include_router(router, prefix="/api")

# ── Module imports (lazy) ─────────────────────────────────────────────
# These are imported on-demand to avoid blocking startup
# from modules.data_access import query_records, catalogue_family
# from modules.oam_categories import OAM_ITEM_CATEGORIES
# from modules.catalogue_builder import read_catalogue, build_blueprint_catalogue
# from modules.blueprint_pool import import_blueprint_pools
# from modules.log_analytics import GameLogStore
# from modules.dc_missions_mixin import resolve_bp_display_name

print("✓ sc-oam-app FastAPI instance created")
