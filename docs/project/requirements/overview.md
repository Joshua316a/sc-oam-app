# 📋 Requirements — sc-oam-app

Official project requirements document. Defines what the system must do, for whom, and under what constraints.

## 👤 Stakeholders & Users

| Role | Description | Access Level |
|------|-------------|--------------|
| **Primary User** | Org asset manager (single user, self) | Full access — all features, all data |
| **Collaborator** | Feedback provider (limited role) | Read-only — can view, cannot edit/delete |
| **Future Users** | Potential multi-user VPS deployment | Planned — PostgreSQL + auth (v1.1.0+) |

## 🎯 Project Goals

| Goal | Description | Success Criteria |
|------|-------------|------------------|
| **G1: API Separation Layer** | Replace Tkinter UI with FastAPI RESTful endpoints | All CRUD operations for blueprints, crafting, warehouse, hangar accessible via `/api/*` |
| **G2: Database Pluggability** | SQLite (local) → PostgreSQL (VPS/container) without code changes | `DATABASE_URL` env var switches backend; same API models work for both |
| **G3: Modern Web UI** | React + Vite + Tailwind replacement for Tkinter panels | UI renders in browser at `http://127.0.0.1:3000`; matches functionality of existing panels |
| **G4: GitHub Collaboration** | Enable contributor onboarding, PR reviews, CI/CD | `.github/workflows/ci.yml` passes on every PR; `Dependabot` updates deps weekly |
| **G5: Documentation** | Onboard humans + AI agents from Day 1 | `docs/` directory covers identification, platforms, code style, architecture, troubleshooting |
| **G6: Docker Deployment** | Containerized local + production deployment | `docker compose up -d` starts all services; `docker build -t sc-oam-app .` builds image |

## ⚙️ Functional Requirements

| ID | Requirement | Priority | Description |
|----|-----------|----------|-------------|
| **FR-001** | Blueprint CRUD | High | Create, read, update, delete blueprints via `/api/blueprints/` |
| **FR-002** | Quality Calculation | High | POST `/api/crafting/quality` returns base/final quality given resource qualities |
| **FR-003** | Warehouse Inventory | Medium | GET `/api/warehouse/` lists items in player_inventory; supports add/edit/delete |
| **FR-004** | Fleet Management | Medium | GET `/api/hangar/` lists player-owned ships; supports add/edit/delete |
| **FR-005** | Health Check | High | GET `/api/health` returns `{status: "ok", service: "OAM API", version: "0.1.0"}` |
| **FR-006** | Database Pluggability | High | `DATABASE_URL="sqlite:///./database.db"` (default) or PostgreSQL URL; zero code changes |
| **FR-007** | CORS Configuration | Medium | `BACKEND_CORS_ORIGINS` from `.env`; default allows `localhost:3000` |
| **FR-008** | Error Responses | Medium | All errors return `{detail: "..."}` per FastAPI convention; 422 for validation, 404 for not found |
| **FR-009** | API Versioning (planned) | Low | `/api/v1/blueprints/` — add when breaking changes necessary; not for v0.1.0 |
| **FR-010** | Search/Filtering | Medium | Blueprints support `?category=weapons&?ilg_label=Weapons/Missiles` query params |

## 🗄️ Non-Functional Requirements

| ID | Requirement | Priority | Description |
|----|-----------|----------|-------------|
| **NFR-001** | Database Pluggability | High | Same SQLAlchemy models work with SQLite (dev) or PostgreSQL (prod) via `DATABASE_URL` |
| **NFR-002** | API Consistency | High | All endpoints follow FastAPI conventions; Pydantic schemas validate input/output |
| **NFR-003** | Type Safety | High | Full TypeScript on frontend matching Python Pydantic schemas; `npm run type-check` passes |
| **NFR-004** | Code Quality | High | `ruff check .`, `black --check .`, `isort --check .` all pass; CI enforces this |
| **NFR-005** | Test Coverage | Medium | `pytest -v` passes for API; `npm test` passes for frontend; CI checks both |
| **NFR-006** | Docker Compatibility | High | `docker compose up -d` starts backend + frontend + db; both development and production configs |
| **NFR-007** | Responsiveness | Medium | Web UI adapts from 320px (mobile) to 1440px+ (desktop) via Tailwind breakpoints |
| **NFR-008** | Performance | Medium | API response < 500ms for CRUD operations with < 1000 records; quality calc < 100ms |
| **NFR-009** | Security Baseline | Medium | No hardcoded secrets (`.env` + `.gitignore`); CORS restricted to known origins in prod |
| **NFR-010** | Accessibility | Low | WCAG AA color contrast; keyboard-navitable form controls; add when UI is feature-complete |

## 📦 Out of Scope (v0.1.0)

| Item | Reason |
|------|--------|
| **O1: Multi-user authentication** | Planned for v1.1.0 with PostgreSQL; adds complexity for single-user v0.1.0 |
| **O2: Advanced reporting/analytics** | Can be added later; data already in database; export via CSV is sufficient for now |
| **O3: Drag-and-drop blueprint editing** | Keyboard+form editing is sufficient; drag-drop can be v1.2.0 feature |
| **O4: Real-time collaboration** | Single-user scope; multi-user requires auth + conflict resolution (v1.1.0+) |
| **O5: Custom themes / branding** | Default Tailwind theme is sufficient for v0.1.0; theming can be v1.2.0 |
| **O5: Mobile-specific UI** | Responsive design covers mobile; dedicated mobile app is future consideration |
| **O6: Export/import JSON/CSV** | Basic API data handling is sufficient; can add endpoints later |

## 🔒 Constraints & Assumptions

| Constraint | Detail |
|------------|--------|
| **C1: Single primary user** | This is the sole developer and user; collaborator has read-only feedback role |
| **C2: Python 3.10+ only** | Leverages modern type hints, `dict` union syntax, etc. |
| **C3: Node.js 20+ only** | Leverages modern JS features, ESM, updated tooling |
| **C4: SQLite default, PostgreSQL optional** | Zero-code-change switch; SQLite for local dev, PostgreSQL for production |
| **C5: No external APIs beyond SC data** | Uses existing `modules/data_access.py` logic; no third-party API dependencies beyond what's already in the codebase |
| **C6: GitHub Actions on ubuntu-latest** | CI configured for Ubuntu; may need adjustment for Windows Server or macOS runners |
| **C7: MIT license** | Chosen for maximum flexibility; must-have for GitHub open-source features |
| **C8: v0.1.0 = scaffold + basic CRUD** | Full feature set planned across v0.1.0 → v1.0.0 → v2.0.0 roadmap |

## 📅 Version & Status

| Field | Value |
|-------|-------|
| **Document Version** | v1.0.0 — 2026-11-12 |
| **Status** | ✅ Finalized — requirements baseline |
| **Owner** | Primary user (self-documenting) |
| **Review Cycle** | Review before each major milestone (v0.1.0 complete, v0.2.0 start) |
| **Related Docs** | `docs/architecture/overview.md` (design), `docs/project/hld/overview.md` (high-level design), `docs/project/lld/overview.md` (low-level specs) |

## 🔗 Cross-References

| Document | Relationship |
|----------|-------------|
| `docs/project/architecture/overview.md` | Translates requirements into system architecture |
| `docs/project/hld/overview.md` | Breaks architecture into subsystems/components |
| `docs/project/lld/overview.md` | Detailed specs for each module/function |
| `docs/getting-started/overview.md` | Maps requirements to onboarding steps for new collaborators |
| `docs/ai-agents/tools-services-cheatsheet.md` | Maps requirements to required tools/services |
| `pyproject.toml` | Technical reflection of requirements (dependencies, scripts) |
| `requirements.txt` | Runtime deps aligned with FR-001 through FR-010 |

---
