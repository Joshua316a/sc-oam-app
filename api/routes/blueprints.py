"""Blueprint API endpoints."""

from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel, Field

router = APIRouter(prefix="/blueprints", tags=["blueprints"])


# Pydantic models
class BlueprintBase(BaseModel):
    """Base fields shared by create, update, and response."""

    blueprint_id: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="User-facing blueprint identifier (e.g., 'bp_001')",
    )
    bp_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Human-readable blueprint name",
    )
    category: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Item category (e.g., 'weapons', 'modules', 'cargo')",
    )
    subcategory: str = Field(
        default="uncategorized",
        max_length=50,
        description="Sub-category (e.g., 'missiles', 'lasers', 'mining')",
    )
    craft_type: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Type of crafting (e.g., 'missile', 'module', 'ore')",
    )
    output_item_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Item produced by crafting (e.g., 'missile')",
    )
    quality_min: float = Field(
        ...,
        ge=0,
        le=1000,
        description="Minimum quality range (0-1000); default 0 in DB",
    )
    quality_max: float = Field(
        ...,
        ge=0,
        le=1000,
        description="Maximum quality range (0-1000); default 1000 in DB",
    )
    craft_time_seconds: float = Field(
        ...,
        ge=0,
        description="Crafting duration in seconds; default 0 in DB",
    )
    ilg_label: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="ILG category label (e.g., 'Weapons/Missiles')",
    )

    model_config = {"from_attributes": True}  # ORM mode


class BlueprintCreate(BlueprintBase):
    """Fields required for CREATE operation."""

    owner_handle: Optional[str] = Field(
        default="",
        max_length=50,
        description="Owner's org handle (e.g., 'oam_corp')",
    )
    acquired_date: Optional[str] = Field(
        default="",
        max_length=20,
        description="ISO date string 'YYYY-MM-DD'; e.g. '2026-01-15'",
    )
    is_learned: bool = Field(
        default=False,
        description="Whether the player has learned this blueprint",
    )
    notes: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Free-form notes about this blueprint",
    )


class BlueprintUpdate(BaseModel):
    """Fields for UPDATE operation — all optional."""

    bp_name: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Update blueprint name (partial update)",
    )
    quality_min: Optional[float] = Field(
        default=None,
        ge=0,
        le=1000,
        description="Update quality_min; ge=0, le=1000 if provided",
    )
    quality_max: Optional[float] = Field(
        default=None,
        ge=0,
        le=1000,
        description="Update quality_max; ge=0, le=1000 if provided",
    )
    notes: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Update free-form notes",
    )
    is_learned: Optional[bool] = Field(
        default=None,
        description="Toggle learned status",
    )


class BlueprintResponse(BlueprintBase):
    """Full response including database-generated fields."""

    id: int

    model_config = {"from_attributes": True}  # enables ORM → Pydantic conversion


# In-memory "database" (replace with real DB later)
_blueprints_db: dict = {}
_blueprint_counter: int = 0


@router.get("/", response_model=list[BlueprintResponse])
async def list_blueprints():
    """List all blueprints."""
    return list(_blueprints_db.values())


@router.post("/", response_model=BlueprintResponse, status_code=201)
async def create_blueprint(blueprint: BlueprintCreate):
    """Create a new blueprint."""
    global _blueprint_counter
    
    # Check for duplicate blueprint_id
    for existing in _blueprints_db.values():
        if existing.blueprint_id == blueprint.blueprint_id:
            raise HTTPException(
                status_code=400,
                detail=f"Blueprint with id '{blueprint.blueprint_id}' already exists",
            )
    
    _blueprint_counter += 1
    bp_dict = BlueprintResponse(
        id=_blueprint_counter,
        **blueprint.model_dump(),
    ).model_dump()
    _blueprints_db[_blueprint_counter] = BlueprintResponse(**bp_dict)
    return _blueprints_db[_blueprint_counter]


@router.get("/{blueprint_id}", response_model=BlueprintResponse)
async def get_blueprint(blueprint_id: int):
    """Get a specific blueprint by ID."""
    if blueprint_id not in _blueprints_db:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    return _blueprints_db[blueprint_id]


@router.put("/{blueprint_id}", response_model=BlueprintResponse)
async def update_blueprint(blueprint_id: int, blueprint: BlueprintUpdate):
    """Update a blueprint."""
    if blueprint_id not in _blueprints_db:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    updated = _blueprints_db[blueprint_id].model_copy(update=blueprint.model_dump(exclude_unset=True))
    _blueprints_db[blueprint_id] = updated
    return updated


@router.delete("/{blueprint_id}", status_code=204)
async def delete_blueprint(blueprint_id: int):
    """Delete a blueprint."""
    if blueprint_id not in _blueprints_db:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    del _blueprints_db[blueprint_id]