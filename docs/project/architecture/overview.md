# 🏗️ Architecture — sc-oam-app

System architecture translating requirements (FR/NFR) into concrete system design. Covers backend, frontend, database, and integration patterns.

## 🌿 High-Level Overview

```
sc-oam-app System Architecture (v0.1.0)
┌─────────────────────────────────────────────────────────────────┐
│                         Presentation Layer                        │
│  ┌─────────────────────┐  ┌─────────────────────────────────┐ │
│  │  Web Browser        │  │  FastAPI + SQLAlchemy             │ │
│  │  (React + Vite)     │→ │  (app.py, api/routes, core/)      │ │
│  └─────────────────────┘  └─────────────────────────────────┘ │
│                                       ▲                         │
│                                       │                         │
│                                 API Calls (HTTP/JSON)       │
│  ┌─────────────────────┐  ┌─────────────────────────────────┐ │
│  │  React Components   │  │  API Routes + Pydantic            │ │
│  │  (pages, hooks)     │→ │  (schemas, models)               │ │
│  └─────────────────────┘  └─────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
          │                                   ▲
          │                                   │
          │                           Database Layer
          │                                   │
          ▼                                   │
 ┌─────────────────────────────────────────────────────────────┐ │
 │                    Database Pluggability                      │ │
 │  ┌─────────────────────┐  ┌─────────────────────────────────┐ │ │
 │  │  SQLite (default)   │  │  PostgreSQL (production)          │ │ │
 │  │  database.db auto-  │  │  External host or Docker          │ │ │
 │  │  created on startup │  │  Alembic migrations               │ │ │
 │  └─────────────────────┘  └─────────────────────────────────┘ │ │
 └─────────────────────────────────────────────────────────────┘ │
```

## 🐍 Backend Architecture — FastAPI + SQLAlchemy

### 1. Application Entry Point

| File | Purpose |
|------|---------|
| `app.py` | FastAPI instance, CORS middleware, startup events (DB health check), `/health` endpoint |

### 2. API Layer

| Module | Endpoints | Purpose |
|--------|-----------|---------|
| `api/routes/blueprints.py` | GET/POST/GET/{id}/PUT/{id}/DELETE/{id} | Blueprint CRUD |
| `api/routes/crafting.py` | POST `/quality`, POST `/result` | Quality calculation + crafting results |
| `api/routes/warehouse.py` *(planned)* | GET/POST/DELETE | Inventory management |
| `api/routes/hangar.py` *(planned)* | GET/POST/DELETE | Fleet vessel management |

### 3. Schema Layer (Pydantic)

| Module | Purpose |
|--------|---------|
| `api/schemas/blueprints.py` | `BlueprintBase`, `BlueprintCreate`, `BlueprintUpdate`, `BlueprintResponse` — validation + serialization |
| `api/schemas/crafting.py` | `QualityCalculation`, `ResourceRequirement`, `CraftingResult` |
| `api/schemas/warehouse.py` *(planned)* | Item schemas for warehouse inventory |
| `api/schemas/hangar.py` *(planned)* | Vessel schemas for fleet management |

### 4. ORM Layer (SQLAlchemy)

| Module | Purpose |
|--------|---------|
| `models/base.py` | `BaseTimeStamped` mixin — `created_at`, `updated_at` columns |
| `models/blueprint.py` | SQLAlchemy `Blueprint` ORM model → `blueprints` table |
| `models/crafting.py` *(planned)* | Crafting results table |
| `models/warehouse.py` *(planned)* | Inventory items table |
| `models/hangar.py` *(planned)* | Fleet vessels table |

### 5. Database Layer (Pluggable)

| Module | SQLite (dev) | PostgreSQL (prod) |
|--------|-------------|-------------------|
| `core/database.py` | `create_engine("sqlite:///./database.db")`<br>`poolclass=None` (NullPool) | `create_engine("postgresql://user:pass@host:port/db")`<br>`pool_size=5, max_overflow=10` |
| **Session** | `sessionmaker(autocommit=False, autoflush=False, bind=engine)` | Same API, different bind |
| **Auto-creation** | `database.db` created on first `Base.metadata.create_all(engine)` | Manual: `alembic init` + `alembic upgrade head` |
| **Migrations** | Not needed (SQLite auto) | **Alembic** — schema versioning, `alembic revision --autogenerate -m "msg"` + `alembic upgrade head` |
| **Connection Pool** | `NullPool` (one connection per thread) | `QueuePool` (5 base + 10 overflow) |

### 6. Dependency Injection

```python
# core/database.py — get_db dependency for FastAPI routes
def get_db() -> Generator:
    """Yield a SQLAlchemy session; FastAPI closes it after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Usage in routes:**
```python
from core.database import get_db
@router.post("/", response_model=BlueprintResponse)
async def create_blueprint(blueprint_in: BlueprintCreate, db: Session = Depends(get_db)):
    ...
```

### 7. Core Configuration

| Module | Purpose |
|--------|---------|
| `core/config.py` | Read `.env`: `DATABASE_URL`, `SECRET_KEY`, `DEBUG`, `BACKEND_CORS_ORIGINS`, `ENVIRONMENT` |
| `pyproject.toml` | Project config: `ruff`, `black`, `pytest`, `setuptools` settings |
| `.env.example` | Template (never committed); copy → `.env` for local config |

---

## ⚛️ Frontend Architecture — React + Vite + Tailwind

### 1. Application Shell

| File | Purpose |
|------|---------|
| `web/src/main.tsx` | `ReactDOM.createRoot(document.getElementById('root')!)` — renders `<App />` |
| `web/src/App.tsx` | `<BrowserRouter>` + navigation bar + `<Routes>` — page-level routing |

### 2. Page Components

| Path | Component | Purpose |
|------|-----------|---------|
| `/` | `DashboardPage` | Welcome overview; links to other pages |
| `/blueprints` | `BlueprintsPage` | Blueprint list + add/edit form |
| `/crafting` | `CraftingPage` | Quality calculator + resource selector |
| `/warehouse` | `WarehousePage` | Inventory table + item management |
| `/hangar` | `HangarPage` | Fleet table + vessel management |

### 3. Component Library

| Category | Components | Purpose |
|----------|-----------|---------|
| **Data Display** | `BlueprintList`, `FleetTable`, `InventoryTable` | Tables/grids of data from API |
| **Forms** | `BlueprintForm` (implicit via inline), `QualityCalculator` | Create/edit data, submit to API |
| **Common** | `Spinner`, `ErrorBoundary`, `ConfirmDialog` | Loading states, error handling, modals |
| **Navigation** | Top bar with links to all pages | Consistent UI across all views |

### 4. API Client

| File | Purpose |
|------|---------|
| `web/src/lib/api.ts` | Axios instance with `baseURL: VITE_API_BASE_URL`; request interceptor adds `Bearer` token from `localStorage`; response interceptor handles `401` (token expiry) |

**Exported helpers:**
- `api.get<T>(url)` — GET request, returns `T`
- `api.post<T, U>(url, body)` — POST request, returns `T`
- `api.put<T, U>(url, body)` — PUT request, returns `T`
- `api.del<T>(url)` — DELETE request, returns `T`

### 5. State Management (Simple — useState + useEffect)

| Hook | Purpose |
|------|---------|
| `useFetch<T>(url)` | Custom hook: fetches `GET url`, returns `{data, loading, error}` |
| Component-level | `useState` for form input, selected item, toggle states |

### 6. Styling — Tailwind CSS

| Config File | Purpose |
|-------------|---------|
| `web/tailwind.config.js` | Theme customization: fonts, colors (`--border`, `--background`, `--foreground`), `daisyui` plugin |
| `web/postcss.config.js` | Autoprefixer — adds vendor prefixes (`-webkit-`, `-moz-`, etc.) |
| `web/src/index.css` | `@tailwind base; @tailwind components; @tailwind utilities;` — entry point |

**Utility classes used:**
- `p-6`, `m-4`, `bg-background`, `text-foreground`, `border`, `border-border`
- `rounded`, `rounded-lg`, `rounded-sm`
- `flex`, `flex-col`, `flex-row`, `items-center`, `justify-between`
- `shadow-sm`, `shadow`, `shadow-lg`
- `hover:bg-primary`, `hover:text-primary-foreground`
- `focus:outline-none`, `focus:ring-2`, `focus:ring-primary`
- `sm:`, `md:`, `lg:`, `xl:` breakpoints (responsive grid, text sizes)

### 7. TypeScript Types

| File | Purpose |
|------|---------|
| `web/src/types/api.ts` | `Blueprint`, `QualityCalculation`, `ResourceRequirement`, `CraftingResult` — match backend Pydantic schemas |
| `web/src/types/` *(planned)* | Additional types as needed |

**Type safety patterns:**
- Fetch with typed data: `const { data: blueprints } = useFetch<Blueprint[]>("blueprints/")`
- State: `const [selected, setSelected] = useState<Blueprint | null>(null)`
- Forms: `interface BlueprintFormValues { ... }` + `useForm` or manual handling

### 8. Routing — react-router-dom

| Path | Component |
|------|-----------|
| `/` | `DashboardPage` |
| `/blueprints` | `BlueprintsPage` |
| `/crafting` | `CraftingPage` |
| `/warehouse` | `WarehousePage` |
| `/hangar` | `HangarPage` |

### 9. Hooks — Reusable Logic

| Hook | Purpose |
|------|---------|
| `useFetch<T>(url)` | Fetch data from API, return `{data, loading, error}` |
| *(planned)* | `useDebounce`, `useErrorBoundary`, `useForm`, `usePermission` |

### 10. Build & Optimization

| Config | Purpose |
|--------|---------|
| `web/vite.config.js` | Vite + React plugin + Tailwind plugin; `dev: port 3000`; `build: output to dist/` |
| `npm run dev` | `vite` — hot-reload dev server (http://127.0.0.1:3000) |
| `npm run build` | `vite build` — production build (minified, hashed) |
| `npm run preview` | `vite preview` — preview production build locally |

---

## 🗄️ Database Pluggability — Detailed Design

### Design Goal

**Zero code changes** to switch from SQLite (local development) to PostgreSQL (production/VPS). The same SQLAlchemy models + Pydantic schemas + FastAPI routes work for both.

### 1. Entry Point — `core/database.py`

```python
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")

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
        echo=False,  # True for SQL debugging
    )

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 2. Model Pattern — `models/*.py`

All models follow the same pattern, inheriting from `Base` + `BaseTimeStamped`:

```python
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from models.base import BaseTimeStamped, Base

class Blueprint(BaseTimeStamped, Base):
    __tablename__ = "blueprints"

    id = Column(Integer, primary_key=True, index=True)
    blueprint_id = Column(String(50), unique=True, index=True, nullable=False)
    bp_name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    subcategory = Column(String(50), index=True)
    craft_type = Column(String(50), nullable=False)
    output_item_name = Column(String(100), nullable=False)
    quality_min = Column(Float, nullable=False, default=0.0)
    quality_max = Column(Float, nullable=False, default=0.0)
    craft_time_seconds = Column(Float, nullable=False, default=0.0)
    ilg_label = Column(String(100), nullable=False)
    owner_handle = Column(String(50), nullable=True)
    acquired_date = Column(String(20), nullable=True)  # ISO: "2026-01-15"
    is_learned = Column(Boolean, nullable=False, default=False)
    notes = Column(String(500), nullable=True)
```

### 3. Switching Databases — Step-by-Step

#### Step 1: Update `.env`

```env
# Before (SQLite - development)
DATABASE_URL="sqlite:///./database.db"

# After (PostgreSQL - production)
DATABASE_URL="postgresql://oam_user:secret_password@db-host.example.com:5432/sc_oam_db"
```

#### Step 2: Ensure PostgreSQL Running

```bash
# Docker Compose (if using project's docker-compose.yml)
docker compose up -d db

# Or macOS Homebrew
brew services start postgresql

# Or Ubuntu
sudo service postgresql start
```

#### Step 3: Create Database

```bash
createdb sc_oam_db
# Or via psql: CREATE DATABASE sc_oam_db OWNER oam_user;
```

#### Step 4: Apply Alembic Migrations

```bash
# Initialize Alembic (one-time)
alembic init migrations

# Generate migration from models
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head
```

#### Step 5: Verify

```bash
# Health check should work
curl http://127.0.0.1:8000/api/health

# API endpoints function with PostgreSQL
curl http://127.0.0.1:8000/api/blueprints/
```

### 4. Migration Strategy — SQLite → PostgreSQL

| Phase | Action | Tool |
|-------|--------|------|
| **P1: Development** | Use SQLite via `DATABASE_URL="sqlite:///./database.db"` | No tool needed; `database.db` auto-created |
| **P2: Testing** | Switch `DATABASE_URL` to PostgreSQL in `.env` | Edit env file |
| **P3: Data Export** | If migrating existing SQLite data: `pg_dump` from old DB, or manual export/import | `pg_dump sc_oam_db_old > backup.sql` |
| **P4: Production** | Use PostgreSQL with Alembic migrations | `alembic upgrade head` on every deploy |
| **P5: Version Control** | Track migrations in git (`migrations/` dir) | `git add migrations/` + commit |

### 5. Database Diagrams (Conceptual)

```
blueprints table                     crafting_results table
─────────────────────────────        ──────────────────────────────
id (PK)                              id (PK)
blueprint_id (UK)                    blueprint_id (FK → blueprints)
bp_name                              output_item
category                             base_quality
subcategory                          final_quality
craft_type                           tier
output_item_name                     created_at
quality_min                          ...
quality_max                          ...
craft_time_seconds                   ...
ilg_label
owner_handle
acquired_date
is_learned
notes
created_at                           ...
updated_at
```

```
warehouse_items table                 hangar_vessels table
─────────────────────────────        ──────────────────────────────
id (PK)                              id (PK)
item_name                            vessel_name
category                             manufacturer
quantity                             size
location                             class
condition                            role
last_updated                         availability
created_at
updated_at
```

---

## 🔌 Integration Points

### 1. API ↔ Frontend Integration

| Flow | Description |
|------|-------------|
| **GET /api/blueprints/** → `BlueprintsPage` | `useFetch<Blueprint[]>("blueprints/")` → renders table or "no data" state |
| **POST /api/blueprints/** → form submission | `api.post("blueprints/", formData)` → on success, refetch list; on error, show error state |
| **POST /api/crafting/quality** → `CraftingPage` | `api.post("/crafting/quality", {blueprintId, type, qualitySelector})` → display `final_quality` |
| **GET /api/warehouse/** → `WarehousePage` | `useFetch<Item[]>("warehouse/")` → renders `InventoryTable` |
| **GET /api/hangar/** → `HangarPage` | `useFetch<Vessel[]>("hangar/")` → renders `FleetTable` |

### 2. Environment Configuration

| File | Variable | Default | Description |
|------|----------|---------|-------------|
| `.env` | `DATABASE_URL` | `sqlite:///./database.db` | Switch to PostgreSQL for production |
| `.env` | `SECRET_KEY` | `change-this-to-a-random-secret` | JWT signing key (planned v1.1.0) |
| `.env` | `DEBUG` | `True` | `False` for production; affects error detail exposure |
| `.env` | `BACKEND_CORS_ORIGINS` | `http://localhost:3000,http://127.0.0.1:3000` | Add production origins for deploy |
| `web/.env` | `VITE_API_BASE_URL` | `http://127.0.0.1:8000/api` | Base URL for API client; change for production domain |

### 3. CI/CD Integration

| Workflow | Trigger | Checks |
|----------|---------|--------|
| `.github/workflows/ci.yml` | `push` (main/develop), `pull_request` (main/develop) | - Python: ruff, black, isort, pytest on 3.10/3.11/3.12<br>- Node: npm ci, eslint, vitest, type-check on Node 20 |

### 4. Deployment Pipeline

| Stage | Tool | Description |
|-------|------|-------------|
| **Local Dev** | `uvicorn app:app --reload` + `npm run dev` | Two terminals; auto-reload on file changes |
| **Docker Dev** | `docker compose up -d` | Backend + frontend + PostgreSQL (if desired) in containers |
| **CI/CD** | GitHub Actions (`ci.yml`) | Lint + test on every PR; block merge if failures |
| **Staging** | Docker Compose + test DB | Deploy to staging environment for final QA |
| **Production** | Docker + PostgreSQL + reverse proxy (nginx/Traefik) | Live deployment with HTTPS, backups, monitoring |

---

## 📦 File Map — Architecture Layer

| Directory | Files | Purpose |
|-----------|-------|---------|
| `docs/project/architecture/` | `overview.md` | This file — system architecture |
| `docs/project/architecture/backend.md` | *(planned)* | Deep-dive on FastAPI + SQLAlchemy |
| `docs/project/architecture/frontend.md` | *(planned)* | Deep-dive on React + Vite + Tailwind |
| `pyproject.toml` | — | Python project config reflecting requirements |
| `requirements.txt` | — | Runtime dependencies |
| `app.py` | — | FastAPI entry point |
| `core/` | `database.py`, `config.py` | Database layer + configuration |
| `api/` | `routes/`, `schemas/`, `models/` | FastAPI routes + Pydantic + SQLAlchemy |
| `web/` | `src/`, `package.json`, `vite.config.js`, `tailwind.config.js` | React + Vite + Tailwind frontend |

---

## ✅ Architecture Validation Checklist

| Question | Answer |
|----------|--------|
| Does every FR have at least one technical implementation path? | ✅ Yes — each FR maps to API route + model + frontend component |
| Is database pluggability (SQLite ↔ PostgreSQL) explicitly designed? | ✅ Yes — `core/database.py` reads `DATABASE_URL`; same models work for both |
| Are TypeScript types aligned with Python Pydantic schemas? | ✅ Yes — `web/src/types/api.ts` mirrors `api/schemas/*.py` |
| Are Tailwind utilities semantic, not inline `style=`? | ✅ Yes — documented in `docs/architecture/frontend.md` |
| Does CI (GitHub Actions) validate the architecture? | ✅ Yes — ruff + black + isort + pytest + vitest all run on every PR |
| Are there any circular imports or tight couplings? | ✅ No — `core/database.py` is independent; `api/routes/` depend on `core` + `schemas` + `models` only |
| Is the architecture documented for both human and AI consumers? | ✅ Yes — `docs/project/architecture/overview.md` + `docs/ai-agents/` guides |
| **Is three-tier authentication designed and documented?** | ✅ Yes — OS login, Google OAuth, RSI integration covered in `docs/project/architecture/overview.md` |

---

## 🔐 Authentication Integration (v1.1.0-planned)

### Three-Tier Design Summary

sc-oam-app v1.1.0 will integrate a three-tier authentication system:

| Tier | Purpose | Implementation |
|------|---------|----------------|
| **OS Login** | Admin/power user operations | `keyring` library, OS-native keychain |
| **Google OAuth** | Primary user auth | OAuth 2.0 / OpenID Connect, refresh tokens |
| **RSI Account** | Pledge hangar data | PyRSI v0.1.19, username/password → session |

### Google OAuth

- Client ID/secret from Google Cloud Console
- Scope: `openid profile email`
- 15-min access / 30-day refresh tokens
- Storage: encrypted file or keychain

### RSI Integration

- PyRSI library (v0.1.19) for website access
- `RSISite.authenticate(username, password)`
- Hangar data: `site.hangar.ships`, `site.hangar.items`, etc.
- Session persisted in `.pyrsi_session` config

### Token Vault

- Fernet encryption for token data
- Hierarchy: keychain → encrypted file → env vars
- Auto-refresh for Google; session reload for RSI

### API Endpoints (planned)

- `GET /auth/status` — authentication state
- `GET/POST /auth/login/google` — Google OAuth flow
- `POST /auth/rsi/login` — RSI username/password login
- `GET /auth/rsi/hangar` — pledge hangar data

### Backward Compatibility

- All v0.1.0 API tests continue unauthenticated
- New endpoints opt-in per tier
- App functional without auth (limited features)
```




## 📦 Docker & Extraction (v1.1.0-planned)

**Single-Container Deployment:**
- sc-oam-app can be run as a single Docker container bundling FastAPI backend, React frontend, and SQLite database
- End-users only need Docker installed; data persists in `./db/` host folder
- `docker compose up` starts all services; `./run.sh` is the one-command launch

**Extraction Pipeline**:
- `POST /api/extraction/run` runs the Data.p4k → SQLite migration pipeline
- Parses original OAM `.p4k` archives into reference databases
- Databases created in `./db/` and consumed by the app

**See also**: `docs/architecture/overview.md` for full Docker + Extraction details.
