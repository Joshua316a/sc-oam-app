# 🛠️ Troubleshooting — sc-oam-app

Common issues and solutions for the sc-oam-app project. Covers backend, frontend, Docker, and environment problems.

---

## 🐍 Python / Backend Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `uvicorn: command not found` | Virtualenv not activated | Activate: `source .venv/bin/activate` (macOS/Linux) or `.\.venv\Scripts\activate.bat` (Windows) |
| `ModuleNotFoundError: No module named 'fastapi'` | Dependencies not installed | `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'uvicorn[standard]'` | Incomplete install | `pip install "uvicorn[standard]"` |
| `pytest not found` | Dev deps not installed | `pip install -r requirements-dev.txt` |
| `ImportError: cannot import name 'XXX'` | Wrong Python version | Use Python 3.10+ (`python3 --version`) |
| `sqlite3.OperationalError: unable to open database file` | DB path wrong or permissions | Check `.env` DATABASE_URL; ensure directory is writable |
| `sqlite3.OperationalError: database is locked` | Another process reading/writing | Add `?timeout=30` to SQLite URL in `.env`; reduce concurrent writes |
| `422 Validation Error` | Request body doesn't match Pydantic model | Check JSON fields match `api/schemas/blueprints.py` (e.g., `blueprint_id`, `bp_name`, `quality_min`, `quality_max`, `ilg_label` required) |
| `500 Internal Server Error` | Server-side error | Check server terminal for traceback; ensure `DEBUG=True` in `.env` for details |
| `CORS policy blocks request` | Frontend origin not in CORS allowlist | Edit `.env`: `BACKEND_CORS_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"`; restart backend |

### `.env` Quick Fixes

```env
# Common tweaks
DATABASE_URL="sqlite:///./database.db"          # Default; or PostgreSQL URL
SECRET_KEY="change-this-to-a-random-secret"   # Must be 32+ chars for production
DEBUG=True                                      # False for production; shows detailed errors
BACKEND_CORS_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"  # Add prod origins
```

---

## 🐳 Docker Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `docker: command not found` | Docker Desktop not installed/running | Install Docker Desktop; ensure "Docker is running" |
| `Build failed` | Python/Node deps issue in Dockerfile | Check `Dockerfile` for correct base image (`python:3.10-slim` + `node:20` stages) |
| `Port 3000 already in use` | Another process on port 3000 | Kill it: `lsof -i :3000` → `kill <PID>`; or adjust `vite.config.js` `server.port` |
| `Container exits immediately` | Process terminates quickly | Ensure `CMD` keeps process running; in dev, use `uvicorn app:app --reload` not `python script.py` |
| `Can't connect to DB from container` | Network/mapping issue | In `docker-compose.yml`, ensure `backend` service can reach `db` service via hostname `db`; check `DATABASE_URL` format |
| `Out of disk space` | Docker images too large | `docker system prune -a` to remove unused images, networks, volumes |
| `404 Not Found` inside Docker | Container ports not mapped correctly | `-p 8000:8000 -p 3000:3000` in `docker run` or `docker compose` ports section |

### Docker Compose Troubleshooting

```bash
# View logs for a specific service
docker compose logs -f backend     # FastAPI backend logs
docker compose logs -f frontend    # React Vite dev server logs
docker compose logs -f db          # PostgreSQL logs

# Restart a service
docker compose restart backend

# Completely reset
docker compose down                  # Stop + remove containers, networks, volumes
docker compose up -d                 # Start fresh
```

---

## ⚛️ Node / Frontend Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `npm: command not found` | Node.js not installed | Install Node.js 20+ from https://nodejs.org |
| `node: command not found` | Same as above | |
| `vite: command not found` | Global install missing | Use `npx vite` (no global install needed) or `cd web && npm run dev` |
| `Port 3000 already in use` | Another process on port 3000 | Kill it: `lsof -i :3000` → `kill <PID>`; or change port in `web/vite.config.js` |
| `Tailwind not generating` | Paths not configured in `tailwind.config.js` | Ensure `content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"]` includes your component paths |
| `TypeScript errors` | Type mismatches | Run `npm run type-check`; fix errors or `// @ts-ignore` temporarily |
| `Component not rendering` | JSX issue, missing return | Check for unclosed tags, missing `import React from 'react'` (not needed in React 18+ with new JSX transform) |
| `API fetch failed — CORS policy` | Frontend origin not allowlisted | Edit `.env`: add `http://127.0.0.1:3000` to `BACKEND_CORS_ORIGINS`; restart backend |
| `404 not found from API` | Wrong endpoint URL | Check `api.ts` base URL (`http://127.0.0.1:8000/api` default); verify backend running at port 8000 |
| `npm install failed` | Corrupt lockfile or network | `rm -rf node_modules package-lock.json; npm install`; or `npm ci` for clean install |

### Frontend Development Commands

| Action | Command | Directory |
|--------|---------|-----------|
| Start dev server | `npm run dev` | `web/` |
| Build for production | `npm run build` | `web/` |
| Preview build locally | `npm run preview` | `web/` |
| Run lint | `npm run lint` | `web/` |
| Type check | `npm run type-check` | `web/` |

---
