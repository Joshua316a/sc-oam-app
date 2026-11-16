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

