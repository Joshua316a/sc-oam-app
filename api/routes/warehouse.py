"""Warehouse inventory endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional


router = APIRouter(prefix="/warehouse", tags=["warehouse"])


# In-memory store (replace with real DB later)
_warehouse_db: dict = {}
_warehouse_counter: int = 0


# Pydantic models
class WarehouseItemCreate(BaseModel):
    """Fields required for CREATE operation."""

    item_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the item",
    )
    category: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Item category",
    )
    quantity: int = Field(
        ...,
        ge=0,
        description="Current quantity in stack",
    )
    capacity: int = Field(
        ...,
        ge=0,
        description="Maximum stack capacity",
    )
    location: str = Field(
        default="Hangar",
        max_length=50,
        description="Storage location",
    )
    notes: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Free-form notes",
    )
    quality: Optional[int] = Field(
        default=None,
        description="Item quality (0-1000), default 500 for old-data compatibility"
    )


class WarehouseItemUpdate(BaseModel):
    """Fields for UPDATE operation — all optional."""

    quantity: Optional[int] = Field(
        default=None,
        ge=0,
        description="Update quantity",
    )
    location: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Update location",
    )
    notes: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Update notes",
    )


class WarehouseItem(BaseModel):
    """Full warehouse item response."""

    id: int
    item_name: str
    category: str
    quantity: int
    capacity: int
    location: str
    quality: Optional[int] = 500
    notes: Optional[str] = None
    last_updated: str = ""

    model_config = {"from_attributes": True}


# In-memory "database" (replace with real DB later)
_warehouse_db: dict = {}
_warehouse_counter: int = 0


def _item_to_dict(item) -> dict:
    """Convert various item types to dict."""
    if hasattr(item, 'item_name'):
        # SQLAlchemy model or ORM object
        return {
            "id": item.id,
            "item_name": item.item_name,
            "category": item.category,
            "quantity": item.quantity,
            "capacity": item.capacity,
            "location": item.location,
            "notes": getattr(item, 'notes', ''),
            "last_updated": getattr(item, 'last_updated', ''),
            "quality": getattr(item, 'quality', 500),
        }
    elif isinstance(item, dict):
        return item
    return {}


@router.get("/", response_model=list)
async def list_warehouse():
    """List all warehouse inventory items."""
    return [_item_to_dict(item) for item in _warehouse_db.values()]


@router.post("/", response_model=WarehouseItem, status_code=201)
async def add_warehouse_item(item_create: WarehouseItemCreate) -> WarehouseItem:
    """Add a new item to warehouse inventory."""
    global _warehouse_counter
    _warehouse_counter += 1

    item = WarehouseItem(
        id=_warehouse_counter,
        item_name=item_create.item_name,
        category=item_create.category,
        quantity=item_create.quantity,
        capacity=item_create.capacity,
        location=item_create.location,
        notes=item_create.notes,
        last_updated="",
    )
    _warehouse_db[_warehouse_counter] = item
    return item


@router.get("/{item_id}", response_model=WarehouseItem)
async def get_warehouse_item(item_id: int) -> WarehouseItem:
    """Get a specific warehouse item by ID."""
    if item_id not in _warehouse_db:
        raise HTTPException(status_code=404, detail="Warehouse item not found")
    return _warehouse_db[item_id]


@router.put("/{item_id}", response_model=WarehouseItem)
async def update_warehouse_item(
    item_id: int,
    item_update: WarehouseItemUpdate,
) -> WarehouseItem:
    """Update a warehouse item (partial update)."""
    if item_id not in _warehouse_db:
        raise HTTPException(status_code=404, detail="Warehouse item not found")

    item = _warehouse_db[item_id]
    update_data = item_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(item, field, value)

    return item


@router.delete("/{item_id}", status_code=204)
async def delete_warehouse_item(item_id: int) -> None:
    """Delete a warehouse item."""
    if item_id not in _warehouse_db:
        raise HTTPException(status_code=404, detail="Warehouse item not found")
    del _warehouse_db[item_id]