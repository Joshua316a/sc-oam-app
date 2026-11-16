# 🛠️ Development Environment Cheat Sheet

A consolidated reference of all tools, skills, and services required for the sc-oam-app project, with installation sources and quick configuration commands.

---

## 🐍 Python Environment

| Tool | Purpose | Install Source | Configure/Verify |
|------|---------|---------------|------------------|
| **Python 3.10+** | Runtime for FastAPI backend | <https://python.org> | `python3 --version` → must be 3.10, 3.11, or 3.12 |
| **venv** | Virtual environment (built-in) | Included with Python | `python3 -m venv .venv` then activate:<br>• macOS/Linux: `source .venv/bin/activate`<br>• Windows PowerShell: `.\.venv\Scripts\Activate.ps1` |
| **pip** | Python package manager | Included with Python | `pip --version` |
| **ruff** | Linter + formatter (fast) | `pip install ruff` | `ruff --version`<br>→ `ruff check .` / `ruff check . --fix` |
| **black** | Python formatter | `pip install black` | `black --version`<br>→ `black --check .` / `black .` |
| **isort** | Import order manager | `pip install isort` | `isort --version`<br>→ `isort --check .` / `isort .` |
| **pyproject.toml** | Project config (ruff, black, pytest) | Project root | Already configured — see `pyproject.toml` |
| **requirements.txt** | Runtime dependencies | Project root | `pip install -r requirements.txt` |
| **requirements-dev.txt** | Dev dependencies | Project root | `pip install -r requirements-dev.txt` |
| **pytest** | Testing framework | `pip install pytest` | `pytest --version`<br>→ `pytest -v` / `pytest tests/api/` |
| **python-dotenv** | Env variable loading | `pip install python-dotenv` | Included in `requirements.txt` |

### `.env` Configuration

```env
# Copy from .env.example
cp .env.example .env

# Required variables
DATABASE_URL="sqlite:///./database.db"          # or PostgreSQL URL
SECRET_KEY="your-256-bit-secret"              # 32+ chars minimum
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=True                                    # False for production
BACKEND_CORS_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"
```

### Verify Python Setup

```bash
python3 --version                              # 3.10+, e.g., 3.12.0
pip --version                                  # e.g., 23.1.2
ruff --version                                 # e.g., 0.4.0
black --version                                # e.g., 23.0.0
isort --version                                # e.g., 5.12.0
pytest --version                               # e.g., 7.4.0
```

---

## ⚛️ Node.js / React Environment

| Tool | Purpose | Install Source | Configure/Verify |
|------|---------|---------------|------------------|
| **Node.js 20+** | JavaScript runtime | <https://nodejs.org> | `node --version` → should be v20.x or v21.x |
| **npm** | Node package manager | Included with Node | `npm --version` → should be 10.x+ |
| **Vite** | Build tool + dev server | `npm install -g vite` (optional) | `vite --version`<br>→ Use `npx vite` or project-local `npm run dev` |
| **npm** | Install dependencies | Included with Node | `npm install` / `npm ci` |
| **Tailwind CSS** | Utility-first CSS framework | `npm install -D tailwindcss postcss autoprefixer` | Project: `web/tailwind.config.js` + `web/postcss.config.js` |
| **PostCSS** | CSS processing | Included in Tailwind install | `npx tailwindcss -i input.css -o output.css` (handled by Vite) |
| **TypeScript** | Type safety | `npm install -D typescript` | `npx tsc --version`<br>→ `npm run type-check` |
| **ESLint** | JS/TS linting | `npm install -D eslint eslint-plugin-react` | `npx eslint --version`<br>→ `npm run lint` |
| **React 18+** | UI library | `npm install react react-dom` | Included in `web/package.json` |
| **react-router-dom** | Routing | `npm install react-router-dom` | Included in `web/package.json` |
| **Vite React Plugin** | JSX support | `npm install -D @vitejs/plugin-react` | Included in `web/package.json` |

### Verify Node Setup

```bash
node --version                                  # v20.x.x, v21.x.x
npm --version                                   # 10.x.x or later
npx vite --version                              # e.g., 5.3.1
npx tsc --version                               # e.g., 5.5.2
npx eslint --version                            # e.g., 8.57.0
```

### Frontend Commands Cheat Sheet

| Action | Command | Directory |
|--------|---------|-----------|
| **Install deps** | `npm install` | `web/` |
| **First-time install** | `npm ci` | `web/` |
| **Start dev server** | `npm run dev` | `web/` |
| **Build for production** | `npm run build` | `web/` |
| **Preview build** | `npm run preview` | `web/` |
| **Run lint** | `npm run lint` | `web/` |
| **Type check** | `npm run type-check` | `web/` |

---

## 🐳 Docker / Container Environment

| Tool | Purpose | Install Source | Configure/Verify |
|------|---------|---------------|------------------|
| **Docker Desktop** | Container engine + UI | <https://docker.com> | Open Docker Desktop → verify "Docker is running" |
| **Docker CLI** | Container commands | Included with Docker Desktop | `docker --version`<br>→ `docker --help` |
| **Docker Compose** | Multi-container orchestrator | Included with Docker Desktop v2+ | `docker compose --version` |
| **Dockerfile** | Build instructions | Project root | `docker build -t sc-oam-app .` |
| **docker-compose.yml** | Local dev orchestration | Project root | See `docs/deployment/docker.md` |

### Docker Commands Cheat Sheet

| Action | Command | Description |
|--------|---------|-------------|
| **Build image** | `docker build -t sc-oam-app .` | From project root |
| **Run dev** | `docker run -d -p 8000:8000 -p 3000:3000 sc-oam-app` | Start both backend + frontend |
| **Docker Compose up** | `docker compose up -d` | Start all services (backend, frontend, db) |
| **Docker Compose down** | `docker compose down` | Stop all services |
| **View logs** | `docker compose logs -f` | Follow all service logs |
| **Exec into container** | `docker compose exec backend sh` | Shell into running container |
| **Prune everything** | `docker system prune -a` | Remove unused images, networks, volumes |

### Docker Compose Quick Start

```bash
# From project root
docker compose up -d              # Start all services (backend, frontend, PostgreSQL DB)
# Access:
#   - FastAPI + docs: http://localhost:8000/docs
#   - React dev: http://localhost:3000
#   - Health check: http://localhost:8000/health

# When done
docker compose down               # Stop and remove containers
```

---

## 🌐 Git / GitHub Environment

| Tool | Purpose | Install Source | Configure/Verify |
|------|---------|---------------|------------------|
| **Git** | Version control | <https://git-scm.com> | `git --version` → e.g., 2.40.0+ |
| **GitHub CLI** | GitHub from terminal | <https://github.com/cli> | `gh --version`<br>→ `gh auth login` |
| **GitHub Account** | Remote repo, CI, issues | <https://github.com> | Create account, accept invitation to org/repo |
| **.gitignore** | Exclude files from version control | Project root | Already configured — see `.gitignore` |
| **Git Configuration** | User identity | Global or repo-local | `git config user.name "Your Name"`<br>`git config user.email "you@example.com"` |
| **GitHub Actions** | CI/CD automation | Automatic via `.github/workflows/` | CI runs on every PR: lint + test on Python + Node matrices |
| **Dependabot** | Automated dependency updates | Automatic via `.github/dependabot.yml` | PRs opened weekly for outdated deps |
| **CODEOWNERS** | Review assignation | `.github/CODEOWNERS` (planned) | Assign specific reviewers per file pattern |

### Git Configuration Quick Start

```bash
# Set identity (do once globally)
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# Verify
git config --list --global

# Set up SSH key for GitHub (optional, for push without password)
ssh-keygen -t ed25519 -C "you@example.com"
cat ~/.ssh/id_ed25519.pub  # Copy output to GitHub: Settings → SSH Keys → New SSH key
```

### Git Daily Commands

```bash
# Clone repo
git clone https://github.com/your-org/sc-oam-app.git
cd sc-oam-app

# Create feature branch
git checkout -b feature/blueprint-crud

# Work, commit
git add .
git commit -m "feat(blueprints): add create endpoint"

# Push and PR
git push origin feature/blueprint-crud
# Then open PR on GitHub web interface
```

### GitHub Actions CI Triggers

| Event | When CI Runs |
|-------|-------------|
| `push` | On `main` and `develop` branches |
| `pull_request` | On `main` and `develop` branches |
| `schedule` | (not currently configured) |
| `workflow_dispatch` | Manual trigger from Actions tab |

### CI Checks Performed

| Check | Tool | Matrix |
|-------|------|--------|
| **Python ruff lint** | `ruff check .` | Python 3.10, 3.11, 3.12 |
| **Python black check** | `black --check .` | Python 3.10, 3.11, 3.12 |
| **Python pytest** | `pytest -v` | Python 3.10, 3.11, 3.12 |
| **Node npm install** | `npm ci` | Node 20 |
| **Node eslint** | `npm run lint` | Node 20 |
| **Node type-check** | `npm run type-check` | Node 20 |
| **Build artifacts** | `python -m build` | Python 3.10, 3.11, 3.12 |

---

## 💡 IDE / Editor Recommendations

| Editor | AI Agent Support | Cost | Why Useful for sc-oam-app |
|--------|-----------------|------|---------------------------|
| **VS Code** | ✅ Excellent (Copilot, debugger) | Free / Pro | Best all-rounder; `code .` opens project; extensions: Python, Tailwind CSS, ESLint |
| **Cursor** | ✅ Built-in AI | Paid | AI-first editor; chat + inline suggestions |
| **OpenCode (Claude Code)** | ✅ Native (skills/tools) | Free (session) | This environment; `skill`, `tool`, `codegraph` commands |
| **WebStorm** | ✅ Good JavaScript support | Paid | Strong TypeScript/React debugging |
| **Vim/Emacs** | ⚠️ Manual setup | Free | For power users; requires plugin configuration |

### VS Code Extensions (Recommended)

| Extension | Purpose |
|-----------|---------|
| `python.python` | Python language support |
| `ms-python.vscode-pylance` | Type checking, autocompletion |
| `ruff.ruff` | Fast linting (same as `ruff` CLI) |
| `esbenp.prettier-vscode` | Formatting (compatible with Black) |
- `tailwindcss.tailwindcss` | IntelliSense for Tailwind classes |
- `esbenp.vite` | Vite project recognition |
- `GitHub.vscode-github-actions` | CI/CD workflow preview |

---

## 🗄️ Database Tools

| Tool | Purpose | Install Source | Configure/Verify |
|------|---------|---------------|------------------|
| **SQLite** | Embedded database (default) | Built into Python | `import sqlite3` → no install needed |
| **pgAdmin 4** | PostgreSQL GUI | <https://www.pgadmin.org> | Connect to `DATABASE_URL` PostgreSQL host |
| **psql** | PostgreSQL CLI | Included with PostgreSQL/Docker | `psql --version`<br>→ `psql "postgresql://..."` |
| **DBeaver** | Multi-database GUI | <https://dbeaver.io> | Free Community Edition; connect to both SQLite + PostgreSQL |
| **Alembic** | Database migrations | `alembic init migrations` | `alembic version`<br>→ `alembic upgrade head` |

### SQLite Quick Verification

```bash
# Already included with Python
python3 -c "import sqlite3; print('SQLite OK')"

# Create/verify database
python3 -c "
import sqlite3
conn = sqlite3.connect('./database.db')
cursor = conn.cursor()
cursor.execute('SELECT 1')
print('Database created and accessible:', cursor.fetchone())
conn.close()
"
```

### PostgreSQL Quick Start (Docker)

```bash
# Start PostgreSQL via Docker Compose (included in project)
docker compose up -d db

# Verify it's running
docker compose ps

# Connect via psql
docker exec -it sc-oam-app-db-1 psql -U oam_user -d sc_oam_db -c "\dt"

# Or via pgAdmin: connect to host=localhost, port=5432, database=sc_oam_db, user=oam_user
```

---

## 🔍 Verification Checklist — New Session Setup

Run this sequence when starting a fresh development session:

```bash
# 1. Verify OS and Python
echo "=== OS ===" && uname -a || ver
echo "=== Python ===" && python3 --version
echo "=== pip ===" && pip --version

# 2. Create and activate venv
python3 -m venv .venv
source .venv/bin/activate          # macOS/Linux
# .venv\Scripts\activate           # Windows PowerShell

# 3. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your settings

# 5. Verify tooling
echo "=== Tool Versions ===" && \
  ruff --version && \
  black --version && \
  isort --version && \
  pytest --version && \
  node --version && \
  npm --version && \
  docker --version

# 6. Run lint + format check
ruff check . && black --check . && isort --check . && echo "✓ Style OK"

# 7. Run tests
pytest -v && echo "✓ Tests OK"

# 8. Start services
# Backend: uvicorn app:app --reload
# Frontend: cd web && npm run dev
```

---

## 📦 Where to Get Everything — Quick Links

| Category | Primary Source |
|----------|----------------|
| **Python 3.10+** | <https://python.org> (download → "Install Python") |
| **Node.js 20+** | <https://nodejs.org> (LTS version) |
| **Git** | <https://git-scm.com> (download or package manager: `brew install git`, `apt-get install git`) |
| **Docker Desktop** | <https://docker.com> (Docker Desktop for Mac/Windows, or Docker Engine for Linux) |
| **GitHub Account** | <https://github.com> (free tier sufficient) |
| **PostgreSQL** | <https://www.postgresql.org> (or use Docker + `postgres:15` image) |
| **VS Code** | <https://code.visualstudio.com> (free) |
| **pip packages** | `pip install <pkg>` (all listed in `requirements.txt` / `requirements-dev.txt`) |

---

## 🎯 Agent-Specific Tool Notes

### OpenCode (This Environment)
- **Skills**: `session-startup`, `codegraph_explore`, `gitnexus_impact`, `pre-release-validation`
- **Tools**: `ruff`, `black`, `isort`, `pytest` (already installed in session)
- **Codegraph**: Indexed project — `codegraph_explore "<query>"` for code intelligence
- **GitNexus**: `gitnexus_impact(target="symbolName")` for blast radius before edits

### Claude Code
- **Preferred IDE**: VS Code or Claude's native editor
- **Context**: Paste `docs/ai-agents/identification.md` + `docs/ai-agents/platforms.md` for full context
- **Commands**: Natural language queries; agent auto-identifies from prompt

### Copilot / Cursor
- **Setup**: Install extensions, enable inline suggestions
- **Context**: Reference `.cursorrules` if present, or project `README.md` + `docs/`
- **Workflow**: Chat for design/architecture, inline for boilerplate

---

## 🆘 Quick Reference — When Something Fails

| Problem | Likely Fix |
|---------|------------|
| `command not found: python` | Ensure Python 3.10+ installed and in PATH |
| `command not found: node` | Install Node.js 20+ from nodejs.org |
| `ruff: command not found` | `pip install ruff` inside venv |
| `black: command not found` | `pip install black` inside venv |
| `pytest not found` | `pip install pytest` inside venv |
| `docker: permission denied` | Add user to docker group, or use `sudo docker` |
| `EACCES: permission error` | `npm config set prefix '$HOME/.npm-global'` then `npx` commands |
| `port 8000 already in use` | Kill existing process: `lsof -i :8000` then `kill <PID>` or change port |
| `npm ERR! code ENOENT` | `cd web && npm install` (run from correct directory) |
| `psql: command not found` | Install PostgreSQL CLI or use Docker: `docker compose up -d db` |
| `404 Not Found: /api/blueprints/` | Ensure backend running: `uvicorn app:app --reload` and visit `/docs` |

---

## 📄 Cheat Sheet Summary — One-Liners

| Task | One-Liner Command |
|------|------------------|
| **Start dev session** | `source session-startup` (or run health check inline) |
| **Create venv** | `python3 -m venv .venv && source .venv/bin/activate` |
| **Install deps** | `pip install -r requirements.txt && pip install -r requirements-dev.txt` |
| **Check style** | `ruff check . && black --check . && isort --check .` |
| **Run tests** | `pytest -v` |
| **Start backend** | `uvicorn app:app --reload` (http://127.0.0.1:8000/docs) |
| **Start frontend** | `cd web && npm run dev` (http://127.0.0.1:3000) |
| **Docker up** | `docker compose up -d` (http://localhost:8000/docs + http://localhost:3000) |
| **Docker down** | `docker compose down` |
| **Git branch** | `git checkout -b feature/name` then `git push origin feature/name` |
| **GitHub PR** | Push branch, then use GitHub web → New Pull Request |
| **Type check** | `npm run type-check` (in `web/`) |
| **Lint+format** | `ruff check . && black . && isort .` (fixes auto) |

---
