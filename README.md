# sc-oam-app

**Org Asset Manager API & Web UI** — A modern, API-first replacement for the Org Asset Manager (OAM) Tkinter-based application.

Built with **FastAPI** for the backend and **React + Vite + Tailwind** for the frontend.

---
<a href="docs/getting-started/overview.md">▶️ Getting Started</a> ·
<a href="docs/contributing/overview.md">👥 Contributing</a> ·
<a href="docs/ai-agents/overview.md">🤖 AI Agent Onboarding</a> ·
<a href="docs/api-reference/overview.md">🔌 API Reference</a> ·
<a href="docs/troubleshooting/overview.md">🔧 Troubleshooting</a> ·
<a href="docs/deployment/overview.md">📦 Deployment</a> ·
<a href="docs/architecture/overview.md">🏗️ Architecture</a>

---

## 🎯 What Is This Project?

sc-oam-app is a complete rewrite of the Org Asset Manager, moving from a Tkinter-based desktop application to a modern **API separation layer + Web UI** architecture.

| Aspect | Description |
|--------|-------------|
| **Purpose** | Manage Star Citizen org assets: blueprints, crafting, warehouse inventory, hangar fleet |
| **Architecture** | FastAPI backend + React/Vite/Tailwind frontend |
| **Database** | SQLite (default) → PostgreSQL (plug-and-play) |
| **Target** | Single-user local development → Multi-user VPS deployment |
| **License** | MIT |

---

## 🏁 Quick Start — 5 Minutes to Running

### Prerequisites
- [Python 3.10+](https://python.org)
- [Node.js 18+](https://nodejs.org)
- [Git](https://git-scm.com)

### macOS / Linux

```bash
# 1. Clone & enter project
git clone https://github.com/your-org/sc-oam-app.git
cd sc-oam-app

# 2. Backend setup
python -m venv .venv
source .venv/bin/activate          # Linux/macOS
# .venv\Scripts\activate           # Windows PowerShell

pip install -r requirements.txt
pip install -r requirements-dev.txt

cp .env.example .env
# Edit .env if needed (DB_URL, SECRET_KEY, etc.)

# 3. Run backend
uvicorn app:app --reload          # Visit: http://127.0.0.1:8000/docs
```



### Feature Overview (v1.1.0-planned)

sc-oam-app will feature a three-tier authentication system:

| Feature | Description |
|---------|-------------|
| **Google OAuth** | Primary user authentication via "Login with Google" |
| **RSI Integration** | Access pledge hangar data via PyRSI library |
| **OS Keychain** | Admin/power user operations with OS-native storage |

### macOS / Linux

```bash
# 1. Clone & enter project
git clone https://github.com/your-org/sc-oam-app.git
cd sc-oam-app

# 2. Backend setup
python -m venv .venv
source .venv/bin/activate          # Linux/macOS

pip install -r requirements.txt
pip install -r requirements-dev.txt

cp .env.example .env
# Edit .env if needed (add GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)

# 3. Run backend
uvicorn app:app --reload          # Visit: http://127.0.0.1:8000/docs
```

### Windows

```powershell
# 1. Clone & enter project
git clone https://github.com/your-org/sc-oam-app.git
cd sc-oam-app

# 2. Backend setup
python -m venv .venv
\.venv\Scripts\activate

pip install -r requirements.txt
pip install -r requirements-dev.txt

copy .env.example .env
# Edit .env if needed
```

### Frontend (all OS)

```bash
# In a separate terminal
cd web
npm install          # Install dependencies
npm run dev          # Visit: http://127.0.0.1:3000
```

### Verify It Works

| Service | URL |
|---------|-----|
| **FastAPI docs** | http://127.0.0.1:8000/docs |
| **React dev server** | http://127.0.0.1:3000 |
| **Health check** | http://127.0.0.1:8000/health |

### Docker + Extraction (v1.1.0-planned)

 sc-oam-app can be run as a single Docker container bundling the FastAPI backend, React frontend, and SQLite database. 

**Quick Start with Docker:**
```bash
# 1. Customize .env
cp .env.example .env
# Edit .env (DATABASE_URL, SECRET_KEY, etc.)

# 2. Launch via Docker
./run.sh

# 3. Access the app
#   - FastAPI docs: http://localhost:8000/docs
#   - React dev server: http://localhost:3000

#  • Data persists in ./db/ folder on this host

### Extraction Pipeline (Data.p4k → Reference DB)

sc-oam-app provides an extraction pipeline to migrate legacy Tkinter OAM game data (`.p4k` archives) into reference SQLite databases.

**API Endpoints**:
- `POST /api/extraction/run` — Run extraction synchronously
- `POST /api/extraction/trigger` — Trigger extraction in background

**Extraction Service** (`api/services/extraction.py`):
- Parses `.p4k` archive files (SC2 mod format from original OAM)
- Creates SQLite databases per category (ships, inventory, blueprints)
- Deduplicates records across multiple `.p4k` files

**Usage**:
1. Place `.p4k` files in a folder
2. Run `./run.sh` to start the app
3. Call `POST /api/extraction/run` to migrate legacy data
4. Databases appear in `./db/` folder

**CLI**:
```bash
python -m api.services.extraction /path/to/p4k/folder ./database.db
'''
## 👥 For Human Collaborators

| Topic | Documentation |
|-------|---------------|
| **Getting started** | `docs/getting-started/overview.md` |
| **Contributing guidelines** | `docs/contributing/overview.md` |
| **Code style** | `docs/contributing/code-style.md` |
| **Pull request process** | `docs/contributing/pr-workflow.md` |
| **Database migration** | `docs/contributing/database.md` |
| **Branch naming** | `docs/contributing/branching.md` |

---

## 🤖 For AI Coding Agents (OpenCode, Claude, Copilot, etc.)

| Topic | Documentation |
|-------|---------------|
| **Agent identification** | `docs/ai-agents/identification.md` |
| **Platform-specific commands** | `docs/ai-agents/platforms.md` |
| **Context injection** | `docs/ai-agents/context.md` |
| **Tool usage guidelines** | `docs/ai-agents/tools.md` |
| **Common patterns** | `docs/ai-agents/patterns.md` |
| **Agent memory management** | `docs/ai-agents/memory.md` |

---

## 🔌 API Reference

| Category | Documentation |
|----------|---------------|
| **Blueprint endpoints** | `docs/api-reference/blueprints.md` |
| **Crafting endpoints** | `docs/api-reference/crafting.md` |
| **Warehouse endpoints** | `docs/api-reference/warehouse.md` |
| **Hangar endpoints** | `docs/api-reference/hangar.md` |
| **Data models** | `docs/api-reference/models.md` |
| **OpenAPI spec** | `/docs` (when server running) |

---

## 🔧 Troubleshooting

| Issue | Documentation |
|-------|---------------|
| **Tkinter vs Web confusion** | `docs/troubleshooting/platform-fix.md` |
| **Database connection errors** | `docs/troubleshooting/db-fix.md` |
| **CORS issues** | `docs/troubleshooting/cors-fix.md` |
| **Node/Vite errors** | `docs/troubleshooting/node-fix.md` |
| **Port conflicts** | `docs/troubleshooting/port-fix.md` |

---

## 📦 Deployment

| Target | Documentation |
|--------|---------------|
| **Local development** | `docs/development/overview.md` |
| **Docker container** | `docs/deployment/docker.md` |
| **VPS/PythonAnywhere** | `docs/deployment/vps.md` |
| **GitHub Pages** | `docs/deployment/github-pages.md` |

---

## 🏗️ Architecture

| Layer | Documentation |
|-------|---------------|
| **Backend** | `docs/architecture/backend.md` |
| **Frontend** | `docs/architecture/frontend.md` |
| **Database schema** | `docs/architecture/database.md` |
| **API design** | `docs/architecture/api-design.md` |
| **Deployment pipeline** | `docs/architecture/pipeline.md` |

---

## 📄 License

MIT License - see LICENSE for details.

---

## 📞 Contact & Support

- **Issues:** [GitHub Issues](https://github.com/your-org/sc-oam-app/issues)
- **Discussions:** [GitHub Discussions](https://github.com/your-org/sc-oam-app/discussions)
- **Email:** your-email@example.com
