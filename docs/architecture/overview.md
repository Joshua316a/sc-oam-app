# Architecture Overview

Complete system architecture for sc-oam-app, integrating backend (FastAPI), frontend (React), and database pluggability.

## 🏗️ System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      sc-oam-app Architecture                     │
├─────────────────────┬───────────────────────────────────────┤
│                     │                                     │
│   ┌─────────────►  │  ┌─────────────────────────────────┐ │
│   │  Frontend     │→ │  FastAPI + SQLAlchemy ORM        │ │
│   │  (React + Vite)│   │  (app.py, api/routes/, core/)    │ │
│   │               │   │                                     │ │
│   │   API Client  │   │  API Endpoints:                   │ │
│   │   (axios)      │   │  • Blueprint CRUD                 │ │
│   │               │   │  • Crafting Quality               │ │
│   │   │             │   │  • Warehouse Inventory            │ │
│   │   │             │   │  • Fleet Vessels                  │ │
│   ▼   ▼             ▼   ▼                                     │
│ ┌────────────────────────────────────────────────────────┐ │ │
│ │                     .env                               │ │ │
│ │  DATABASE_URL="sqlite:///./database.db"                │ │ │
│ │  (or) DATABASE_URL="postgresql://..."                 │ │ │
│ └────────────────────────────────────────────────────────┘ │ │
├───────────────────────────────────────────────────────────────┤
│                      DATABASE LAYER                            │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────┐  ┌─────────────────────────────────┐ │
│  │  SQLite (dev)   │  │  PostgreSQL (prod/container)    │ │
│  │  database.db    │  │  External host or Docker          │ │
│  │  auto-created   │  │  Alembic migrations               │ │
│  │  (on startup)   │  │  Manual schema management         │ │
│  └─────────────────┘  └─────────────────────────────────┘ │
│                                                               │
│  ORM: SQLAlchemy  Core: core/database.py                      │
│  Models: models/*.py  Schemas: api/schemas/*.py              │
│                                                               │
├───────────────────────────────────────────────────────────────┤
│                        CONFIGURATION                          │
├───────────────────────────────────────────────────────────────┤
│  ┌─────────────────────┐  ┌───────────────────────────────┐ │
│  │  pyproject.toml     │  │  .env (never committed)         │ │
│  │  requirements.txt   │  │  DATABASE_URL                     │ │
│  │  requirements-dev.txt│  │  SECRET_KEY                       │ │
│  │                     │  │  DEBUG/ENVIRONMENT               │ │
│  │                     │  │  BACKEND_CORS_ORIGINS            │ │
│  └─────────────────────┘  └───────────────────────────────┘ │
├───────────────────────────────────────────────────────────────┤
│                        GITHUB INTEGRATION                      │
├───────────────────────────────────────────────────────────────┤
│  .github/                                                   │
│  ├── workflows/ci.yml          # Lint + test on every PR      │ │
│  ├── dependabot.yml           # Automated dependency updates  │ │
│  ├── PULL_REQUEST_TEMPLATE.md # Standardized PR contributions │ │
│  └── CODEOWNERS             # File-specific reviewers       │ │
├───────────────────────────────────────────────────────────────┤
│                        DEPLOYMENT                             │
├───────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌────────────────────────────────┐ │
│  │  Local Dev      │  │  Docker (dev + prod)             │ │ │
│  │  uvicorn ...    │  │  docker build + docker compose   │ │ │
│  │  npm run dev    │  │  docker-compose up -d            │ │ │
│  └─────────────┘  └────────────────────────────────┘ │ │
│  ┌─────────────┐  ┌────────────────────────────────┐ │
│  │  GitHub Actions │  │  VPS / PythonAnywhere          │ │ │
│  │  (CI/CD)        │  │  Docker + reverse proxy          │ │ │
│  └─────────────┘  └────────────────────────────────┘ │ │
├───────────────────────────────────────────────────────────────┤
│                        DOCUMENTATION                          │
├───────────────────────────────────────────────────────────────┤
│  docs/                                                      │
│  ├── getting-started/         # New collaborator onboarding   │ │
│ ├── contributing/             # Human developer guidelines   │ │
│ ├── ai-agents/                # AI agent identification,      │ │
│  │                          #   platforms, context, tools  │ │ │
│ ├── api-reference/            # Auto-generated + structured   │ │
│ │                          #   endpoint docs            │ │ │
│ ├── troubleshooting/          # Common issues + fixes        │ │
│ ├── deployment/               # Docker, VPS, production       │ │
│ └── architecture/             # Backend + Frontend design    │ │
└───────────────────────────────────────────────────────────────┘
```

## 🐍 Backend — FastAPI + SQLAlchemy

### Key Design Principles

| Principle | Implementation |
|-----------|---------------|
| **Database Pluggability** | `core/database.py` reads `DATABASE_URL` from `.env` — SQLite default, PostgreSQL configurable |
| **API-First Design** | All data access through FastAPI endpoints with Pydantic schemas |
| **Testability** | FastAPI `TestClient` + SQLAlchemy `session` dependency injection |
| **Type Safety** | SQLAlchemy models + Pydantic schemas share same data definitions |
| **Security** | Secrets via environment, CORS restriction, input validation via Pydantic |
| **Extensibility** | Modular router structure — add new feature by adding route file + models |

### Core Modules

| Module | Purpose |
|--------|---------|
| `app.py` | FastAPI entry point, middleware (CORS), startup events |
| `core/config.py` | Settings management via `python-dotenv` |
| `core/database.py` | Engine, session, Base — pluggable SQLite/PostgreSQL |
| `api/models/*.py` | SQLAlchemy ORM models (database tables) |
| `api/schemas/*.py` | Pydantic models (API input/output, validation) |
| `api/routes/*.py` | FastAPI routers with CRUD endpoints |
| `core/security.py` (planned) | JWT auth, password hashing |

### Database Pluggability Detail

#### SQLite (Development Default)

```python
# core/database.py — SQLite configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=None,  # NullPool — one connection per thread
    )
```

**Pros:**
- Zero setup — `database.db` created on first run
- No external service needed
- Great for local development, testing

**Cons:**
- Not suitable for concurrent/multi-user
- Limited advanced data types
- File-locking issues under heavy write load

#### PostgreSQL (Production)

```python
# core/database.py — PostgreSQL configuration
else:
    engine = create_engine(
        DATABASE_URL,
        pool_size=5,           # Connections in pool
        max_overflow=10,       # Overflow allowed
        echo=False,            # Set True for SQL debugging
    )
```

**Pros:**
- Multi-user concurrent access
- Advanced data types (JSONB, ARRAY, UUID)
- Robust transaction handling
- Industry-standard for web apps
- Docker/VPS compatible

**Cons:**
- Requires PostgreSQL server setup
- Needs `alembic` migrations for schema changes
- Connection management overhead

### Switching Between Databases

```bash
# 1. Update .env (create from .env.example)
DATABASE_URL="postgresql://oam_user:password@localhost:5432/sc_oam_db"

# 2. Ensure PostgreSQL running
# Docker: docker-compose up -d db
# Or: brew services start postgresql (macOS)

# 3. Create database
createdb sc_oam_db

# 4. Apply Alembic migrations
alembic upgrade head

# 5. Verify
uvicorn app:app --reload
# Visit: http://127.0.0.1:8000/api/blueprints/
```

## ⚛️ Frontend — React + Vite + Tailwind

### Key Design Principles

| Principle | Implementation |
|-----------|---------------|
| **API Client Layer** | All calls go through `web/src/lib/api.ts` — single point of URL/config change |
| **Type Safety** | Full TypeScript types in `web/src/types/` matching backend Pydantic schemas |
| **Responsive Design** | Tailwind CSS breakpoints for mobile-first design |
| **Component Composition** | Small, focused components composed together |
| **Hooks over Classes** | `useFetch`, `useDebounce` custom hooks for reusable logic |
| **Testing Ready** | Vitest + React Testing Library configured from Day 1 |

### Core Modules

| Module | Purpose |
|--------|---------|
| `web/src/main.tsx` | ReactDOM root rendering |
| `web/src/App.tsx` | Navigation + Route definitions |
| `web/src/App.css` (minimal) | Global styles — mostly Tailwind utilities |
| `web/src/components/` | Reusable UI components (BlueprintList, QualityCalculator, etc.) |
| `web/src/hooks/` | Custom React hooks (useFetch, useDebounce, etc.) |
| `web/src/lib/api.ts` | Axios-configured API client |
| `web/src/types/` | TypeScript interfaces matching backend schemas |
| `web/src/pages/` | Page-level components per route |
| `web/tailwind.config.js` | Theme customization, content paths |
| `web/vite.config.js` | Vite config, plugins, build options |

### Component Guidelines

#### ✅ Do

- Use PascalCase for component names: `BlueprintList`
- Use camelCase for props and variables: `blueprintId`
- Export components as named exports: `export const BlueprintsList = ...`
- Keep components focused — one responsibility each
- Use Tailwind utility classes for styling
- Type props interfaces explicitly
- Handle loading, error, and empty states

#### ❌ Don't

- Use inline `style=` props (use Tailwind classes)
- Mix camelCase and PascalCase inconsistently
- Export default components (use named exports)
- Skip error/loading state handling
- Hardcode API URLs (use `api.ts` client)

### Page Architecture

```
App.tsx
├── / — DashboardPage
│   └── Welcome text + overview stats
├── /blueprints — BlueprintsPage
│   ├── BlueprintsList component
│   ├── Add/Edit form (modal)
│   └── API: GET/POST /api/blueprints/
├── /crafting — CraftingPage
│   ├── QualityCalculator component
│   ├── ResourceRequirement form
│   └── API: POST /api/crafting/quality
├── /warehouse — WarehousePage
│   ├── InventoryTable component
│   ├── Add item form
│   └── API: GET /api/warehouse/
└── /hangar — HangarPage
    ├── FleetTable component
    ├── Add vessel form
    └── API: GET /api/hangar/
```

## 🗄️ Database Layer — Detailed Design

### SQLAlchemy Model Base

```python
# models/base.py
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

class BaseTimeStamped:
    """Mixin providing created_at/updated_at columns."""
    created_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

Base = declarative_base()
```

### Example Model — Blueprint

```python
# models/blueprint.py
from sqlalchemy import Column, String, Integer, Float, Boolean
from models.base import BaseTimeStamped, Base

class Blueprint(BaseTimeStamped, Base):
    __tablename__ = "blueprints"

    id = Column(Integer, primary_key=True, index=True)
    blueprint_id = Column(String(50), unique=True, index=True, nullable=False)
    bp_name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    subcategory = Column(String(50), index=True, nullable=False)
    craft_type = Column(String(50), nullable=False)
    output_item_name = Column(String(100), nullable=False)
    quality_min = Column(Float, nullable=False, default=0.0)
    quality_max = Column(Float, nullable=False, default=0.0)
    craft_time_seconds = Column(Float, nullable=False, default=0.0)
    ilg_label = Column(String(100), nullable=False)
    owner_handle = Column(String(50), nullable=True)
    acquired_date = Column(String(20), nullable=True)  # ISO format: "2026-01-15"
    is_learned = Column(Boolean, nullable=False, default=False)
    notes = Column(String(500), nullable=True)
```

### Pydantic Schemas — Matching Models

```python
# schemas/blueprints.py
from pydantic import BaseModel, Field, Optional
from datetime import datetime
from typing import Optional as OptionalTy

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
        from_attributes = True


class BlueprintCreate(BlueprintBase):
    owner_handle: Optional[str] = Field(default="", max_length=50)
    acquired_date: Optional[str] = Field(default="", max_length=20)
    is_learned: bool = Field(default=False)
    notes: Optional[str] = Field(default=None, max_length=500)


class BlueprintUpdate(BaseModel):
    bp_name: Optional[str] = Field(default=None, max_length=100)
    quality_min: Optional[float] = Field(default=None, ge=0, le=1000)
    quality_max: Optional[float] = Field(
        default=None, gt="quality_min", le=1000
    )
    notes: Optional[str] = Field(default=None, max_length=500)
    is_learned: Optional[bool] = Field(default=None)


class BlueprintResponse(BlueprintCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### API Route Using Both

```python
# api/routes/blueprints.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.blueprint import Blueprint as BlueprintModel
from schemas.blueprints import BlueprintCreate, BlueprintUpdate, BlueprintResponse
from core.database import get_db, Base

router = APIRouter(prefix="/blueprints", tags=["blueprints"])


@router.post("/", response_model=BlueprintResponse, status_code=201)
async def create_blueprint(
    blueprint_in: BlueprintCreate,
    db: Session = Depends(get_db),
) -> BlueprintResponse:
    """Create a new blueprint — works with SQLite or PostgreSQL."""
    
    # Check for duplicate (SQLite or PostgreSQL alike)
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
    
    # Persist
    db.add(db_blueprint)
    db.commit()
    db.refresh(db_blueprint)

    # Return Pydantic response (ORM → Pydantic via from_attributes)
    return db_blueprint
```

## 🔄 Data Flow — Request Lifecycle

### 1. Frontend User Action

```
User clicks "Calculate Quality" button
→ useFetch hook calls api.post("/api/crafting/quality", {...})
```

### 2. API Client

```typescript
// web/src/lib/api.ts
post("/crafting/quality", {
  blueprintId: 1,
  type: "missile",
  qualitySelector: 750.0,
})
```

### 3. HTTP Request

```
POST http://127.0.0.1:8000/api/crafting/quality
Content-Type: application/json
Body: { "blueprintId": 1, "type": "missile", "qualitySelector": 750.0 }
```

### 4. FastAPI Route

```python
# api/routes/crafting.py
@router.post("/quality")
async def calculate_quality(
    req: ResourceRequirement,  # Pydantic validates JSON body
    db: Session = Depends(get_db),
) -> QualityCalculation:
    # ... business logic using SQLAlchemy models
    # ... returns Pydantic response model
```

### 5. Business Logic

```python
# Simplified quality calculation
def calculate_quality(req: ResourceRequirement) -> QualityCalculation:
    base = req.quality_selector / 1000.0
    # ... compute final quality from resource qualities
    return QualityCalculation(
        base_quality=round(base, 2),
        resource_qualities=req.resource_qualities,
        resource_weights=req.resource_weights,
        final_quality=round(final, 2),
    )
```

### 6. Response

```json
HTTP 200 OK
{
  "base_quality": 0.75,
  "resource_qualities": {"element": 0.85},
  "resource_weights": {"element": 0.2},
  "final_quality": 0.82
}
```

### 7. Frontend Handles Response

```typescript
// useFetch or direct API call
const { data, error } = await api.post("/api/crafting/quality", body)

// Display result
setResult(data?.final_quality ?? 0)
setError(error?.message ?? null)
```

## 🔐 Authentication Design (v1.1.0-planned)

### Three-Tier Authentication Architecture

sc-oam-app employs a three-tier authentication system designed to support different user roles and data access patterns:

| Tier | Purpose | Method | Token Lifetime |
|------|---------|--------|----------------|
| **1: OS-Level** | Admin/Power User operations | OS Keychain (macOS Keychain, Linux Keyring, Windows Credential Manager) via `keyring` library | Until app clear/reinstall |
| **2: Google OAuth** | Primary user authentication | OAuth 2.0 + OpenID Connect, `openid profile email` scope | 15-min access / 30-day refresh |
| **3: RSI Account** | Pledge hangar & ship data | PyRSI library (`rsi.RSISite`) username/password → session cookies | Session-based, persisted via `.pyrsi_session` |

#### Tier 1: OS-Level Authentication (Admin/Power User)

- **Library**: `keyring` (cross-platform)
- **Storage**: OS-native secure keychain
- **Use Case**: Admin operations, config changes, power user overrides
- **Code Example**:
  ```python
  import keyring
  keyring.set_password('sc-oam-app', 'admin_user', token_data)
  token = keyring.get_password('sc-oam-app', 'admin_user')
  ```

#### Tier 2: Google OAuth 2.0 (Primary User Auth)

- **Protocol**: OAuth 2.0 + OpenID Connect
- **Scope**: `openid profile email`
- **Token Flow**: 15-min access tokens, 30-day refresh tokens
- **Storage**: Encrypted file `~/.config/sc-oam-app/tokens.json` (Fernet) or keychain
- **Flow**:
  1. User clicks "Login with Google"
  2. Redirect to Google OAuth consent screen
  3. Exchange authorization code → access_token + refresh_token
  4. Store encrypted refresh token
  5. Auto-refresh when access token expires
- **Code Pattern**:
  ```python
  from authlib.integrations.starlette_client import OAuth
  oauth.register(name='google', client_id=..., client_secret=...,
                 server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
                 client_kwargs={'scope': 'openid profile email'})
  # Login route → authorize_redirect
  # Callback → authorize_access_token → store token → set session
  ```

#### Tier 3: RSI Account Data Access

- **Library**: PyRSI v0.1.19 (`rsi.RSISite`)
- **Auth Method**: Username/password → session cookies
- **Data Access**: `site.hangar` (ships, items, packages, upgrades), `site.citizen()`, `site.org()`
- **Session Persistence**: `.pyrsi_session` config file, auto-load on startup
- **Fallback**: Browser automation (Selenium/Playwright) if PyRSI endpoints change
- **Code Pattern**:
  ```python
  from rsi import RSISite
  site = RSISite()
  site.authenticate(username, password)
  if site.is_authenticated:
      hangar = site.hangar
      ships = hangar.ships
      items = hangar.items
  ```

### Token Management Design

#### Unified Token Store Structure

```
~/.config/sc-oam-app/
├── tokens.json          # Google OAuth tokens (encrypted via Fernet)
├── rsi_token.json       # RSI session data
├── keychain/            # OS keychain entries (if available)
└── app.db              # Application database
```

#### Token Encryption

- **Primary**: `cryptography.fernet` (symmetric encryption)
- **Key Source**: `SC_OAM_TOKEN_KEY` env var or auto-generated
- **Algorithm**: Fernet (AES-128-CBC with 128-bit SHA HMAC)
- **Fallback**: OS keychain via `keyring` library

#### Token Refresh Logic

| Auth Type | Access Token | Refresh Token | Expiry Handling |
|-----------|-------------|---------------|-----------------|
| **Google** | ~15 minutes | ~30 days | Use refresh_token → new access_token; force re-auth if refresh expired |
| **RSI** | Session-based | Persistent via `.pyrsi_session` | Auto-load on startup; re-auth when session invalid (401/timeout) |
| **OS Keychain** | Until removed | N/A | No expiry; cleared on app uninstall |

#### Vault Class Design

```python
from cryptography.fernet import Fernet
import os
import json

class TokenVault:
    def __init__(self):
        key = os.getenv('SC_OAM_TOKEN_KEY') or Fernet.generate_key()
        self._fernet = Fernet(key)
    
    def encrypt(self, data: dict) -> str:
        json_data = json.dumps(data).encode()
        return self._fernet.encrypt(json_data).decode()
    
    def decrypt(self, token: str) -> dict:
        json_data = self._fernet.decrypt(token.encode())
        return json.loads(json_data)
```

### API Endpoint Design

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/auth/status` | GET | Check current auth status | Yes (self) |
| `/auth/login/google` | GET | Initiate Google OAuth flow | No |
| `/auth/callback/google` | GET | Handle Google OAuth callback | No |
| `/auth/rsi/login` | POST | Authenticate with RSI | No |
| `/auth/rsi/logout` | POST | Clear RSI session | Yes (self) |
| `/auth/rsi/hangar` | GET | Get RSI hangar data | Yes (Tier 3) |

#### Auth Status Response

```json
{
  "authenticated": true,
  "auth_tier": "google",       // "os", "google", "rsi", or null
  "user": {
    "id": "google-uid-123",
    "email": "user@example.com",
    "name": "Colin Smith"
  },
  "tiers": {
    "google": {"active": true, "since": 1731157200},
    "rsi": {"active": true, "since": 1731150000},
    "os": {"active": true}
  }
}
```

### User Flow Design

#### Flow 1: New User - Google Login
1. User opens app → `/auth/status` → `{authenticated: false}`
2. User clicks "Login with Google"
3. → Redirect to `/auth/login/google`
4. → Google OAuth consent screen
5. User grants permissions
6. → Redirect to `/auth/callback/google`
7. → Exchange code → tokens stored encrypted
8. → `/auth/status` → `{authenticated: true, auth_tier: "google"}`

#### Flow 2: Returning User - Auto-Login
1. User opens app
2. → Check `/auth/status`
3. → Find valid Google refresh token
4. → Use refresh token → new access token (no user interaction)
5. → `/auth/status` → `{authenticated: true, auth_tier: "google"}`

#### Flow 3: RSI Data Integration
1. User clicks "Connect RSI Account"
2. → `/auth/rsi/login` → prompt for username/password
3. → RSISite.authenticate(username, password)
4. → Session stored in `.pyrsi_session`
5. → `/auth/rsi/hangar` → fetch hangar data
6. → `/auth/status` → shows RSI tier active

#### Flow 4: Admin OS Login
1. Admin operation triggered
2. → Check auth status → no Google/RSI token for admin
3. → Prompt "Enter OS credentials for admin access"
4. → keyring operations with service 'sc-oam-app-admin'
5. → Perform admin operation
6. → Clear credentials after operation

### Security Considerations

- **Token interception**: HTTPS for all API calls; tokens never in URLs
- **Token storage**: Encrypted file with Fernet; keychain preferred
- **Token leakage**: Never log tokens; clear from memory after use
- **Refresh token theft**: Short lifetime (30 days); rotate on each use
- **CSRF protection**: State parameter on OAuth flows; SameSite cookies
- **Session fixation**: Regenerate session ID after OAuth login
- **Encryption at rest**: All sensitive data encrypted

### Implementation Roadmap

| Phase | Tasks | Estimated Effort |
|-------|-------|------------------|
| **P1: Google OAuth** | Cloud project setup, OAuth flow, token storage, status endpoint | ~4 days |
| **P2: RSI Integration** | PyRSI module, login/logout/hangar endpoints, token management | ~4 days |
| **P3: OS Auth** | keyring integration, admin guard, auth status checks | ~2 days |
| **P4: Polish** | Token vault, auto-refresh, error handling, UI feedback | ~3.5 days |
| **Total** | | **~13.5 days (3 weeks)** |

### Integration Points with Existing Code

| Component | Auth Integration Point |
|-----------|----------------------|
| FastAPI routes | Depend on `auth` status before processing |
| Crafting quality | User-specific quality presets based on tier |
| Warehouse model | RSI data can populate warehouse items |
| API tests | All 4 existing tests continue unauthenticated |
| Database | User ID stored with records for multi-user support |

### Backward Compatibility

- ✅ All 4 existing API tests continue unauthenticated (public endpoints)
- ✅ New auth endpoints don't break existing routes
- ✅ Optional auth - app works without authentication (limited features)
- ✅ Token storage is opt-in per tier

---



## 🐳 Docker & Extraction (v1.1.0)

### Single-Container Deployment

sc-oam-app can be run as a single Docker container that bundles the FastAPI backend, React frontend, and SQLite database. This simplifies deployment for end-users who only need Docker installed.

**Container Overview:**
- **Image**: Multi-stage build (Node + Python)
- **Ports**: 8000 (FastAPI) + 3000 (React dev server)
- **Database**: SQLite stored on host via volume mount (`./db/`)
- **Entry point**: `docker compose up` or `./run.sh`

**Dockerfile** (`Dockerfile`):
- Multi-stage build: first stage installs Node/Pnpm + builds React app
- Second stage: Python runtime with uvicorn
- Environment: `DATABASE_URL="sqlite:////host_db/database.db"` (4 slashes = absolute path mount)
- Environment variables: `.env.example` provided

**docker-compose.yml** (`docker-compose.yml`):
- 3 services: PostgreSQL (optional), FastAPI backend, React frontend
- SQLite data persists in host `./db/` folder via volume mount
- `docker compose up` starts all services

**run.sh** (`run.sh`):
- One-command launch: `docker compose up --build -d`
- Outputs service URLs and instructions

### Extraction Pipeline (Data.p4k → Reference DB)

The extraction pipeline migrates legacy Tkinter OAM game data (`.p4k` archives) into reference SQLite databases usable by sc-oam-app.

**Purpose**: Migrate data from the original OAM application's `.p4k` files into the new sc-oam-app database format.

**API Endpoints**:
- `POST /api/extraction/run` — Run extraction pipeline synchronously
- `POST /api/extraction/trigger` — Trigger extraction in background
- `GET /api/extraction/status/{task_id}` — Check extraction task status (placeholder)
- `GET /api/extraction/health` — Service health check

**Extraction Service** (`api/services/extraction.py`):
- Parses `.p4k` archive files (SC2 mod format from original OAM)
- Creates SQLite databases per category (ships, items, packages, upgrades)
- Deduplicates records across multiple `.p4k` files
- Output: database paths per category

**Usage**:
```bash
# 1. Place .p4k files in a folder
mkdir -p ./legacy_data/p4k
# 2. Run extraction via API
curl -X POST http://localhost:8000/api/extraction/run \\
     -d '{"input_folder": "./legacy_data/p4k", "output_db": "./database", "overwrite": false}'
# 3. Databases created in ./db/ (ships.db, inventory.db, blueprints.db)
# 4. Start app: docker compose up
```

**Extraction Logic** (`api/services/extraction.py`):
- Parses SC2 `.p4k` archive binary format
- Three chunk types: `ship`, `inventory`, `blueprint`
- Creates SQLite databases with proper schemas
- Deduplication across source archives

**CLI Entrypoint** (`extraction.py` `main_cli()`):
- `python -m api.services.extraction /path/to/p4k/folder ./database.db`
- For one-time migration from old OAM data

### Impact on Roadmap

| Roadmap Phase | Docker Impact | Extraction Impact |
|--------------|-------------|-------------------|
| **P1: Google OAuth** | ✅ Docker dev setup complete | ✅ Extraction API ready |
| **P2: RSI Integration** | ✅ Containerized RSI auth | ✅ Extraction ready for data migration |
| **P3: OS Admin Auth** | ✅ keyring in container | ✅ Extraction doesn't interfere |
| **P4: Token Vault Polish** | ✅ Fernet env var in container | ✅ Extraction data can be vaulted |

### Developer Onboarding

New developers can get started in **3 commands**:

```bash
# 1. Clone & deps
git clone ... && cd sc-oam-app
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Start Docker (optional, for containerized dev)
./run.sh

# 3. Run tests
pytest -v
```

### Known Limitations

- SQLite concurrency: Suitable for single-user/standalone mode; upgrade to PostgreSQL for multi-user
- React build: `pnpm run build` in Dockerfile may need Node.js dependencies adjusted per environment
- .p4k format: Parser is simplified; actual SC2 .p4k spec may require updates for full compatibility
- Google OAuth: Requires Google Cloud Console setup (client ID/secret) outside Docker scope

## 🛠️ Development Workflow

### Local Development

```bash
# 1. Backend
python -m venv .venv
source .venv/bin/activate          # macOS/Linux
# .venv\Scripts\activate           # Windows PowerShell

pip install -r requirements.txt
pip install -r requirements-dev.txt

# 3. Environment
cp .env.example .env
# Edit .env if needed

# 4. Start backend
uvicorn app:app --reload           # http://127.0.0.1:8000/docs

# 5. Start frontend (separate terminal)
cd web
npm install                      # First time only
npm run dev                      # http://127.0.0.1:3000
```

### Docker Development

```bash
docker-compose up -d              # Start all services (backend, frontend, db if PostgreSQL)
# Access:
#   - FastAPI: http://localhost:8000/docs
#   - React: http://localhost:3000
#   - Health: http://localhost:8000/health
```

### Testing

```bash
# Backend tests
pytest -v                         # Run all API tests
pytest tests/api/ -v              # Specific API test directory

# Frontend tests
cd web
npm test                          # Run vitest tests

# Lint + format
ruff check .                      # Lint
black --check .                   # Format check
isort --check .                   # Import order check
```

### CI/CD (GitHub Actions)

The `.github/workflows/ci.yml` already configured runs on every PR:

1. **Python matrix** — ruff, black, isort, pytest on Python 3.10/3.11/3.12
2. **Node matrix** — npm install, eslint, vitest on Node 20
3. **Build artifacts** — Python package upload

### Code Review Checklist

| Category | Check |
|----------|-------|
| **Functionality** | Feature works as intended |
| **Style** | Ruff + Black + Isort pass |
| **Types** | TypeScript compiles (`npm run type-check`) |
| **Tests** | All tests pass (`pytest -v` + `npm test`) |
| **Docs** | README, API docs, architecture updated if needed |
| **DB Pluggability** | SQLite default works, PostgreSQL config viable |
| **Security** | No hardcoded secrets, CORS restricted |
| **Commit Messages** | Conventional commits format |
| **Branch Naming** | feature/fix/doc pattern observed |

## 🎯 Novice to Expert Learning Path

### Novice Contributor (First Timers)

1. **Read** `docs/getting-started/overview.md` — 10 minutes
2. **Set up** following `docs/ai-agents/platforms.md` for your OS — 15 minutes
3. **Run** `ruff check . && black . && isort .` — fix any issues — 5 minutes
4. **Run** `pytest -v` + `npm test` — verify all pass — 5 minutes
5. **Pick** a simple issue from `docs/contributing/` — 2 minutes
6. **Create** branch `feature/your-feature-name` — 1 minute
7. **Implement** + **test** + **document** — 30-60 minutes
8. **Open** PR using the template — 2 minutes
9. **Address** feedback — iterate until CI passes — variable
10. **Celebrate** merge! 🎉

### Expert Contributor

1. **Review** full architecture docs in `docs/architecture/`
2. **Propose** RFCs for major design decisions
3. **Optimize** performance, scalability, maintainability
4. **Mentor** newer contributors via PR feedback
5. **Drive** the project vision and roadmap
6. **Evaluate** database migration strategies (SQLite → PostgreSQL)
7. **Plan** release cycles and version numbering

### AI Agent Collaborator

1. **Identify** agent type at prompt start (OpenCode, Claude, Copilot, etc.)
2. **Reference** `docs/ai-agents/identification.md` for context guidelines
3. **Use** platform-specific notes from `docs/ai-agents/platforms.md`
4. **Follow** code style per `docs/contributing/code-style.md`
5. **Maintain** database pluggability — never hardcode SQLite-specific logic
6. **Update** documentation alongside code changes
7. **Request** clarification when scope ambiguous

## 📦 Release History

| Version | Date | Changes |
|---------|------|---------|
| **0.1.0** | 2026-11-12 | Initial scaffold — FastAPI + React + Vite + Tailwind; API routes (blueprints, crafting); database pluggability (SQLite → PostgreSQL); GitHub Actions CI; docs structure |
| **0.1.1** | — | Bug fixes, documentation updates |
| **0.2.0** | — | Full blueprint CRUD + quality calculation; warehouse + hangar API endpoints; Docker Compose setup |
| **1.0.0** | — | Stable release — production-ready with auth, migrations, deployment guides |
| **1.1.0** | — | PostgreSQL-first design; Alembic migrations; advanced UI features |
| **2.0.0** | — | API v2, breaking changes, major refactor (if/when needed) |

Follow [Semantic Versioning](https://semver.org/) (MAJOR.MINOR.PATCH).

## 🆘 Getting Help

| Resource | When to Use |
|----------|-------------|
| **docs/** | Self-service guides, architecture, onboarding |
| **GitHub Issues** | Bug reports, feature requests, questions |
| **GitHub Discussions** | "How do I...", design questions, onboarding help |
| **CI/CD Logs** | Check GitHub Actions for test/lint failures |
| **AI Agents** | Use `docs/ai-agents/` guides for agent-specific help |
| **peers** | Tag specific collaborators `@username` |

---

## 📄 License

MIT License - see LICENSE for details.

---

**sc-oam-app** — Org Asset Manager API & Web UI. Built with FastAPI, React, Vite, and Tailwind CSS. Database pluggable from SQLite to PostgreSQL.
