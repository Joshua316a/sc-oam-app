# 📐 Low-Level Design / Specs — sc-oam-app

Detailed module specifications, API endpoint definitions, data models, and module-level designs. This is the "code-ready" documentation that developers (human or AI) use to implement features.

## 🎯 Purpose

This document provides:
- **Module-level specs** — Each module's interface, inputs, outputs, and behavior
- **API endpoint specs** — Full request/response schemas, error handling, examples
- **Pydantic model specs** — Field definitions, validators, validators, ORM mapping
- **SQLAlchemy model specs** — Table definitions, column types, constraints, indexes
- **Component specs** — React component props interfaces, state shapes, hook APIs

All specs are designed to be implementation-ready: a developer should be able to start coding from these specs without needing to read the requirements or architecture documents.

---

# 📐 Low-Level Design / Specs — sc-oam-app

Detailed module specifications, API endpoint definitions, data models, and module-level designs.

---

# 📐 Module Specifications

## 1. `app.py` — FastAPI Application Entry Point

| Attribute | Value |
|-----------|-------|
| **File** | `app.py` |
| **Purpose** | Creates FastAPI instance, configures middleware, defines root endpoints |
| **Key Exports** | `app` (FastAPI instance) |

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check — `{status: "ok", service: "OAM API", version: "0.1.0"}` |
| `GET` | `/` (root) | Root response — `{name: "sc-oam-app", version: "0.1.0"}` (development only) |

### Configuration

| Setting | Source | Default |
|---------|--------|---------|
| `DEBUG` | `os.getenv("DEBUG", "True")` | `True` (development) |
| `ENVIRONMENT` | `os.getenv("ENVIRONMENT", "development")` | `development` |
| `BACKEND_CORS_ORIGINS` | `os.getenv("BACKEND_CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")` | Allow localhost dev origins |

### Code Structure

```python
"""sc-oam-app FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="OAM API",
    description="Org Asset Manager API — FastAPI + React Web UI",
    version="0.1.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Overridden by .env in production via allowlist
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["root"])
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "service": "OAM API", "version": "0.1.0"}
```

---

# 📐 Module Specifications (continued)

## 2. `api/routes/blueprints.py` — Blueprint CRUD Endpoints

| Attribute | Value |
|-----------|-------|
| **File** | `api/routes/blueprints.py` |
| **Prefix** | `/api/blueprints` |
| **Tags** | `["blueprints"]` |
| **Purpose** | Create, read, update, delete blueprint entries |

### Pydantic Schemas

#### `BlueprintBase` — Base Fields (shared by create/update/response)

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `blueprint_id` | `str` | Unique blueprint identifier | `min_length=1, max_length=50` |
| `bp_name` | `str` | Blueprint name | `min_length=1, max_length=100` |
| `category` | `str` | Item category | `min_length=1, max_length=50` |
| `subcategory` | `str` | Sub-category | `default="uncategorized", max_length=50` |
| `craft_type` | `str` | Type of crafting | `min_length=1, max_length=50` |
| `output_item_name` | `str` | Item produced by crafting | `min_length=1, max_length=100` |
| `quality_min` | `float` | Minimum quality range | `ge=0, le=1000` |
| `quality_max` | `float` | Maximum quality range | `ge=0, le=1000, gt="quality_min"` |
| `craft_time_seconds` | `float` | Time to craft | `ge=0` |
| `ilg_label` | `str` | ILG category label | `min_length=1, max_length=100` |

#### `BlueprintCreate` — Fields for CREATE Operation

| Additional Field | Type | Default | Description |
|------------------|------|---------|-------------|
| `owner_handle` | `Optional[str]` | `""` | Owner's org handle |
| `acquired_date` | `Optional[str]` | `""` | ISO date string: `"YYYY-MM-DD"` |
| `is_learned` | `bool` | `False` | Whether blueprint is learned |
| `notes` | `Optional[str]` | `None` | Free-form notes; `max_length=500` |

#### `BlueprintUpdate` — Fields for UPDATE Operation (all optional)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `bp_name` | `Optional[str]` | `None` | Update blueprint name |
| `quality_min` | `Optional[float]` | `None` | `ge=0, le=1000` if provided |
| `quality_max` | `Optional[float]` | `None` | `ge=0, le=1000, gt=quality_min` if provided |
| `notes` | `Optional[str]` | `None` | Update notes; `max_length=500` |
| `is_learned` | `Optional[bool]` | `None` | Toggle learned status |

#### `BlueprintResponse` — Full Response (includes DB-generated fields)

| Field | Type | Description |
|-------|------|-------------|
| `id` | `int` | Database-generated primary key |
| `created_at` | `datetime` | UTC timestamp, auto-created |
| `updated_at` | `datetime` | UTC timestamp, auto-updated on each save |
| *(all BlueprintBase fields)* | — | — |

**Config:** `class Config: from_attributes = True` — enables ORM → Pydantic conversion.

### Route Handlers

| Method | Path | Request | Response | Status | Description |
|--------|------|---------|----------|--------|-------------|
| `POST` | `/` | `BlueprintCreate` | `BlueprintResponse` | `201` | Create new blueprint; `400` if `blueprint_id` already exists |
| `GET` | `/` | — | `list[BlueprintResponse]` | `200` | List all blueprints (paginatable in future) |
| `GET` | `/{blueprint_id}` | — | `BlueprintResponse` | `200` | Get blueprint by ID; `404` if not found |
| `PUT` | `/{blueprint_id}` | `BlueprintUpdate` | `BlueprintResponse` | `200` | Partial update; `404` if not found |
| `DELETE` | `/{blueprint_id}` | — | `204` | `204` no-content; `404` if not found |

### Business Logic

```python
@router.post("/", response_model=BlueprintResponse, status_code=201)
async def create_blueprint(
    blueprint_in: BlueprintCreate,
    db: Session = Depends(get_db),
) -> BlueprintResponse:
    """Create a new blueprint entry."""
    
    # Check for duplicate blueprint_id
    existing = db.query(BlueprintModel).filter(
        BlueprintModel.blueprint_id == blueprint_in.blueprint_id
    ).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Blueprint with id '{blueprint_in.blueprint_id}' already exists",
        )
    
    # Build ORM model from Pydantic schema
    db_blueprint = BlueprintModel(**blueprint_in.model_dump())
    
    # Persist to database
    db.add(db_blueprint)
    db.commit()
    db.refresh(db_blueprint)
    
    # Return Pydantic response (ORM → Pydantic via from_attributes)
    return db_blueprint
```

### Error Responses

| Status | Model | Body Example |
|--------|-------|-------------|
| `400` | `HTTPException` | `{"detail": "Blueprint with id 'bp_001' already exists"}` |
| `404` | `HTTPException` | `{"detail": "Blueprint not found"}` |
| `422` | Validation error (FastAPI auto) | `{"detail": {"blueprint_id": ["Missing required field"]}}` |

---

## 3. `api/routes/crafting.py` — Crafting Quality Endpoints

| Attribute | Value |
|-----------|-------|
| **File** | `api/routes/crafting.py` |
| **Prefix** | `/api/crafting` |
| **Tags** | `["crafting"]` |
| **Purpose** | Quality calculation and crafting result generation |

### Pydantic Schemas

#### `QualityCalculation` — Result of Quality Calculation

| Field | Type | Description |
|-------|------|-------------|
| `base_quality` | `float` | Base quality score (0-1 range, derived from quality_selector/1000) |
| `resource_qualities` | `dict[str, float]` | Per-resource quality scores (0-1000 range) |
| `resource_weights` | `dict[str, float]` | Per-resource weight/count contributing to final quality |
| `final_quality` | `float` | Enhanced/adjusted final quality (0-1 range) |

#### `ResourceRequirement` — Input for Quality Calculation

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `type` | `str` | Resource type identifier | `min_length=1` |
| `amount` | `Optional[float]` | `0.0` | cSCU amount for ore/gems; `ge=0` if provided |
| `count` | `int` | `0` | Number of items (gems, objects); `ge=0` |
| `quality_selector` | `float` | `500.0` | Base quality selector (500 = average, >500 = enhances, <500 = reduces) | `ge=0` |

#### `CraftingResult` — Output of Crafting Operation

| Field | Type | Description |
|-------|------|-------------|
| `blueprint_id` | `int` | Associated blueprint ID |
| `output_item` | `str` | Name of item produced |
| `base_quality` | `float` | Base quality (same as `QualityCalculation.base_quality`) |
| `final_quality` | `float` | Final calculated quality after resource adjustments |
| `tier` | `str` | Quality tier: `"Common"`, `"Uncommon"`, `"Rare"`, `"Epic"`, `"Legendary"` |

### Route Handlers

| Method | Path | Request | Response | Status | Description |
|--------|------|---------|----------|--------|-------------|
| `POST` | `/quality` | `ResourceRequirement` | `QualityCalculation` | `200` | Calculate quality score for given resources |
| `POST` | `/result` | `ResourceRequirement` | `CraftingResult` | `200` | Get crafting result with tier determination |

### Business Logic — Quality Calculation

```python
@router.post("/quality", response_model=QualityCalculation)
async def calculate_quality(
    req: ResourceRequirement,
    db: Session = Depends(get_db),
) -> QualityCalculation:
    """Calculate quality score for crafting."""
    
    # Simplified quality calculation:
    # base = quality_selector / 1000 (range 0-1)
    # final = base + (average_resource_quality - 500) * 0.1 / 1000 (small adjustment)
    
    base = req.quality_selector / 1000.0
    
    # Calculate average resource quality (if resource_qualities provided in future)
    # For now, use quality_selector as baseline
    avg_resource = req.quality_selector  # placeholder; will use resource_qualities when implemented
    
    final = base + (avg_resource - 500.0) * 0.1 / 1000.0
    
    return QualityCalculation(
        base_quality=round(base, 2),
        resource_qualities={req.type: req.quality_selector / 1000.0},
        resource_weights={req.type: 1.0},
        final_quality=round(final, 2),
    )
```

### Error Responses

| Status | Model | Body Example |
|--------|-------|-------------|
| `422` | Validation error (FastAPI auto) | `{"detail": {"quality_selector": ["Greater than or equal to 0 is required"]}}` |
| `500` | Unexpected error | `{"detail": "Internal server error"}` (FastAPI default) |

---

## 4. SQLAlchemy Model Specifications

### 4.1 `models/base.py` — Base Class + Timestamps

| Attribute | Value |
|-----------|-------|
| **File** | `models/base.py` |
| **Purpose** | Shared base class for all ORM models; provides `created_at`/`updated_at` |

### Content

```python
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Mixin providing created_at/updated_at columns
class BaseTimeStamped:
    """Mixin that adds created_at and updated_at timestamp columns."""
    
    created_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        comment="UTC timestamp when row was created",
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        comment="UTC timestamp when row was last updated",
    )

# Declarative base for all SQLAlchemy models
Base = declarative_base()
```

### Usage

```python
from models.base import BaseTimeStamped, Base

class Blueprint(BaseTimeStamped, Base):
    __tablename__ = "blueprints"
    # ... additional columns
```

---

## 4.2 `models/blueprint.py` — Blueprint ORM Model

| Attribute | Value |
|-----------|-------|
| **File** | `models/blueprint.py` |
| **Inherits** | `BaseTimeStamped`, `Base` |
| **Table** | `blueprints` |

### Columns

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | `Integer` | `primary_key=True, index=True` | DB-generated PK |
| `blueprint_id` | `String(50)` | `unique=True, index=True, nullable=False` | User-facing BP identifier (e.g., `"bp_001"`) |
| `bp_name` | `String(100)` | `nullable=False` | Human-readable blueprint name |
| `category` | `String(50)` | `index=True, nullable=False` | e.g., `"weapons"`, `"modules"`, `"cargo"` |
| `subcategory` | `String(50)` | `index=True` | e.g., `"missiles"`, `"lasers"`, `"mining"` |
| `craft_type` | `String(50)` | `nullable=False` | e.g., `"missile"`, `"module"`, `"ore"` |
| `output_item_name` | `String(100)` | `nullable=False` | e.g., `"missile"`, `"mining_drone"` |
| `quality_min` | `Float` | `nullable=False, default=0.0` | Minimum quality range (0-1000) |
| `quality_max` | `Float` | `nullable=False, default=1000.0` | Maximum quality range (0-1000, must be >= quality_min) |
| `craft_time_seconds` | `Float` | `nullable=False, default=0.0` | Crafting duration in seconds |
| `ilg_label` | `String(100)` | `nullable=False` | ILG category: `"Weapons/Missiles"`, etc. |
| `owner_handle` | `String(50)` | `nullable=True` | Org handle of owner (e.g., `"oam_corp"`) |
| `acquired_date` | `String(20)` | `nullable=True` | ISO format: `"YYYY-MM-DD"`; e.g., `"2026-01-15"` |
| `is_learned` | `Boolean` | `nullable=False, default=False` | Whether the player has learned this BP |
| `notes` | `String(500)` | `nullable=True` | Free-form notes |

### Indexes

| Index | Columns | Purpose |
|-------|---------|---------|
| `ix_blueprints_blueprint_id` | `blueprint_id` | Fast lookup by user-facing ID; enforces uniqueness |
| `ix_blueprints_category` | `category` | Filter queries by category (warehouse/hangar reports) |
| `ix_blueprints_is_learned` | `is_learned` | Query learned vs unlearned blueprints |

### Example Usage

```python
from models.blueprint import Blueprint
from core.database import get_db, engine, Base
from sqlalchemy import select

# Create tables (SQLite: auto; PostgreSQL: via Alembic migration)
Base.metadata.create_all(bind=engine)

# Insert a new blueprint
new_bp = Blueprint(
    blueprint_id="bp_001",
    bp_name="Tactical Missile Blueprint",
    category="weapons",
    subcategory="missiles",
    craft_type="missile",
    output_item_name="missile",
    quality_min=500.0,
    quality_max=800.0,
    craft_time_seconds=30.0,
    ilg_label="Weapons/Missiles",
    is_learned=True,
    notes="High-yield missile blueprint acquired from mission reward.",
)

with SessionLocal() as db:
    db.add(new_bp)
    db.commit()
    db.refresh(new_bp)
    print(f"Created BP ID {new_bp.id}, DB ID {new_bp.blueprint_id}")
```

### SQLite → PostgreSQL Compatibility

| Feature | SQLite | PostgreSQL |
|---------|--------|------------|
| `Integer` | `INTEGER` (8-bit signed) | `INTEGER` (32-bit signed) |
| `Float` | `REAL` or `FLOAT` | `DOUBLE PRECISION` (higher precision) |
| `String(N)` | `VARCHAR(N)` | `VARCHAR(N)` (same) |
| `Boolean` | `INTEGER (0/1)` | `BOOLEAN` (true/false) |
| `auto-create` | `Base.metadata.create_all()` | Requires `alembic upgrade head` |
| `JSON columns` | Not used | `JSONB` available (not used in v0.1.0) |

---

## 5. Pydantic Schema Specifications

### 5.1 `api/schemas/blueprints.py` — Blueprint Pydantic Models

| Attribute | Value |
|-----------|-------|
| **File** | `api/schemas/blueprints.py` |
| **Purpose** | Pydantic models for blueprint API request/response validation + ORM mode |

### Content

```python
from pydantic import BaseModel, Field, Optional as OptionalTy
from typing import Optional as OptionalTy
from datetime import datetime
from typing import Optional, Dict, Any


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
        gt="quality_min",
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
    
    owner_handle: OptionalTy[str] = Field(
        default="",
        max_length=50,
        description="Owner's org handle (e.g., 'oam_corp')",
    )
    acquired_date: OptionalTy[str] = Field(
        default="",
        max_length=20,
        description="ISO date string 'YYYY-MM-DD'; e.g. '2026-01-15'",
    )
    is_learned: bool = Field(
        default=False,
        description="Whether the player has learned this blueprint",
    )
    notes: OptionalTy[str] = Field(
        default=None,
        max_length=500,
        description="Free-form notes about this blueprint",
    )


class BlueprintUpdate(BaseModel):
    """Fields for UPDATE operation — all optional."""
    
    bp_name: OptionalTy[str] = Field(
        default=None,
        max_length=100,
        description="Update blueprint name (partial update)",
    )
    quality_min: OptionalTy[float] = Field(
        default=None,
        ge=0,
        le=1000,
        description="Update quality_min; ge=0, le=1000 if provided",
    )
    quality_max: OptionalTy[float] = Field(
        default=None,
        gt="quality_min",
        le=1000,
        description="Update quality_max; gt=quality_min, le=1000 if provided",
    )
    notes: OptionalTy[str] = Field(
        default=None,
        max_length=500,
        description="Update free-form notes",
    )
    is_learned: OptionalTy[bool] = Field(
        default=None,
        description="Toggle learned status",
    )


class BlueprintResponse(BlueprintBase):
    """Full response including database-generated fields."""
    
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}
```

### 5.2 `api/schemas/crafting.py` — Crafting Pydantic Models

| Attribute | Value |
|-----------|-------|
| **File** | `api/schemas/crafting.py` |
| **Purpose** | Pydantic models for crafting quality/result API endpoints |

### Content

```python
from pydantic import BaseModel, Field, Optional as OptionalTy
from typing import Optional, Dict, Any, Any


class QualityCalculation(BaseModel):
    """Result of a quality calculation."""
    
    base_quality: float = Field(
        ge=0,
        le=1,
        description="Base quality score (quality_selector / 1000, range 0-1)",
    )
    resource_qualities: Dict[str, float] = Field(
        default_factory=dict,
        description="Per-resource quality scores (0-1000 range)",
    )
    resource_weights: Dict[str, float] = Field(
        default_factory=dict,
        description="Per-resource weight/count contributing to final quality",
    )
    final_quality: float = Field(
        ge=0,
        le=1,
        description="Final adjusted quality after resource contributions",
    )


class ResourceRequirement(BaseModel):
    """Input parameters for quality calculation / crafting result."""
    
    type: str = Field(
        ...,
        min_length=1,
        description="Resource type identifier (e.g., 'element', 'mercox', 'isogen')",
    )
    amount: Optional[float] = Field(
        default=0.0,
        ge=0,
        description="cSCU amount for ore/gems; 0 if not applicable",
    )
    count: int = Field(
        default=0,
        ge=0,
        description="Number of items (gems, manufactured objects); 0 if not applicable",
    )
    quality_selector: float = Field(
        ...,
        ge=0,
        description="Base quality selector (500 = average; >500 enhances; <500 reduces quality)",
    )


class CraftingResult(BaseModel):
    """Output of a crafting operation."""
    
    blueprint_id: int = Field(
        ge=0,
        description="Associated blueprint ID from database",
    )
    output_item: str = Field(
        ...,
        min_length=1,
        description="Name of item produced (e.g., 'missile')",
    )
    base_quality: float = Field(
        ge=0,
        le=1,
        description="Base quality before resource adjustments",
    )
    final_quality: float = Field(
        ge=0,
        le=1,
        description="Final quality after resource contributions",
    )
    tier: str = Field(
        ...,
        description="Quality tier: 'Common', 'Uncommon', 'Rare', 'Epic', 'Legendary'",
    )
```

---

## 6. React Component Specifications

### 6.1 `web/src/components/BlueprintList.tsx` — Blueprint List Component

| Attribute | Value |
|-----------|-------|
| **File** | `web/src/components/BlueprintList.tsx` |
| **Purpose** | Display a list/grid of blueprints with filtering and selection |

### Props Interface

```typescript
interface BlueprintListProps {
  /** Array of blueprint data from API */
  blueprints: Blueprint[]
  /** Called when user selects/edits a blueprint */
  onSelect: (blueprint: Blueprint) => void
  /** Called when user deletes a blueprint */
  onDelete: (blueprintId: string) => void
  /** Called when user opens add/edit form */
  onEdit: (blueprint: Blueprint) => void
  /** Optional loading state */
  loading?: boolean
  /** Optional error state */
  error?: string
}
```

### Component Behavior

| State | Description |
|-------|-------------|
| `loading` | Shows `Spinner` component while API data is fetching |
| `error` | Displays error message if API fetch fails |
| `blueprints.length === 0` | Shows "No blueprints found. Add one using the navigation." |
| `blueprints.length > 0` | Renders `BlueprintTable` or `BlueprintGrid` with data |

### Render Output

```tsx
// Pseudo-code of render logic
{if (loading) return <Spinner />}
{if (error) return <p className="text-destructive">{error}</p>}
{if (blueprints.length === 0) return <p className="text-muted-foreground">No blueprints found...</p>}
{/* Render table/grid with blueprint data */}
/* Each row: blueprint.name, category, ilg_label, actions (edit, delete) }*/
```

### Exported API

```typescript
export const BlueprintList: React.FC<BlueprintListProps>
```

### Dependencies

- `react`, `react-dom`
- `@mui/material` or Tailwind classes (project uses Tailwind — use `className` for styling)
- `axios` (via `web/src/lib/api.ts`)

---

## 6.2 `web/src/components/QualityCalculator.tsx` — Crafting Quality Calculator

| Attribute | Value |
|-----------|-------|
| **File** | `web/src/components/QualityCalculator.tsx` |
| **Purpose** | Two-section layout: Resources Required (left) + Calculated Properties (right) |

### Props Interface

```typescript
interface QualityCalculatorProps {
  /** Blueprint ID to calculate quality for */
  blueprintId: number
  /** Called when calculation completes */
  onResult: (result: QualityCalculation) => void
  /** Called on error */
  onError: (error: string) => void
}
```

### Form Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | `string` | Resource type (e.g., `"element"`, `"mercox"`, `"isogen"`) |
| `qualitySelector` | `number` | Base quality selector (500 = average; range 0-1000) |
| `amount` | `Optional<number>` | cSCU amount (0 if not applicable) |
| `count` | `number` | Number of items (0 if not applicable) |

### Two-Section Layout

**Left Column (Resources Required):**
- Resource type dropdown (populated from API or hardcoded options)
- Quality selector slider (0-1000, default 500)
- Amount input (cSCU, optional)
- Count input (number, optional)
- "Calculate" button

**Right Column (Calculated Properties):**
- Base quality display (output of API call, range 0-1)
- Final quality display (after resource adjustments, range 0-1)
- Quality tier badge ("Common"/"Uncommon"/etc.)
- Resource quality weights breakdown

### API Call

```typescript
// Inside component, on "Calculate" click:
const result = await api.post<QualityCalculation>(
  "/api/crafting/quality",
  {
    type,
    amount,
    count,
    qualitySelector,
  }
)
onResult(result)  // Pass result up to parent
```

### Exported API

```typescript
export const QualityCalculator: React.FC<QualityCalculatorProps>
```

### Dependencies

- `react`, `react-dom`
- `axios` (via `web/src/lib/api.ts`)
- Tailwind classes for two-column layout (`grid grid-cols-1 md:grid-cols-2 gap-6`)
- `@testing-library/react` (for tests)

---

## 6.3 `web/src/components/FleetTable.tsx` — Fleet Vessel Table

| Attribute | Value |
|-----------|-------|
| **File** | `web/src/components/FleetTable.tsx` |
| **Purpose** | Display player-owned ships from hangar database |

### Props Interface

```typescript
interface FleetTableProps {
  /** Ships data from API */
  ships: Vessel[]
  /** Called when user selects a ship */
  onSelect: (ship: Vessel) => void
  /** Called when user edits a ship */
  onEdit: (ship: Vessel) => void
  /** Called when user deletes a ship */
  onDelete: (shipId: string) => void
  /** Loading state */
  loading?: boolean
  /** Error state */
  error?: string
}
```

### Ship Data Fields (from `Vessel` type)

| Field | Type | Description |
|-------|------|-------------|
| `id` | `number` | DB-generated primary key |
| `vessel_name` | `string` | Ship name (e.g., `"Manticore"`, `"Freya"`) |
| `manufacturer` | `string` | e.g., `"Messer", "Aegis", "Anvil"` |
| `size` | `string` | e.g., `"Small", "Medium", "Large"` |
| `class` | `string` | e.g., `"Fighter", "Explorer", "Freighter"` |
| `role` | `string` | e.g., `"Combat", "Transport", "Mining"` |
| `availability` | `string` | e.g., `"Pledge", "Flyable", "Retired"` |
| `pledge` | `Optional[string]` | Pledge price (e.g., `"$195.00"`) |
| `status` | `string` | e.g., `"Active", "Stored", "Sold"` |

### Render Behavior

| Condition | Output |
|-----------|--------|
| `loading` | `<Spinner />` |
| `error` | `<p className="text-destructive">{error}</p>` |
| `ships.length === 0` | `<p className="text-muted-foreground">No ships in fleet.</p>` |
| `ships.length > 0` | `<Table>` with columns: Name, Manufacturer, Size, Class, Role, Availability, Pledge, Actions |

### Table Columns

| Column | Data Field | Sortable |
|--------|-----------|----------|
| Name | `ship.vessel_name` | Yes |
| Manufacturer | `ship.manufacturer` | Yes |
| Size | `ship.size` | Yes |
| Class | `ship.class` | Yes |
| Role | `ship.role` | Yes |
| Availability | `ship.availability` | Yes |
| Pledge | `ship.pledge` | Yes |
| Actions | — | — (edit/delete buttons) |

### Exported API

```typescript
export const FleetTable: React.FC<FleetTableProps>
```

### Dependencies

- Tailwind for table styling (`w-full bg-card border border-border rounded`)
- `react-icons` (optional: delete icon, edit icon)
- `axios` (via `api.ts` for delete/edit API calls)

---

## 6.4 `web/src/components/InventoryTable.tsx` — Warehouse Inventory Table

| Attribute | Value |
|-----------|-------|
| **File** | `web/src/components/InventoryTable.tsx` |
| **Purpose** | Display player inventory items from warehouse database |

### Props Interface

```typescript
interface InventoryTableProps {
  /** Items data from API */
  items: InventoryItem[]
  /** Called when user selects an item */
  onSelect: (item: InventoryItem) => void
  /** Called when user edits an item */
  onEdit: (item: InventoryItem) => void
  /** Called when user deletes an item */
  onDelete: (itemId: number) => void
  /** Loading state */
  loading?: boolean
  /** Error state */
  error?: string
}
```

### Inventory Item Data Fields (from `InventoryItem` type)

| Field | Type | Description |
|-------|------|-------------|
| `id` | `number` | DB-generated primary key |
| `item_name` | `string` | e.g., `"Tritanium", "Megacyte", "Nocxium"` |
| `category` | `string` | e.g., `"resources", "components", "modules"` |
| `quantity` | `number` | Current stack size in player hangar |
| `capacity` | `number` | Max stack size (25000 for common resources) |
| `location` | `string` | e.g., `"Hangar", "Asset Hangar", "Market"` |
| `last_updated` | `string` | ISO timestamp: `"2026-01-15T10:30:00Z"` |

### Render Behavior

| Condition | Output |
|-----------|--------|
| `loading` | `<Spinner />` |
| `error` | `<p className="text-destructive">{error}</p>` |
| `items.length === 0` | `<p className="text-muted-foreground">No items in inventory.</p>` |
| `items.length > 0` | `<Table>` with columns: Name, Category, Quantity/Capacity, Location, Last Updated, Actions |

### Table Columns

| Column | Data Field | Format |
|--------|-----------|--------|
| Name | `item.item_name` | Plain text |
| Category | `item.category` | Capitalized (e.g., `"Resources"`) |
| Quantity/Capacity | `${item.quantity}/${item.capacity}` | `quantity/Capacity` |
| Location | `item.location` | Plain text |
| Last Updated | `item.last_updated` | Relative time: `"2 hours ago"` or full ISO |
| Actions | — | Edit/delete buttons |

### Exported API

```typescript
export const InventoryTable: React.FC<InventoryTableProps>
```

### Dependencies

- Tailwind for responsive table (`w-full bg-card border border-border rounded`)
- `react-icons` (delete/edit icons)
- `axios` (for delete/edit API calls via `api.ts`)

---

## 7. Custom Hook Specifications

### 7.1 `web/src/hooks/useFetch.ts` — Data Fetching Hook

| Attribute | Value |
|-----------|-------|
| **File** | `web/src/hooks/useFetch.ts` |
| **Purpose** | Reusable hook for fetching data from FastAPI endpoints |

### Return Interface

```typescript
interface UseFetchResult<T> {
  data: T | null
  loading: boolean
  error: string | null
}
```

### Hook Logic

```typescript
import { useEffect, useState } from "react"
import { api } from "../lib/api"

export function useFetch<T>(url: string): UseFetchResult<T> {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchData() {
      try {
        const result = await api.get<T>(url)
        setData(result)
      } catch (err) {
        setError((err as Error).message)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [url])

  return { data, loading, error }
}
```

### Usage Example

```typescript
const { data: blueprints, loading, error } = useFetch<Blueprint[]>("blueprints/")

if (loading) return <Spinner />
if (error) return <p className="text-destructive">{error} />

return <BlueprintList blueprints={blueprints} onSelect={...} onDelete={...} onEdit={...} />
```

### Dependencies

- `react`, `react-dom`
- `web/src/lib/api.ts` (configured with `baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api"`)

---

## 8. Test Specifications

### 8.1 Backend (pytest) — API Tests

| File | `tests/api/test_blueprints.py` |
|------|-------------------------------|

#### `test_crud_lifecycle` — Full CRUD Test

```python
from fastapi.testclient import TestClient
from main import app

def test_crud_lifecycle():
    """Test complete CREATE-READ-UPDATE-DELETE lifecycle for blueprints."""
    client = TestClient(app)

    # 1. CREATE: Post a new blueprint
    bp = {
        "blueprint_id": "bp_test_001",
        "bp_name": "Test Missile Blueprint",
        "category": "weapons",
        "subcategory": "missiles",
        "craft_type": "missile",
        "output_item_name": "missile",
        "quality_min": 500.0,
        "quality_max": 800.0,
        "craft_time_seconds": 30.0,
        "ilg_label": "Weapons/Missiles",
    }
    response = client.post("/api/blueprints/", json=bp)
    assert response.status_code == 201, f"Create failed: {response.text}"
    created = response.json()
    assert created["bp_name"] == "Test Missile Blueprint"
    assert created["blueprint_id"] == "bp_test_001"
    bp_id = created["id"]  # DB-generated ID

    # 2. READ: Get the created blueprint
    response = client.get(f"/api/blueprints/{bp_id}")
    assert response.status_code == 200, f"Read failed: {response.text}"
    assert response.json()["bp_name"] == "Test Missile Blueprint"

    # 3. UPDATE: Modify quality_min
    response = client.put(
        f"/api/blueprints/{bp_id}",
        json={"quality_min": 600.0},
    )
    assert response.status_code == 200, f"Update failed: {response.text}"
    updated = response.json()
    assert updated["quality_min"] == 600.0

    # 4. DELETE: Remove the blueprint
    response = client.delete(f"/api/blueprints/{bp_id}")
    assert response.status_code == 204, f"Delete failed: {response.text}"

    # 5. Verify deletion
    response = client.get(f"/api/blueprints/{bp_id}")
    assert response.status_code == 404, "Blueprint should no longer exist"
```

#### `test_list_empty` — Initial State

```python
def test_list_empty():
    """GET /api/blueprints/ returns empty list when no data."""
    client = TestClient(app)
    response = client.get("/api/blueprints/")
    assert response.status_code == 200
    assert len(response.json()) == 0
```

#### `test_duplicate_id` — Duplicate Prevention

```python
def test_duplicate_id():
    """POST /api/blueprints/ returns 400 if blueprint_id already exists."""
    client = TestClient(app)

    bp = {
        "blueprint_id": "bp_duplicate",
        "bp_name": "Duplicate",
        "category": "test",
        "subcategory": "test",
        "craft_type": "test",
        "output_item_name": "test",
        "quality_min": 100.0,
        "quality_max": 200.0,
        "craft_time_seconds": 1.0,
        "ilg_label": "Test",
    }

    # First create
    client.post("/api/blueprints/", json=bp)

    # Second create with same blueprint_id should fail
    response = client.post("/api/blueprints/", json=bp)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]
```

### 8.2 Frontend (vitest + React Testing Library) — Component Tests

| File | `web/src/components/__tests__/BlueprintList.test.tsx` |
|------|------------------------------------------------------|

#### `renders_heading_and_placeholder` — Basic Render Test

```typescript
import { render, screen } from "@testing-library/react"
import { BlueprintsList } from "../BlueprintList"

describe("BlueprintsList", () => {
  it("renders heading and placeholder when no data", () => {
    render(<BlueprintsList />)

    expect(screen.getByRole("heading", { level: 2 })).toBeInTheDocument()
    expect(
      screen.getByText("No blueprints found. Add one using the navigation."),
    ).toBeInTheDocument()
  })
})
```

#### `fetches_and_displays_blueprints` — API Integration Test

```typescript
import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { BlueprintsList } from "../BlueprintList"
import axios from "axios"

// Mock axios globally
beforeEach(() => {
  jest.spyOn(axios, "get").mockResolvedValueOnce({
    data: {
      data: [
        {
          id: 1,
          blueprint_id: "bp_001",
          bp_name: "Test Missile",
          category: "weapons",
          subcategory: "missiles",
          craft_type: "missile",
          output_item_name: "missile",
          quality_min: 500,
          quality_max: 800,
          craft_time_seconds: 30,
          ilg_label: "Weapons/Missiles",
          owner_handle: "",
          acquired_date: "",
          is_learned: false,
          notes: "",
          created_at: "",
          updated_at: "",
        },
      ],
      success: true,
      message: "",
    },
    status: 200,
  } as any)
})

describe("BlueprintsList with data", () => {
  it("fetches and displays blueprints", async () => {
    render(<BlueprintsList />)

    expect(screen.getByRole("heading", { level: 2 })).toBeInTheDocument()
    expect(screen.getByText("Test Missile")).toBeInTheDocument()
  })
})
```

#### `shows_error_when_api_fails` — Error Handling Test

```typescript
import { render, screen } from "@testing-library/react"
import axios from "axios"

beforeEach(() => {
  jest.spyOn(axios, "get").mockRejectedValueOnce(new Error("Network error"))
})

describe("BlueprintsList error handling", () => {
  it("shows error when API fails", async () => {
    render(<BlueprintsList />)

    expect(screen.getByText("Network error")).toBeInTheDocument()
  })
})
```

### 8.3 Test Configuration

| File | `vitest.config.ts` |
|------|-------------------|
| **Coverage** | `enabled: true, provider: "v8", reporter: ["text", "json", "html"]` |
| **Environment** | `environment: "jsdom"` |
| **Globals** | `globals: true` (assert, expect, describe, it, test available without import) |
| **Setup File** | `vitest.setup.ts` (includes `@testing-library/jest-dom`) |

### 8.4 Running Tests

```bash
# Backend: all API tests
pytest -v

# Backend: specific test file
pytest tests/api/test_blueprints.py -v

# Frontend: all component tests
cd web && npm test

# Frontend: specific test file
cd web && npx vitest run components/__tests__/BlueprintList.test.tsx
```

---
