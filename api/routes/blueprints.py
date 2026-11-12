"""Blueprint API endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/blueprints", tags=["blueprints"])

# Pydantic models
class BlueprintBase(BaseModel):
    blueprint_id: str
    bp_name: str
    category: str
    subcategory: str
    craft_type: str
    output_item_name: str
    quality_min: float
    quality_max: float
    craft_time_seconds: float = 0.0
    ilg_label: str

class BlueprintCreate(BlueprintBase):
    owner_handle: str = ""
    acquired_date: str = ""
    is_learned: bool = False
    notes: str = ""

class BlueprintUpdate(BlueprintBase):
    pass

class BlueprintResponse(BlueprintBase):
    id: int

    class Config:
        from_attributes = True

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
