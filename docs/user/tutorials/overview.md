# 📚 Tutorials — sc-oam-app

Step-by-step guides for common tasks. Each tutorial assumes the development server is running at `http://127.0.0.1:8000` (backend) and `http://127.0.0.1:3000` (frontend).

---

## 🎯 Tutorial 1 — Add Your First Blueprint

### Objective
Create a new blueprint entry via the API, then verify it appears in the web UI.

### Prerequisites
- Backend running: `uvicorn app:app --reload`
- Frontend running: `npm run dev` in `web/`

### Step-by-Step

**Step 1 — Create via curl**

```bash
curl -X POST http://127.0.0.1:8000/api/blueprints/ \
  -H "Content-Type: application/json" \
  -d '{"blueprint_id":"bp_fuelpod01","bp_name":"Fuel Pod Blueprint","category":"vehicles","subcategory":"fuel-tanks","craft_type":"fuel-pod","output_item_name":"fuel-pod","quality_min":500.0,"quality_max":700.0,"craft_time_seconds":0.0,"ilg_label":"Vehicles/FuelTanks"}'
# → 201 Created
# → Response includes id, blueprint_id, bp_name, etc.
```

**Step 2 — Verify via the Web UI**
1. Open http://127.0.0.1:3000 in your browser
2. Navigate to the **Blueprints** page (top nav link or go to `/blueprints`)
3. You should see "Fuel Pod Blueprint" in the list/table
4. The blueprint should also appear at http://127.0.0.1:8000/api/blueprints/ (Swagger UI)

### Expected Result
- Blueprint appears in the list with name "Fuel Pod Blueprint"
- Category shows as "vehicles", ILG label as "Vehicles/FuelTanks"
- You can click/edit/delete (depending on UI implementation)

### Troubleshooting
- **Blueprint not showing?** Check the backend terminal for errors; ensure `uvicorn app:app --reload` is running
- **CORS error?** Verify `.env` has `BACKEND_CORS_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"`

---

## 🧪 Tutorial 2 — Calculate Quality for a Blueprint

### Objective
Use the crafting quality API to compute a quality score, then see the result.

### Prerequisites
- Blueprint created from Tutorial 1 (or any blueprint with `blueprint_id=1`)
- Backend running

### Step-by-Step

**Step 1 — Calculate quality via curl**

```bash
curl -X POST http://127.0.0.1:8000/api/crafting/quality \
  -H "Content-Type: application/json" \
  -d '{"blueprint_id":1,"type":"missile","amount":1.0,"count":1,"quality_selector":750.0}'
# → 200 OK
# → Response:
# {
#   "base_quality": 0.75,
#   "resource_qualities": {"missile": 0.75},
#   "resource_weights": {"missile": 1.0},
#   "final_quality": 0.77
# }
```

### Understand the Response

| Field | Meaning | Range |
|-------|---------|-------|
| `base_quality` | `quality_selector / 1000` | 0.0 – 1.0 (here: 750/1000 = 0.75) |
| `resource_qualities` | Per-resource quality (placeholder in v0.1.0) | 0.0 – 1.0 |
| `resource_weights` | Weight/count per resource | 1.0 = one resource of this type |
| `final_quality` | Base + small adjustment | 0.0 – 1.0 (here: 0.77, slightly above base) |

**Step 2 — Verify via the Web UI**
1. Open http://127.0.0.1:3000 and go to the **Crafting** page (`/crafting`)
2. Enter blueprint ID `1`, resource type `missile`, quality selector `750`
3. Click **Calculate Quality**
4. See `base_quality` ≈ 0.75 and `final_quality` ≈ 0.77 displayed

### Expected Result
- Calculator shows base quality and final quality numbers
- Tier badge (Common/Uncommon/etc.) may appear (v0.1.0 has basic display)

### Troubleshooting
- **422 Validation Error?** Check that `quality_selector` is a number ≥ 0; `blueprint_id` exists in the DB
- **Numbers look wrong?** The v0.1.0 calculation is intentionally simple — `final = base + (avg_resource - 500) * 0.1 / 1000`; more complex logic coming in v1.1.0

---

## 🐘 Tutorial 3 — Switch from SQLite to PostgreSQL

### Objective
Change the database backend from the default SQLite (local file) to PostgreSQL (external server), with zero code changes.

### Prerequisites
- Backend running with SQLite (default, from Quick Start)
- PostgreSQL server accessible (Docker: `docker compose up -d db`, or local install)
- Text editor to modify `.env`

### Step-by-Step

**Step 1 — Ensure PostgreSQL is running**

```bash
# If using Docker Compose (included in project)
docker compose up -d db

# Verify it's running
docker compose ps
# → should show the db service with status "Up"
```

**Step 2 — Create the database**

```bash
# If using Docker exec
docker exec -i sc-oam-app-db-1 psql -U oam_user -d sc_oam_db \
  -c "CREATE TABLE IF NOT EXISTS blueprints (id SERIAL PRIMARY KEY, blueprint_id VARCHAR(50) UNIQUE, bp_name VARCHAR(100) NOT NULL, ...)"

# Or locally: createdb sc_oam_db (if PostgreSQL installed natively)
```

**Step 3 — Update `.env`**

```bash
# Before (SQLite - default, already working)
DATABASE_URL="sqlite:///./database.db"

# After (PostgreSQL)
DATABASE_URL="postgresql://oam_user:password@localhost:5432/sc_oam_db"
# Or via Docker: postgresql://oam_user:password@db:5432/sc_oam_db
```

**Step 4 — Apply migrations (Alembic)**

```bash
# From the project root
alembic init migrations   # (one-time, if not already initialized)

# Generate migration from your SQLAlchemy models
alembic revision --autogenerate -m "Initial schema"

# Apply the migration to PostgreSQL
alembic upgrade head
```

**Step 5 — Verify the switch**

```bash
# Health check should still work
curl http://127.0.0.1:8000/api/health
# → {"status":"ok","service":"OAM API","version":"0.1.0"}

# API endpoints now query PostgreSQL
curl http://127.0.0.1:8000/api/blueprints/
# → Previously empty (SQLite had no data), now may show data if you migrated/seeded
```

### Expected Result
- All API endpoints function identically — same URLs, same JSON shapes
- `database.db` file remains untouched (SQLite is read/default; PostgreSQL is now the active backend)
- No code changes required — the `core/database.py` reads `DATABASE_URL` at runtime

### Rollback to SQLite

```bash
# Edit .env back to:
DATABASE_URL="sqlite:///./database.db"

# Restart the backend
# (uvicorn auto-reload will detect the change, or: uvicorn app:app --reload)

# Verify
curl http://127.0.0.1:8000/api/health
# → Still works; data in SQLite is separate from PostgreSQL
```

### Why This Matters
- **Development:** SQLite requires zero setup — `database.db` auto-creates on first run
- **Production/VPS:** PostgreSQL supports concurrent users, larger datasets, and remote access
- **Zero-Downtime Switch:** Change one env var; the same SQLAlchemy models, Pydantic schemas, and FastAPI routes work for both

### Notes
- `alembic` migrations are **PostgreSQL-only** — SQLite auto-creates tables via `Base.metadata.create_all(engine)`; no migration needed for SQLite
- Data in SQLite is **not** automatically migrated to PostgreSQL — you must export/import if you have existing data
- For v0.1.0, SQLite is the default; PostgreSQL is targeted at v1.1.0 multi-user deployment

---
