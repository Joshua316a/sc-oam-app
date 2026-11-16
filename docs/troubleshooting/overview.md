# Troubleshooting

Common issues and their solutions for the sc-oam-app project.

## 🐍 Python Environment Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `uvicorn: command not found` | Virtualenv not activated | Activate: `source .venv/bin/activate` (macOS/Linux) or `.\.venv\Scripts\activate.bat` (Windows) |
| `ModuleNotFoundError: No module named 'fastapi'` | Dependencies not installed | `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'uvicorn[standard]'` | Incomplete install | `pip install "uvicorn[standard]"` |
| `pytest not found` | Dev deps not installed | `pip install -r requirements-dev.txt` |
| `ImportError: cannot import name 'xxx'` | Wrong Python version | Use Python 3.10+ (`python3 --version`) |

## 📦 Dependency Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `numpy` version conflict | Incompatible versions | `pip install --upgrade numpy` or `pip install -r requirements.txt --force-reinstall` |
| `node_modules` missing | npm install not run | `cd web && npm install` |
| `vite: command not found` | Node not in PATH | Install Node.js 18+ from https://nodejs.org |
| `tailwindcss not configured` | Config missing | Ensure `tailwind.config.js` exists in `web/` |

## ⚛️ React/Vite Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `vite: command not found` | Global install missing | `npm install -g vite` or use `npx vite` |
| `Port 3000 already in use` | Another process on port 3000 | Kill the process or change port in `vite.config.js` |
| `Tailwind not generating` | Paths not configured | Verify `tailwind.config.js` content paths are correct |
| `TypeScript errors` | Type mismatches | Run `npm run type-check` and fix errors |
| `Component not rendering` | JSX issue | Check for unclosed tags, missing imports |

## 🐳 Docker Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `docker: command not found` | Docker not installed/running | Install Docker Desktop, start it |
| `Build failed` | Python/Node deps issue | Check `Dockerfile` for correct base image |
| `Port conflicts` | 8000/3000 already in use | Use `-p 8001:8000` or adjust ports |
| `Container exits immediately` | Process terminates | Ensure `CMD` keeps process running (use `--reload` in dev) |

## 🗄️ Database Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `sqlite3.OperationalError: unable to open database file` | DB path wrong or permissions | Check `.env` DATABASE_URL, ensure writable |
| `Database is locked` | Another process reading/writing | Add `?mode=rw` to SQLite URL, reduce concurrent writes |
| `Connection refused` | PostgreSQL not running | Start PostgreSQL: `pg_ctlcluster ... start` or use Docker |
| `Unknown host` | Wrong DATABASE_URL format | Verify `postgresql://user:pass@host:port/db` format |

### SQLite Specific

| Issue | Fix |
|-------|-----|
| `database is locked` | Use `PRAGMA journal_mode=WAL;` or add `?timeout=30` to URL |
| `performance issues with large DB` | Add indexes, consider PostgreSQL migration |
| `migration from SQLite to PostgreSQL` | Update `.env` DATABASE_URL, may need data export/import |

## 🌐 CORS Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Fetch failed — CORS policy` | Frontend origin not in CORS allowlist | Add origin to `BACKEND_CORS_ORIGINS` in `.env` |
| `Headers not accessible` | Custom headers not configured | Add headers to `ALLOWED_HEADERS` in FastAPI config |

### `.env` Fix

```
# Add your frontend origin
BACKEND_CORS_ORIGINS="http://localhost:3000,http://127.0.0.1:3000,http://192.168.1.50:3000"
```

## 🔌 API Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `404 Not Found` | Wrong endpoint URL | Check `/api/health` first, see `docs/api-reference/overview.md` |
| `422 Validation Error` | Request body format wrong | Ensure JSON matches Pydantic model exactly |
| `500 Internal Server Error` | Server-side error | Check server logs, look for tracebacks |
| `Timeout` | Server not running | Start: `uvicorn app:app --reload` |

## 📦 Node Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `npm: command not found` | Node.js not installed | Install from https://nodejs.org |
| `node: command not found` | Same as above | |
| `EACCES` permission errors | Global install without sudo | Use `npm config set prefix '$HOME/.npm-global'` |
| `EMFILE: too many open files` | Too many concurrent processes | Close unused terminals, increase file limit |
| `ENAVAIL` module not available | Missing build tools | `sudo apt-get install build-essential` (Linux) |

## 🐳 Container Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Docker build fails` | Dockerfile issue | Check Dockerfile syntax, build args |
| `Container can't connect to DB` | Network config | Verify Docker network, port mapping |
| `Out of disk space` | Docker images too large | `docker system prune -a` |
| `Can't access from host` | Port mapping wrong | `-p 8000:8000 -p 3000:3000` |

## 🆘 When Nothing Else Works

1. **Check the logs** — `uvicorn app:app --reload` shows server output
2. **Re-run setup** — `rm -rf .venv; python -m venv .venv; source .venv/bin/activate; pip install -r requirements.txt`
3. **Check GitHub Issues** — search existing problems
4. **Ask in Discussions** — `GitHub Discussions` tab
5. **File an Issue** — if nothing matches, create a new issue with:
   - OS and version
   - Python/Node versions
   - Steps to reproduce
   - Full error messages (including tracebacks)
   - `.env` contents (sensitive data masked)

---

## 📬 Getting Help

| Channel | Best For |
|---------|----------|
| **GitHub Issues** | Bug reports, feature requests |
| **GitHub Discussions** | "How do I...", design questions, onboarding help |
| **AI Agents** | Use `docs/ai-agents/` guides for agent-specific troubleshooting |
| **GitHub Actions** | Check CI logs for test/lint failures |
| ** peers** | Tag specific collaborators `@username` |

---

**Tip:** Always include your OS, Python version (`python3 --version`), and Node version (`node --version`) when asking for help. This saves time diagnosing environment-specific issues.
