# � User Guide — sc-oam-app

Welcome to the Org Asset Manager API & Web UI. This guide helps you get up and running, whether you're a human using the web interface or a developer calling the REST API.

---

## 🏁 Quick Start — 5 Minutes to Running

### Prerequisites
- [Python 3.10+](https://python.org)
- [Node.js 18+](https://nodejs.org)
- [Git](https://git-scm.com)

### macOS / Linux

```bash
# 1. Clone the repository
git clone https://github.com/your-org/sc-oam-app.git
cd sc-oam-app

# 2. Backend (FastAPI)
python -m venv .venv
source .venv/bin/activate          # macOS/Linux
# .venv\Scripts\activate           # Windows PowerShell

pip install -r requirements.txt
pip install -r requirements-dev.txt

cp .env.example .env
# The default DATABASE_URL uses SQLite — no further DB setup needed for local dev

# 3. Run the backend
uvicorn app:app --reload
# Visit: http://127.0.0.1:8000/docs (auto-generated interactive API docs)

# 4. Frontend (React + Vite) — separate terminal
cd web
npm install          # First time only
npm run dev
# Visit: http://127.0.0.1:3000 (React development server)
```

### Windows

```powershell
# 1. Clone the repository
git clone https://github.com/your-org/sc-oam-app.git
cd sc-oam-app

# 2. Backend
python -m venv .venv
.\.venv\Scripts\activate

pip install -r requirements.txt
pip install -r requirements-dev.txt

copy .env.example .env
# Default uses SQLite — no extra DB setup

# 3. Run backend
uvicorn app:app --reload
# Visit: http://127.0.0.1:8000/docs

# 4. Run frontend
cd web
npm install
npm run dev
# Visit: http://127.0.0.1:3000
```

### 🔑 Default Login & Access

| Access Method | URL | Notes |
|---------------|-----|-------|
| **FastAPI Docs (Swagger UI)** | http://127.0.0.1:8000/docs | Interactive API exploration; test endpoints directly |
| **React UI** | http://127.0.0.1:3000 | Blueprints, Crafting, Warehouse, Dashboard pages |
| **Health Check** | http://127.0.0.1:8000/health | Returns `{status: "ok", service: "OAM API", version: "0.1.0"}` |
| **ReDoc (API docs)** | http://127.0.0.1:8000/redoc | Alternative, markdown-styled API reference |

### 📡 API Quick Test — curl Examples

```bash
# Health check
curl http://127.0.0.1:8000/api/health
# → {"status":"ok","service":"OAM API","version":"0.1.0"}

# List blueprints (empty at start)
curl http://127.0.0.1:8000/api/blueprints/
# → []

# Create a blueprint
curl -X POST http://127.0.0.1:8000/api/blueprints/ \
  -H "Content-Type: application/json" \
  -d '{"blueprint_id":"bp_001","bp_name":"Tactical Missile BP","category":"weapons","subcategory":"missiles","craft_type":"missile","output_item_name":"missile","quality_min":500.0,"quality_max":800.0,"craft_time_seconds":30.0,"ilg_label":"Weapons/Missiles"}'
# → 201 Created with full blueprint object

# Check created blueprint
curl http://127.0.0.1:8000/api/blueprints/1
```

### 📦 Production Deployment

| Method | Command | Description |
|--------|---------|-------------|
| **Docker (dev)** | `docker compose up -d` | Starts backend + frontend + (optional) PostgreSQL |
| **Docker (prod)** | `docker build -t sc-oam-app . && docker run -d -p 80:8000 -e ENVIRONMENT=production -e DATABASE_URL="postgresql://..." sc-oam-app` | Full production container |
| **Manual** | `uvicorn app:app --reload` + `npm run build` + serve `web/dist/` | Do-it-yourself deployment |

---
