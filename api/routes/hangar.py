"""Hangar fleet endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional


router = APIRouter(prefix="/hangar", tags=["hangar"])


# In-memory store (replace with real DB later)
_hangar_db: dict = {}
_hangar_counter: int = 0


# Pydantic models
class VesselCreate(BaseModel):
    """Fields required for CREATE operation."""

    vessel_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the vessel (e.g., 'Manticore', 'Freya')",
    )
    manufacturer: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Ship manufacturer (e.g., 'Messer', 'Aegis', 'Anvil')",
    )
    size: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Ship size (e.g., 'Small', 'Medium', 'Large')",
    )
    vessel_class: str = Field(
        ...,
        min_length=1,
        max_length=30,
        description="Ship class (e.g., 'Fighter', 'Explorer', 'Freighter')",
    )
    role: str = Field(
        ...,
        min_length=1,
        max_length=30,
        description="Ship role (e.g., 'Combat', 'Transport', 'Mining')",
    )
    availability: str = Field(
        ...,
        min_length=1,
        max_length=30,
        description="Availability status (e.g., 'Pledge', 'Flyable', 'Retired')",
    )
    pledge: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Pledge price (e.g., '$195.00')",
    )
    status: str = Field(
        default="Active",
        min_length=1,
        max_length=20,
        description="Ship status (e.g., 'Active', 'Stored', 'Sold')",
    )


class VesselUpdate(BaseModel):
    """Fields for UPDATE operation — all optional."""

    vessel_name: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Update vessel name",
    )
    manufacturer: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Update manufacturer",
    )
    size: Optional[str] = Field(
        default=None,
        max_length=20,
        description="Update size",
    )
    vessel_class: Optional[str] = Field(
        default=None,
        max_length=30,
        description="Update class",
    )
    role: Optional[str] = Field(
        default=None,
        max_length=30,
        description="Update role",
    )
    availability: Optional[str] = Field(
        default=None,
        max_length=30,
        description="Update availability",
    )
    pledge: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Update pledge price",
    )
    status: Optional[str] = Field(
        default=None,
        max_length=20,
        description="Update status",
    )


class Vessel(BaseModel):
    """Full vessel response."""

    id: int
    vessel_name: str
    manufacturer: str
    size: str
    vessel_class: str
    role: str
    availability: str
    pledge: Optional[str] = None
    status: str

    model_config = {"from_attributes": True}


# In-memory "database" (replace with real DB later)
_hangar_db: dict = {}
_hangar_counter: int = 0


@router.get("/", response_model=list)
async def list_vessels():
    """List all player-owned ships."""
    return [vessel.model_dump() for vessel in _hangar_db.values()]


@router.post("/", response_model=Vessel, status_code=201)
async def add_vessel(vessel_create: VesselCreate) -> Vessel:
    """Add a new ship to the player fleet."""
    global _hangar_counter
    _hangar_counter += 1

    vessel = Vessel(
        id=_hangar_counter,
        vessel_name=vessel_create.vessel_name,
        manufacturer=vessel_create.manufacturer,
        size=vessel_create.size,
        vessel_class=vessel_create.vessel_class,
        role=vessel_create.role,
        availability=vessel_create.availability,
        pledge=vessel_create.pledge,
        status=vessel_create.status,
    )
    _hangar_db[_hangar_counter] = vessel
    return vessel


@router.get("/{ship_id}", response_model=Vessel)
async def get_ship(ship_id: int) -> Vessel:
    """Get a specific ship by ID."""
    if ship_id not in _hangar_db:
        raise HTTPException(status_code=404, detail="Ship not found")
    return _hangar_db[ship_id]


@router.put("/{ship_id}", response_model=Vessel)
async def update_ship(
    ship_id: int,
    vessel_update: VesselUpdate,
) -> Vessel:
    """Update a ship (partial update)."""
    if ship_id not in _hangar_db:
        raise HTTPException(status_code=404, detail="Ship not found")

    vessel = _hangar_db[ship_id]
    update_data = vessel_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(vessel, field, value)

    return vessel


@router.delete("/{ship_id}", status_code=204)
async def delete_ship(ship_id: int) -> None:
    """Delete a ship from the fleet."""
    if ship_id not in _hangar_db:
        raise HTTPException(status_code=404, detail="Ship not found")
    del _hangar_db[ship_id]