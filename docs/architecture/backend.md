# Backend Architecture — FastAPI

Overview of the backend architecture, designed for maintainability, testability, and database pluggability.

## 🏗️ High-Level Design

```
sc-oam-app Backend
┌─────────────────────────────────────────┐
│            FastAPI Application           │
│  (app.py + api/routes/ + api/models/)    │
├─────────────────────────────────────────┤
│          Database Abstraction Layer       │
│  (SQLAlchemy models + session management)│
├─────────────────────────────────────────┤
│              API Endpoints               │
│  (CRUD, crafting, warehouse, hangar)     │
├─────────────────────────────────────────┤
│             Configuration & Utilities     │
│  (.env, pyproject.toml, requirements)    │
└─────────────────────────────────────────┘
```

## 🐍 Python Package Structure

```
sc-oam-app/
├── app.py                          # FastAPI entry point
├── api/
│   ├── __init__.py                 # Package init, API router inclusion
│   ├── api.py                      # Route definitions (blueprints, crafting, etc.)
│   ├── models/                     # SQLAlchemy model definitions
│   │   ├── base.py                 # Base class, common columns
│   │   ├── blueprint.py            # Blueprint SQL model
│   │   ├── crafting.py             # Crafting result model
│   │   ├── warehouse.py            # Inventory item model
│   │   └── hangar.py               # Vessel model
│   ├── schemas/                    # Pydantic schemas (API input/output)
│   │   ├── blueprints.py           # Blueprint Pydantic models
│   │   ├── crafting.py             # Crafting Pydantic models
│   │   ├── warehouse.py            # Warehouse Pydantic models
│   │   └── hangar.py               # Hangar Pydantic models
│   └── routes/                     # FastAPI Router modules
│       ├── __init__.py             # Router inclusion in app
│       ├── blueprints.py           # Blueprint CRUD endpoints
│       └── crafting.py             # Crafting quality endpoints
├── core/                           # Core configuration
│   ├── config.py                   # Settings, environment variables
│   ├── security.py                 # JWT auth (planned)
│   └── database.py                 # SQLAlchemy engine & session
├── models/                         # SQLAlchemy ORM models
│   ├── __init__.py
│   ├── base.py                     # Base model with id, timestamps
│   ├── blueprint.py                # Blueprint table definition
│   ├── crafting.py                 # Crafting result table
│   ├── warehouse.py                # Inventory table
│   └── hangar.py                   # Fleet vessel table
├── tests/                          # Test suite
│   ├── api/
│   │   ├── test_blueprints.py
│   │   └── test_crafting.py
│   └── web/                        # (React component tests)
├── requirements.txt                # Runtime dependencies
├── requirements-dev.txt            # Dev dependencies (ruff, black, pytest)
└── pyproject.toml                  # Project config (ruff, black, pytest)
```

## 🗄️ Database Pluggability — SQLite → PostgreSQL

### Design Goal

The database layer is abstracted so the same API code works with **SQLite** (local development) or **PostgreSQL** (VPS/containers) without code changes.

### Implementation Approach

| Component | SQLite | PostgreSQL |
|-----------|--------|------------|
| **Engine Creation** | `create_engine("sqlite:///./database.db")` | `create_engine("postgresql://user:pass@host:port/db")` |
| **Session Local** | `sessionmaker(autocommit=False, autoflush=False, bind=engine)` | Same, different bind |
| **Models** | SQLAlchemy `Table` or `Mapper` | Same class definitions |
| **Migrations** | Alembic not needed (SQLite creates on startup) | **Alembic** for schema versioning |
| **Data Types** | `Integer`, `String`, `Float`, `Boolean` | Same + `UUID`, `JSONB`, `ARRAY` |
| **Connection Pool** | `NullPool` (SQLite) | `StaticPool` or `QueuePool` (PostgreSQL) |

### `core/database.py` — Core Module

```python
"""
Database layer — pluggable SQLite ↔ PostgreSQL.

Default: SQLite for local development.
Production: Configure DATABASE_URL via .env to use PostgreSQL.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import Generator

# ── Environment ─────────────────────────────────────────────
# Read from .env: DATABASE_URL="sqlite:///./database.db"
#             or DATABASE_URL="postgresql://user:pass@host:port/db"
import os
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")

# ── Engine ──────────────────────────────────────────────────
# SQLite uses connect_args for thread safety; PostgreSQL uses pool
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=None,  # NullPool for SQLite
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_size=5,
        max_overflow=10,
        echo=False,  # Set True for SQL debugging
    )

# ── Session ────────────────────────────────────────────────
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# ── ORM Base ────────────────────────────────────────────────
Base = declarative_base()

# ── Dependency ────────────────────────────────────────────────
def get_db() -> Generator:
    """FastAPI dependency that yields a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### SQLAlchemy Models Example

```python
# models/blueprint.py
from datetime import datetime
from core.database import Base

class Blueprint(Base):
    __tablename__ = "blueprints"

    id = Column(Integer, primary_key=True, index=True)
    blueprint_id = Column(String, unique=True, index=True, nullable=False)
    bp_name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    subcategory = Column(String, index=True)
    craft_type = Column(String, nullable=False)
    output_item_name = Column(String, nullable=False)
    quality_min = Column(Float, nullable=False, default=0.0)
    quality_max = Column(Float, nullable=False, default=0.0)
    craft_time_seconds = Column(Float, nullable=False, default=0.0)
    ilg_label = Column(String, nullable=False)
    owner_handle = Column(String, nullable=True)
    acquired_date = Column(String, nullable=True)  # ISO format date string
    is_learned = Column(Boolean, nullable=False, default=False)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### Pydantic Schemas (API)

```python
# schemas/blueprints.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class BlueprintBase(BaseModel):
    blueprint_id: str = Field(..., min_length=1, max_length=50)
    bp_name: str = Field(..., min_length=1, max_length=100)
    category: str = Field(..., min_length=1, max_length=50)
    subcategory: str = Field(default="uncategorized", max_length=50)
    craft_type: str = Field(..., min_length=1, max_length=50)
    output_item_name: str = Field(..., min_length=1, max_length=100)
    quality_min: float = Field(ge=0, le=1000)
    quality_max: float = Field(ge=0, le=1000, gt="quality_min")
    craft_time_seconds: float = Field(ge=0)
    ilg_label: str = Field(..., min_length=1, max_length=100)

    class Config:
        from_attributes = True  # Enable ORM mode


class BlueprintCreate(BlueprintBase):
    """Fields required for CREATE operation."""
    owner_handle: Optional[str] = Field(default="", max_length=50)
    acquired_date: Optional[str] = Field(default="", max_length=20)  # ISO format
    is_learned: bool = Field(default=False)
    notes: Optional[str] = Field(default=None, max_length=500)


class BlueprintUpdate(BaseModel):
    """Fields for UPDATE operation — all optional."""
    bp_name: Optional[str] = Field(default=None, max_length=100)
    quality_min: Optional[float] = Field(default=None, ge=0, le=1000)
    quality_max: Optional[float] = Field(default=None, gt="quality_min", le=1000)
    notes: Optional[str] = Field(default=None, max_length=500)
    is_learned: Optional[bool] = Field(default=None)


class BlueprintResponse(BlueprintCreate):
    """Full response including database-generated fields."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### API Route Using Dependency

```python
# api/routes/blueprints.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db, Base, Blueprint as BlueprintModel
from schemas.blueprints import BlueprintCreate, BlueprintUpdate, BlueprintResponse

router = APIRouter(prefix="/blueprints", tags=["blueprints"])


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
    blueprint_dict = blueprint_in.model_dump(exclude_unset=False)
    db_blueprint = BlueprintModel(**blueprint_dict)

    # Persist to database
    db.add(db_blueprint)
    db.commit()
    db.refresh(db_blueprint)

    return db_blueprint
```

### Switching from SQLite to PostgreSQL

#### Step 1: Update `.env`

```env
# Before (SQLite - default)
DATABASE_URL="sqlite:///./database.db"

# After (PostgreSQL)
DATABASE_URL="postgresql://oam_user:secret_password@db-host.example.com:5432/sc_oam_db"
```

#### Step 2: Ensure PostgreSQL is Running

```bash
# Docker Compose (if using)
docker-compose up -d db

# Or start PostgreSQL directly
# brew services start postgresql (macOS)
# sudo service postgresql start (Ubuntu)
# pg_ctlcluster 15 main start (Ubuntu 20.04+)
```

#### Step 3: Create Database

```bash
# Using psql
createdb sc_oam_db

# Or via SQL
psql -c "CREATE DATABASE sc_oam_db OWNER oam_user;"
```

#### Step 4: Run Migrations (Alembic)

```bash
# Initialize Alembic (one-time)
alembic init migrations

# Create initial migration
alembic init

# Generate migration from models
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head

# Or using FastAPI startup (auto-create for SQLite, manual for PostgreSQL)
```

#### Step 5: Verify

```bash
# Health check should work
curl http://127.0.0.1:8000/api/health

# API endpoints should function with PostgreSQL data
curl http://127.0.0.1:8000/api/blueprints/
```

## 🔒 Security Considerations

| Area | Best Practice |
|------|--------------|
| **Secret Management** | Never hardcode secrets — use `.env` + `.gitignore` |
| **CORS** | Restrict `BACKEND_CORS_ORIGINS` for production |
| **HTTPS** | Use a reverse proxy (nginx, Traefik) in production |
| **Database Auth** | Use strong passwords, limit user permissions |
| **Input Validation** | Rely on Pydantic schemas for all API input |
| **Error Handling** | Don't expose stack traces to clients (`debug=False` in prod) |
| **Dependency Scanning** | Dependabot alerts → update promptly |

### `.env` Template (never commit)

```env
# ⚠️ This file is in .gitignore — never commit real values!
# Copy .env.example → .env and fill in real values

# Application
APP_NAME="sc-oam-app"
APP_VERSION="0.1.0"
DEBUG=False  # True for dev, False for prod

# Database
DATABASE_URL="postgresql://user:password@host:port/db"
# DEFAULT: "sqlite:///./database.db" (development only)

# Security
SECRET_KEY="your-256-bit-secret-here-must-be-32-chars"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
BACKEND_CORS_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"
```

## 📦 Deployment Pipeline

| Stage | Tool/Service | Description |
|-------|--------------|-------------|
| **Local Dev** | `uvicorn`, `npm run dev` | FastAPI + Vite dev servers |
| **Docker** | `docker build`, `docker run` | Multi-stage container |
| **CI/CD** | GitHub Actions (`ci.yml`) | Lint + test on every PR |
| **Staging** | Docker Compose + test DB | Pre-production testing |
| **Production** | Docker + PostgreSQL + reverse proxy | Live deployment |

### GitHub Actions CI (Existing)

The `.github/workflows/ci.yml` already configured runs:

1. **Python lint/test** — ruff, black, isort, pytest on Python 3.10/3.11/3.12
2. **Node lint/test** — npm install, eslint, vitest on Node 20
3. **Build artifacts** — Python package build upload

### Release Process (Planned)

1. Feature complete on `develop`
2. Create release branch `release/vX.Y.Z`
3. Bump version in `pyproject.toml`
4. Run full test suite
5. `git tag -a vX.Y.Z -m "vX.Y.Z: summary"`
6. `git push origin release/vX.Y.Z && git push origin vX.Y.Z`
7. GitHub Action creates release (future enhancement)

## 🧪 Testing Strategy

| Level | Tool | Scope |
|-------|------|-------|
| **Unit** | pytest | Individual functions, model methods |
| **Integration** | pytest + TestClient | API endpoints with database |
| **API** | FastAPI TestClient | `/docs` auto-generated tests |
| **Frontend** | vitest + React Testing Library | Component rendering, user interactions |
| **E2E** | (planned) | Full user flows (Cypress/Playwright) |

### Sample API Test

```python
# tests/api/test_blueprints.py
from fastapi.testclient import TestClient
from main import app

def test_crud_lifecycle():
    client = TestClient(app)

    # Create
    bp = {
        "blueprint_id": "bp_test_001",
        "bp_name": "Test Blueprint",
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
    assert response.status_code == 201
    created = response.json()
    assert created["bp_name"] == "Test Blueprint"
    assert created["blueprint_id"] == "bp_test_001"
    bp_id = created["id"]

    # Read
    response = client.get(f"/api/blueprints/{bp_id}")
    assert response.status_code == 200
    assert response.json()["bp_name"] == "Test Blueprint"

    # Update
    response = client.put(
        f"/api/blueprints/{bp_id}",
        json={"quality_min": 600.0},
    )
    assert response.status_code == 200
    updated = response.json()
    assert updated["quality_min"] == 600.0

    # Delete
    response = client.delete(f"/api/blueprints/{bp_id}")
    assert response.status_code == 204

    # Verify deleted
    response = client.get(f"/api/blueprints/{bp_id}")
    assert response.status_code == 404
```
