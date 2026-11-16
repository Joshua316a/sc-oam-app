# Platform-Specific Guidelines — Windows, macOS, Linux

Each operating system has subtle differences in this project. Here's what AI agents need to know.

## 🐍 Python Virtual Environment

| OS | Command to Create | Command to Activate |
|----|------------------|---------------------|
| **macOS / Linux** | `python -m venv .venv` | `source .venv/bin/activate` |
| **Windows CMD** | `python -m venv .venv` | `.venv\Scripts\activate.bat` |
| **Windows PowerShell** | `python -m venv .venv` | `.\.venv\Scripts\Activate.ps1` |
| **WSL (Windows)** | `python -m venv .venv` | `source .venv/bin/activate` |

## 📦 Dependency Installation

| OS | Backend (FastAPI) | Frontend (Node) |
|----|------------------|-----------------|
| **macOS** | `pip install -r requirements.txt` | `npm install` |
| **Linux** | `pip install -r requirements.txt` | `npm install` |
| **Windows PowerShell** | `pip install -r requirements.txt` | `npm install` |
| **WSL** | `pip install -r requirements.txt` | `npm install` |

## 🛠️ Common Commands by OS

### Backend Commands

| OS | Install Deps | Run Server | Run Tests |
|----|-------------|------------|-----------|
| **macOS/Linux** | `pip install -r requirements.txt` | `uvicorn app:app --reload` | `pytest -v` |
| **Windows CMD** | `pip install -r requirements.txt` | `uvicorn app:app --reload` | `pytest -v` |
| **Windows PowerShell** | `pip install -r requirements.txt` | `uvicorn app:app --reload` | `pytest -v` |

### Frontend Commands

| OS | Install Deps | Start Dev | Build |
|----|-------------|-----------|-------|
| **macOS/Linux** | `cd web && npm install` | `npm run dev` | `npm run build` |
| **Windows CMD** | `cd web && npm install` | `npm run dev` | `npm run build` |
| **Windows PowerShell** | `cd web && npm install` | `npm run dev` | `npm run build` |

## 🐳 Docker

| OS | Build | Run |
|----|-------|-----|
| **macOS** | `docker build -t sc-oam-app .` | `docker run -p 8000:8000 -p 3000:3000 sc-oam-app` |
| **Linux** | `docker build -t sc-oam-app .` | `docker run -p 8000:8000 -p 3000:3000 sc-oam-app` |
| **Windows PowerShell** | `docker build -t sc-oam-app .` | `docker run -p 8000:8000 -p 3000:3000 sc-oam-app` |

## 🔧 Platform-Specific Issues

### macOS
- ✅ Default — all development tested here
- ⚠️ `tkinter` may not be available (not used in this project)
- ✅ Homebrew packages generally available
- ✅ Keychain for secret storage (optional)

### Linux (Ubuntu/Debian)
- ✅ `sudo apt-get update && sudo apt-get install -y python3-venv nodejs npm`
- ⚠️ May need `node 20+` via nvm
- ✅ Docker usually works out-of-the-box

### Windows
- ✅ PowerShell recommended over CMD for activate scripts
- ✅ `git bash` works well for all commands
- ⚠️ May need Windows Terminal for best experience
- ✅ WSL2 recommended for Linux-like experience

### WSL (Windows Subsystem for Linux)
- ✅ Best of both worlds: Windows file system + Linux tooling
- Use: `source .venv/bin/activate` (Linux path)
- Node commands work natively
- Docker may need port mapping adjustments

## 📁 Path Conventions

| Convention | Example |
|------------|---------|
| **Forward slashes** | `/Users/colin/Development/sc-oam-app` (all OS) |
| **Backslashes** | `C:\Users\colin\Development\sc-oam-app` (Windows only) |
| **Git paths** | Always use forward slashes in git commands |
| **Python paths** | `./.venv/bin/python` (all OS with venv) |

## 🌐 Port Usage

| Service | Port | Notes |
|---------|------|-------|
| **FastAPI** | 8000 | `uvicorn app:app --reload` |
| **Vite/React** | 3000 | `npm run dev` |
| **Health check** | 8000/health | Returns JSON status |

## 🔄 Cross-OS Workflow

1. **Developer starts on one OS** — follow that OS's setup
2. **Switch OS?** — re-run setup for new OS (virtualenv is OS-specific)
3. **Code is OS-agnostic** — Python/TypeScript runs everywhere
4. **Git repo** — same repo works on all three OS
5. **Docker** — builds uniformly across all OS
