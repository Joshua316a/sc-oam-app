# 📖 Technology Reference — sc-oam-app

Foundational reference documentation for all technologies, data formats, and content structures employed by this project. Serves as the "dictionary" for developers, AI agents, and collaborators.

---

## 🎮 Game Data Formats

This project interfaces with Star Citizen game data in several formats. Understanding these is key to extending the data extraction and management capabilities.

### 1. `.p4k` — Pyro Archive

| Attribute | Value |
|-----------|-------|
| **Format** | Proprietary Rockstar/CIG archive format (derived from .RPK/.ARCHIVE) |
| **Contents** | Compressed game data archives (ships, items, modules, blueprints, textures) |
| **Tools to read** | `scdatatools` (command-line), `svarog` (native macOS parser) |
| **Typical path** | `GameData/LIVE/Data.p4k` (from CIG install) |
| **Project usage** | `full_extractor.py` reads `.p4k` to populate reference DB tables; `compare_extraction_gaps.py` vs svarog validates coverage |

### 2. `.s3d` / `.s3o` — Ship & Item 3D Models

| Attribute | Value |
|-----------|-------|
| **Format** | Star Citizen 3D model formats (binary) |
| **Contents** | Mesh data, LODs, texture references for ships, weapons, equipment |
| **Tools to read** | Limited — primarily 3D software (Blender with plugins) or CIG pipeline tools |
| **Project usage** | Not directly parsed; IDs referenced via blueprint `output_item_name` and catalogue lookups |

### 3. `UE/JSON` — Universe Entity Data

| Attribute | Value |
|-----------|-------|
| **Format** | JSON-based entity definitions (used in newer CIG pipelines) |
| **Contents** | Component definitions, attachment points, default states, procedural rules |
| **Tools to read** | Any JSON parser; `jq` for CLI inspection |
| **Project usage** | Occasional reference; most data still flows through `.p4k` → `svarog` → reference DB |

### 4. CSV / TXT — Configuration Data

| Attribute | Value |
|-----------|-------|
| **Format** | Plain-text comma/tab-separated values |
| **Contents** | Ship manifest tables, item databases, manufacturer configs, module stats |
| **Tools to read** | `python csv` module, `cat`, `xlsx` import |
| **Project usage** | `modules/data_access.py` reads reference DB; historical configs may be CSV-sourced |

---

## 📡 Data Extraction Pipeline

This project's core capability lies in extracting and categorizing Star Citizen item data from game archives.

### 1. `scdatatools` (p4k → CSV/JSON)

| Attribute | Value |
|-----------|-------|
| **Purpose** | Read CIG `.p4k` archives and export item data |
| **Input** | `Data.p4k` (LIVE branch) |
| **Output** | CSV files per category (weapons, modules, cargo, etc.) |
| **CLI** | `scdatatools <p4k_path> <output_dir>` |
| **Project integration** | `scripts/compare_extraction_gaps.py` compares scdatatools output vs svarog |

### 2. `svarog` (native macOS parser)

| Attribute | Value |
|-----------|-------|
| **Purpose** | Native macOS parser for CIG game archives; faster than scdatatools on macOS |
| **Input** | `Data.p4k` (same format) |
| **Output** | Structured Python dicts / CSV |
| **Advantage** | No Windows-only dependency; native Apple silicon optimization |
| **Project integration** | `compare_extraction_gaps.py` uses svarog as the "ground truth" reference; gaps between scdatatools and svarog are documented as "extraction pipeline gap fixes" |

### 3. Extraction Pipeline Gap Summary

| Gap Category | Description | Example |
|-------------|-------------|---------|
| **Silent drop** | Items present in DB but not in code catalogue | 40 `SCItem*` items recovered |
| **ILG unmapped** | Items with NULL `item_type` — cannot categorize | Fuel Pods (30), Radars (119), Bombs (~33) |
| **Category missing** | No `TYPE_TO_LIGHTGROUP` mapping exists | New ILG categories added by CIG |
| **Type misclassification** | Wrong category assigned (e.g., Bomb → MRCK) | 1 Bomb misclassified as MRCK |

### 3. `modules/data_access.py` — Reference Database Abstraction

| Attribute | Value |
|-----------|-------|
| **Purpose** | SQLite-based reference catalogue; persists extracted game data for fast runtime access |
| **Path** | `~/Library/Caches/OrgAssetManager/databases/` (OS X) <br>or configurable via `DATABASE_URL` |
| **Schema** | Tables: `items`, `item_cross_ref`, `blueprints`, `player_inventory`, `player_ships`, `crafting_config` |
| **Key tables** | - `items`: all SC item definitions (name, category, mass, volume, price)<br>- `item_cross_ref`: category hierarchy (Vehicle Components, Weapon Attachments, etc.)<br>- `blueprints`: player-owned blueprint entries<br>- `player_inventory`: org warehouse stock<br>- `player_ships`: org hangar fleet |
| **Query patterns** | `query_items(category="weapons")`, `get_blueprints(owner_handle="oam_corp")`, `list_ships_by_role("combat")` |
| **Puggability** | `core/database.py` reads `DATABASE_URL` — SQLite default, PostgreSQL configurable; same SQLAlchemy models work for both |

### 4. Data Flow — From Archive to Reference DB

```mermaid
flowchart TD
    A[Game Data.p4k] --> B[scdatatools] --> C[CSV export]
    A --> D[svarog] --> E[Structured Python dicts]
    C --> F[compare_extraction_gaps.py] --> G[Gap report]
    E --> G
    G --> H[Fix extraction gaps] --> I[Re-extract] --> J[Reference SQLite DB]
    I --> J
    K[modules/data_access.py] --> J
    J --> L[FastAPI endpoints] --> M[React UI]
```

---

## 📦 Item Categories & Classification

This project maintains a curated catalogue of Star Citizen item types, used for:
- UI filtering and grouping
- ILG (Item Light Group) assignment
- Database categorization
- API query filtering

### 1. `modules/oam_categories.py` — OAM Category Definitions

| Attribute | Value |
|-----------|-------|
| **File** | `modules/oam_categories.py` |
| **Purpose** | Canonical list of 22 item categories + "All" used throughout the project |
| **Structure** | Module-level constants: `OAM_ITEM_CATEGORIES`, `CATEGORY_DISPLAY_NAMES`, `CATEGORY_PARENTS` |

### Category List (22 + "All")

| Category Key | Display Name | Typical Items |
|-------------|-------------|---------------|
| `all` | All | — |
| `vehicles` | Vehicles / Ships | Ships, vehicles, land rovers |
| `weapons` | Weapons | Missiles, guns, turrets |
| `modules` | Modules | Drives, reactors, shields, sensors |
| `cargo` | Cargo | Ore, trade goods, containers |
| `consumables` | Consumables | Fuel, repair kits, food |
| `equipment` | Equipment | EVA suits, backpacks, tools |
| `components` | Components | Sub-components, fittings, hardware |
| `interiors` | Interiors | Cabins, corridors, decks |
| `weapons_missiles` | Weapons — Missiles | Missile blueprints, warheads |
| `weapons_guns` | Weapons — Guns | Fixed guns, turret guns |
| `modules_shields` | Shields | Shield generators, batteries |
| `modules_drives` | Drives | Faster-than-light, impulse engines |
| `modules_sensors` | Sensors | Scanners, ladars, astrometers |
| `cargo_ore` | Ore | Tritanium, Megacyte, Nocxium, Promethium |
| `cargo_trade` | Trade Goods | Data drives, luxury items, artifacts |
| `consumables_fuel` | Fuel | Quantanium, Hydrocarbons, Isotope |
| `consumables_repair` | Repair | Nanomachine repair kits, patch kits |
| `equipment_eva` | EVA Suits | Space suits, maneuvering units |
| `equipment_tools` | Tools | Multitools, welding torches, drills |
| `flights_systems` | Flight Systems | Auto-pilot, flight computers, controllers |

### 2. Category Hierarchy

| Parent | Children |
|--------|----------|
| `vehicles` | ships, land-vehicles |
| `weapons` | `weapons_missiles`, `weapons_guns` |
| `modules` | `modules_shields`, `modules_drives`, `modules_sensors` |
| `cargo` | `cargo_ore`, `cargo_trade` |
| `consumables` | `consumables_fuel`, `consumables_repair` |
| `equipment` | `equipment_eva`, `equipment_tools` |

### 3. ILG (Item Light Group) Classification

| Attribute | Value |
|-----------|-------|
| **Concept** | Items are grouped into "light groups" for UI display purposes — e.g., all weapons share a light group, all ships share another |
| **Mapping** | `TYPE_TO_LIGHTGROUP` dict in `modules/data_extraction.py` maps item `item_type` → light group key |
| **Example** | `FUELPOD` → `Vehicles/FuelTanks` <br> `RADAR` → `Vehicles/Radars` <br> `BOMB` → `Vehicles/Ordnance` (planned) |
| **Hardcoded** | Currently in `modules/data_extraction.py` and `modules/classifier.py` — project goal: make pluggable/database-driven (see REDOX-001 in requirements) |
| **Auto-update** | Not yet implemented — runtime drift detection logs warnings but does not auto-update the mapping |

### 2. `modules/data_extraction.py` — Extraction Logic

| Attribute | Value |
|-----------|-------|
| **File** | `modules/data_extraction.py` |
| **Purpose** | Extracts items from `.p4k`/svarog, classifies into categories, assigns ILG labels |
| **Key Functions** | - `extract_items()` — main entry point <br> - `_extract_items_basic()` — basic extraction <br> - `TYPE_TO_LIGHTGROUP` — hardcoded mapping dict <br> - `_classify_inventory_lightgroups()` — assigns ILG to inventory items <br> - `_compare_ilg_categories()` — logs DB vs CODE mismatches |
| **Gap Detection** | Logs items where `item_type` is NULL or unmapped; documents as "extraction pipeline gap fixes" |

### 3. Category Query Patterns

| Purpose | Code Pattern |
|---------|-------------|
| **List all categories** | `from modules.oam_categories import OAM_ITEM_CATEGORIES; OAM_ITEM_CATEGORIES` |
| **Check if valid** | `if category in OAM_ITEM_CATEGORIES:` |
| **Display name** | `CATEGORY_DISPLAY_NAMES.get(category, category)` |
| **Filter API queries** | `GET /api/blueprints/?category=weapons` — FastAPI reads from same `OAM_ITEM_CATEGORIES` |
| **UI filter dropdown** | Populated from `OAM_ITEM_CATEGORIES` + "All" option |

---

## 🗄️ Database Schema — SQLAlchemy Models

Foundational reference for all SQLAlchemy ORM models used in the project. These models define the database structure and are designed for pluggability between SQLite (development) and PostgreSQL (production).

### 1. `models/base.py` — Base Class + Timestamps

| Attribute | Value |
|-----------|-------|
| **File** | `models/base.py` |
| **Purpose** | Mixin providing `created_at`/`updated_at` columns; base for all ORM models |

### Content

```python
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

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

## 2. `models/blueprint.py` — Blueprint ORM Model

| Attribute | Value |
|-----------|-------|
| **File** | `models/blueprint.py` |
| **Inherits** | `BaseTimeStamped`, `Base` |
| **Table** | `blueprints` |

### Columns

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | `Integer` | `primary_key=True, index=True` | DB-generated primary key |
| `blueprint_id` | `String(50)` | `unique=True, index=True, nullable=False` | User-facing identifier (e.g., `"bp_001"`) |
| `bp_name` | `String(100)` | `nullable=False` | Human-readable blueprint name |
| `category` | `String(50)` | `index=True, nullable=False` | e.g., `"weapons"`, `"modules"`, `"cargo"` |
| `subcategory` | `String(50)` | `index=True` | e.g., `"missiles"`, `"lasers"`, `"mining"` |
| `craft_type` | `String(50)` | `nullable=False` | e.g., `"missile"`, `"module"`, `"ore"` |
| `output_item_name` | `String(100)` | `nullable=False` | e.g., `"missile"` |
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

### SQLite ↔ PostgreSQL Compatibility

| Feature | SQLite | PostgreSQL |
|---------|--------|------------|
| `Integer` | `INTEGER` (8-bit signed) | `INTEGER` (32-bit signed) |
| `Float` | `REAL` or `FLOAT` | `DOUBLE PRECISION` (higher precision) |
| `String(N)` | `VARCHAR(N)` | `VARCHAR(N)` (same) |
| `Boolean` | `INTEGER (0/1)` | `BOOLEAN` (true/false) |
| `auto-create` | `Base.metadata.create_all()` | Requires `alembic upgrade head` |
| `JSON columns` | Not used | `JSONB` available (not used in v0.1.0) |

---

## 📐 Pydantic Schemas — API Input/Output Validation

Foundational reference for all Pydantic models used in the FastAPI backend. These schemas validate request/response data and map to SQLAlchemy ORM models via `from_attributes = True`.

### 1. `api/schemas/blueprints.py` — Blueprint Pydantic Models

| Attribute | Value |
|-----------|-------|
| **File** | `api/schemas/blueprints.py` |
| **Purpose** | Pydantic models for blueprint API request/response validation + ORM mode |

### `BlueprintBase` — Base Fields (shared by all operations)

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `blueprint_id` | `str` | `min_length=1, max_length=50` | User-facing BP identifier (e.g., `"bp_001")` |
| `bp_name` | `str` | `min_length=1, max_length=100` | Human-readable name |
| `category` | `str` | `min_length=1, max_length=50` | e.g., `"weapons"`, `"modules"`, `"cargo"` |
| `subcategory` | `str` | `default="uncategorized"`, `max_length=50` | Sub-category |
| `craft_type` | `str` | `min_length=1, max_length=50` | e.g., `"missile"`, `"module"`, `"ore"` |
| `output_item_name` | `str` | `min_length=1, max_length=100` | Item produced by crafting |
| `quality_min` | `float` | `ge=0, le=1000` | Minimum quality range |
| `quality_max` | `float` | `ge=0, le=1000, gt="quality_min"` | Maximum quality range |
| `craft_time_seconds` | `float` | `ge=0` | Crafting duration in seconds |
| `ilg_label` | `str` | `min_length=1, max_length=100` | ILG category label |

**Config:** `model_config = {"from_attributes": True}` — enables ORM → Pydantic conversion.

### `BlueprintCreate` — Fields for CREATE Operation

| Additional Field | Type | Default | Description |
|------------------|------|---------|-------------|
| `owner_handle` | `Optional[str]` | `""` | Owner's org handle |
| `acquired_date` | `Optional[str]` | `""` | ISO date string: `"YYYY-MM-DD"` |
| `is_learned` | `bool` | `False` | Whether blueprint is learned |
| `notes` | `Optional[str]` | `None` | Free-form notes; `max_length=500` |

### `BlueprintUpdate` — Fields for UPDATE Operation (all optional)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `bp_name` | `Optional[str]` | `None` | Update blueprint name |
| `quality_min` | `Optional[float]` | `None` | `ge=0, le=1000` if provided |
| `quality_max` | `Optional[float]` | `None` | `ge=0, le=1000, gt=quality_min` if provided |
| `notes` | `Optional[str]` | `None` | Update notes; `max_length=500` |
| `is_learned` | `Optional[bool]` | `None` | Toggle learned status |

### `BlueprintResponse` — Full Response (includes DB-generated fields)

| Field | Type | Description |
|-------|------|-------------|
| `id` | `int` | Database-generated primary key |
| `created_at` | `datetime` | UTC timestamp, auto-created |
| `updated_at` | `datetime` | UTC timestamp, auto-updated on each save |
| *(all BlueprintBase fields)* | — | — |

### 2. `api/schemas/crafting.py` — Crafting Pydantic Models

| Attribute | Value |
|-----------|-------|
| **File** | `api/schemas/crafting.py` |
| **Purpose** | Pydantic models for crafting quality/result API endpoints |

### `QualityCalculation` — Result of Quality Calculation

| Field | Type | Description |
|-------|------|-------------|
| `base_quality` | `float` | Base quality score (`quality_selector / 1000`, range 0-1) |
| `resource_qualities` | `dict[str, float]` | Per-resource quality scores (0-1000 range) |
| `resource_weights` | `dict[str, float]` | Per-resource weight/count contributing to final quality |
| `final_quality` | `float` | Enhanced/adjusted final quality (0-1 range) |

### `ResourceRequirement` — Input for Quality Calculation

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `type` | `str` | Resource type identifier | `min_length=1` |
| `amount` | `Optional[float]` | `0.0` | cSCU amount for ore/gems; `ge=0` if provided |
| `count` | `int` | `0` | Number of items (gems, objects); `ge=0` |
| `quality_selector` | `float` | `500.0` | Base quality selector (500 = average; >500 enhances, <500 reduces) | `ge=0` |

### `CraftingResult` — Output of Crafting Operation

| Field | Type | Description |
|-------|------|-------------|
| `blueprint_id` | `int` | Associated blueprint ID |
| `output_item` | `str` | Name of item produced |
| `base_quality` | `float` | Base quality before resource adjustments |
| `final_quality` | `float` | Final calculated quality after resource adjustments |
| `tier` | `str` | Quality tier: `"Common"`, `"Uncommon"`, `"Rare"`, `"Epic"`, `"Legendary"` |

---

## 🔌 API Client — React to FastAPI Communication

Reference for the frontend API client that connects the React UI to the FastAPI backend.

### 1. `web/src/lib/api.ts` — Axios-Configured Client

| Attribute | Value |
|-----------|-------|
| **File** | `web/src/lib/api.ts` |
| **Purpose** | Centralized API client for all frontend → backend communication |

### Client Configuration

```typescript
import axios from "axios"

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api"

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
    // Authorization header added interceptively if token exists
  },
)

// Request interceptor — add auth token from localStorage
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token")
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor — handle common errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired — clear localStorage
      localStorage.removeItem("access_token")
      // Could redirect to login here
    }
    return Promise.reject(error)
  }
)

// Exported helpers — used by all React components
export const get = <T>(url: string) => api.get<Response<T>>(url).then((r) => r.data.data)
export const post = <T, U>(url: string, body: U) =>
  api.post<Response<T>>(url, body).then((r) => r.data.data)
export const put = <T, U>(url: string, body: U) =>
  api.put<Response<T>>(url, body).then((r) => r.data.data)
export const del = <T>(url: string) => api.delete<Response<T>>(url).then((r) => r.data.data)
```

### Usage Examples

```typescript
// List blueprints
const { data: blueprints, loading, error } = useFetch<Blueprint[]>("blueprints/")

// Create a blueprint
await api.post("/blueprints/", {
  blueprint_id: "bp_001",
  bp_name: "Test",
  category: "weapons",
  // ... other required fields
})

// Calculate quality
const result = await api.post<QualityCalculation>(
  "/api/crafting/quality",
  { blueprintId: 1, type: "missile", qualitySelector: 750.0 }
)
```

### Environment Configuration

| File | Variable | Default | Description |
|------|----------|---------|-------------|
| `web/.env` (optional) | `VITE_API_BASE_URL` | `http://127.0.0.1:8000/api` | Base URL for API client; change for production domain |
| `app.py` (via `.env`) | `BACKEND_CORS_ORIGINS` | `http://localhost:3000,http://127.0.0.1:3000` | Must include this origin for frontend fetch to work |

---

## 📂 Data Formats & File Structures

Reference for all file formats and data structures used in the project.

### 1. SQLite Database Format

| Attribute | Value |
|-----------|-------|
| **File** | `database.db` (default, created at project root) |
| **Engine** | SQLAlchemy + `sqlite3` Python library |
| **Path** | `./database.db` (relative to project root) <br>or configurable via `DATABASE_URL` in `.env` |
| **Convention** | Never commit `database.db` to git (in `.gitignore`) <br>→ backed up separately or replaced by PostgreSQL in production |
| **Schema** | Defined by SQLAlchemy models (`models/*.py`) <br>→ Alembic migrations for PostgreSQL; auto-create for SQLite |

### 2. `.env` — Environment Configuration

| Attribute | Value |
|-----------|-------|
| **File** | `.env` (root project directory) |
| **Purpose** | Override default settings; **never committed to git** (in `.gitignore`) |
| **Format** | `KEY=VALUE` one-per-line; blank lines and `#` comments allowed |
| **Never commit these** | `DATABASE_URL` (contains secrets), `SECRET_KEY`, any real production values |
| **Template** | `.env.example` committed to git; users copy → `.env` and fill real values |

### `.env.example` Content

```env
# sc-oam-app Environment Configuration
# See https://github.com/your-org/sc-oam-app for details

# Application
APP_NAME="sc-oam-app"
APP_VERSION="0.1.0"
DEBUG=True                          # False for production

# Database (required)
DATABASE_URL="sqlite:///./database.db"
# For PostgreSQL: DATABASE_URL="postgresql://user:password@host:port/db"

# Security
SECRET_KEY="change-this-to-a-random-secret"  # 32+ chars minimum
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
BACKEND_CORS_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"
```

### 3. `requirements.txt` — Runtime Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `fastapi` | `>=0.104.0` | Web framework (API routes, dependency injection) |
| `uvicorn[standard]` | `>=0.27.0` | ASGI server (run `uvicorn app:app --reload`) |
| `python-dotenv` | `>=1.0.0` | Read `.env` files into `os.environ` |
| (other deps as added) | | |

### 4. `requirements-dev.txt` — Development Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `pytest` | `>=7.4.0` | Backend test framework |
| `ruff` | `>=0.4.0` | Linter + formatter (fast) |
| `black` | `>=23.0.0` | Python code formatter |
| `isort` | `>=5.12.0` | Import order manager |
| `typescript` | `>=5.5.2` | Type checking for frontend |
| `vite` | `>=5.3.1` | Build tool + dev server (React + Vite) |
| `tailwindcss` | `>=3.4.4` | Utility-first CSS framework |
| `eslint` | `>=8.57.0` | JS/TS linting |
| `vitest` | `>=2.0.6` | Frontend test framework (Vitest) |

---

## 🏗️ Architectural Patterns

### 1. Separation of Concerns — Three Distinct Layers

| Layer | Responsibility | Key Files |
|-------|---------------|-----------|
| **Presentation** | React + Vite + Tailwind UI, API client, page components | `web/src/`, `web/tailwind.config.js`, `web/vite.config.js` |
| **Application** | FastAPI routes, business logic, Pydantic validation | `app.py`, `api/routes/`, `api/schemas/`, `core/` |
| **Data** | SQLAlchemy models, database abstraction, extraction pipeline | `models/`, `core/database.py`, `modules/data_extraction.py` |

**Dependency Direction:** Data ← Application ← Presentation (no circular dependencies)

### 2. Database Pluggability Pattern

| Component | SQLite (dev) | PostgreSQL (prod) | Mechanism |
|-----------|-------------|-------------------|-----------|
| **Engine** | `create_engine("sqlite:///./database.db")` | `create_engine("postgresql://user:pass@host:port/db")` | `core/database.py` reads `DATABASE_URL` env var |
| **Auto-create** | `Base.metadata.create_all(engine)` | `alembic upgrade head` | Different mechanisms for each DB |
| **Session** | `sessionmaker(bind=engine)` | Same API, different bind | Identical interface, different configuration |
| **Migrations** | Not needed | `alembic upgrade head` | Alembic only for PostgreSQL |
| **Code changes** | None required | None required | Zero-code-change switch |

### 3. API Contract Pattern

| Layer | Format | Validation | Generation |
|-------|--------|------------|------------|
| **Request** | JSON bodies | Pydantic schemas (`api/schemas/*.py`) | Auto-generated into FastAPI docs at `/docs` |
| **Response** | JSON responses | Pydantic `response_model` on each route | Same schemas; `from_attributes=True` for ORM mapping |
| **OpenAPI** | Auto-generated Swagger/ReDoc | FastAPI `title/version` + route decorators | Zero extra work; `/docs` and `/redoc` URLs |

### 4. Hook-Based State Management (Frontend)

| Pattern | Description | Example Hook |
|---------|-------------|--------------|
| `useFetch<T>(url)` | Data fetching, loading/error state | `web/src/hooks/useFetch.ts` |
| Custom hooks encapsulate API calls + state, making components thin and testable | |

---

## 🔄 Integration Patterns

### 1. Backend ↔ Frontend Data Flow

```mermaid
sequenceDiagram
    participant User as Human/User
    participant UI as React Frontend
    participant API as FastAPI Backend
    participant DB as SQLite/PostgreSQL

    User->>UI: Navigate to /blueprints
    UI->>API: GET /api/blueprints/ (useFetch hook)
    API->>DB: SELECT * FROM blueprints
    DB-->>API: Blueprints rows
    API-->>UI: JSON array of blueprint objects
    UI-->>User: Render BlueprintList component
```

### 2. Environment Configuration Flow

```mermaid
graph TD
    A[.env file] --> B[os.getenv() at runtime]
    B --> C{core/database.py}
    C -->|startswith "sqlite"| D[SQLite engine]
    C -->|else| E[PostgreSQL engine]
    D --> F[SessionLocal session]
    E --> F
    F --> G[SQLAlchemy models]
    G --> H[FastAPI routes]
    H --> I[API endpoints]
    I --> J[React API client]
    J --> K[Frontend UI]
```

### 3. CI/CD Integration Pattern

| Trigger | Checks | Outcome |
|---------|--------|---------|
| `push` to `main`/`develop` | Python: ruff, black, isort, pytest on 3.10/3.11/3.12 <br> Node: npm ci, eslint, vitest, type-check on Node 20 | CI badge on GitHub; merge protected if all pass |
| `pull_request` | Same checks as push | PR cannot merge until lint + test pass |
| `Dependabot PR` | Updates deps; CI runs on new PR | Keep deps current; review & merge |

---
