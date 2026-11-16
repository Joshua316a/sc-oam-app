# 📚 Glossary & Terminology — sc-oam-app

Comprehensive glossary of terms, acronyms, and project-specific vocabulary used throughout the sc-oam-app documentation and codebase.

| **MCP** | **Model Context Protocol** — Protocol for structured communication between distributed agents and the primary host in the sc-oam-app architecture; defines message formats, routing, and data serialization for inter-agent communication.

---

# 📚 Glossary & Terminology — sc-oam-app

A comprehensive glossary of terms, acronyms, and project-specific vocabulary. Organized by category for easy reference.

---

## 🎮 Project-Specific Terms

| Term | Definition |
|------|------------|
| **OAM** | Star Citizen Organisation Asset Management tool — the original name and concept for the project, representing the organisation's asset management functionality |
| **OAMv1** | The original Tkinter-based Python application (pre-FastAPI/React rewrite); legacy single-user desktop application for asset management |
| **OAMv2** | The FastAPI + React rewrite of OAM — this version; a modular, API-first full-stack application with React + Vite frontend, FastAPI backend, and SQLite/PostgreSQL database support |
| **sc-oam-app** | The new project repository — "Star Citizen Org API & App" — the FastAPI + React replacement for OAM |
| **Blueprints** | Player-owned crafting recipes/patterns in Star Citizen; tracked via `player_blueprints` table; CRUD endpoints at `/api/blueprints/` |
| **Crafting** | The process of combining resources to produce output items; quality calculation at `/api/crafting/quality`; result at `/api/crafting/result` |
| **Warehouse** | Organization inventory management; tracks `player_inventory` items; endpoints at `/api/warehouse/` |
| **Hangar** | Organization fleet management; tracks `player_ships` vessels; endpoints at `/api/hangar/` |
| **ILG** | Item Light Group — UI classification grouping items by visual/functional category (e.g., all weapons share one light group) |
| **TYPE_TO_LIGHTGROUP** | Hardcoded dict mapping `item_type` values → light group keys (e.g., `FUELPOD` → `Vehicles/FuelTanks`) — project goal: make database-driven |
| **DCB** | Data Concept Base — internal term for the structured data catalogue extracted from Star Citizen game archives |
| **SCItem** | Star Citizen Item — individual item definition found in game data archives (`.p4k`) |
| **p4k** | Pyro Archive — CIG's proprietary archive format containing game data (ships, items, modules, blueprints) |
| **svarog** | Native macOS parser for CIG game archives; faster alternative to scdatatools on Apple silicon |
| **scdatatools** | Command-line tool for reading `.p4k` archives and exporting item data to CSV |
| **Extraction Pipeline** | The process of reading game archives (`p4k`/`svarog`), classifying items, assigning categories/ILGs, and populating the reference SQLite database |
| **Gap** | Discrepancy between game data and the project's internal catalogue; categories: silent drop, ILG unmapped, category missing, type misclassification |
| **Reference DB** | SQLite database (`database.db`) persisting extracted game data for fast runtime access via `modules/data_access.py` |
| **Pluggable Database** | Architecture pattern where `DATABASE_URL` env var switches between SQLite (dev) and PostgreSQL (prod) without code changes |
| **OAM Item Categories** | 22 canonical categories (`all`, `vehicles`, `weapons`, `modules`, `cargo`, `consumables`, `equipment`, `components`, `interiors`, plus `weapons_missiles`, `weapons_guns`, `modules_shields`, `modules_drives`, `modules_sensors`, `cargo_ore`, `cargo_trade`, `consumables_fuel`, `consumables_repair`, `equipment_eva`, `equipment_tools`, `flights_systems`) |
| **Light Group** | UI visual grouping; items in same light group share rendering properties in the display UI |

---

## 💻 Software & Architecture Terms

| Term | Definition |
|------|------------|
| **FastAPI** | Modern, fast (high-performance) Python web framework for building APIs; uses type hints for automatic validation and docs |
| **Pydantic** | Python data validation using type annotations; defines schemas for API request/response validation; enables `from_attributes=True` for ORM ↔ Pydantic conversion |
| **SQLAlchemy** | SQL toolkit and ORM for Python; defines database models (`models/*.py`) and manages sessions; supports SQLite ↔ PostgreSQL pluggability |
| **Alembic** | Database migration tool for SQLAlchemy; handles schema evolution (`alembic upgrade head`, `alembic revision`) |
| **SQLite** | Embedded relational database; file-based (`database.db`), zero-config for local development; not suitable for concurrent multi-user |
| **PostgreSQL** | Open-source relational database server; supports concurrent users, larger datasets, remote access; production/VPS deployment |
| **Docker** | Containerization platform; packages application + dependencies for consistent deployment across environments |
| **Docker Compose** | Tool for defining and running multi-container Docker applications; `docker compose up -d` starts all services |
| **Git** | Distributed version control system; tracks code changes, enables branching/merging, pull requests |
| **GitHub Actions** | CI/CD automation platform; runs lint + test on every PR; block merge if failures; Dependabot for auto-updates |
| **Conventional Commits** | Commit message format: `<type>(<scope>): <description>` (feat, fix, docs, style, refactor, test, chore) |
| **API** | Application Programming Interface — set of endpoints/methods that define how software components communicate |
| **REST** | Architectural style for APIs; uses HTTP methods (GET/POST/PUT/DELETE) and URL patterns; sc-oam-app follows REST conventions |
| **OpenAPI** | Specification format for describing REST APIs; auto-generates Swagger UI (`/docs`) and ReDoc (`/redoc`) |
| **Swagger UI** | Interactive API documentation (`/docs` endpoint); test endpoints directly from browser |
| **ReDoc** | Alternative API documentation format (`/redoc` endpoint); markdown-styled presentation |
| **CI/CD** | Continuous Integration / Continuous Deployment; automatic testing, building, and deployment pipeline |
| **Dependabot** | GitHub feature that opens PRs for automated dependency updates (weekly by default) |
| **CODEOWNERS** | GitHub file; assigns specific reviewers for certain file patterns or directories |
| **PR** | Pull Request — proposal to merge code changes; triggers CI/CD and code review |
| **Issue** | GitHub issue tracker item; bug report, feature request, or task |
| **Discussion** | GitHub Discussions — Q&A, design discussions, "how do I" questions (less formal than Issues) |
| **Virtual Environment (venv)** | Isolated Python environment (`python -m venv .venv`); prevents package conflicts between projects |
| **PEP 508** | Python environment marker syntax; used in `.env` and `requirements.txt` for conditional dependencies |
| **ASGI** | Asynchronous Server Gateway Interface; protocol standard between async web servers and Python web frameworks (FastAPI uses ASGI) |
| **WSGI** | Web Server Gateway Interface; synchronous protocol (older; not used by FastAPI which is ASGI) |

---

## 🤖 AI Agent Terms

| Term | Definition |
|------|------------|
| **OpenCode** | This project's AI agent framework; provides skills, tools, codegraph, guardrails, and session management; the agent runtime executing this conversation |
| **Skill** | Reusable, modular unit of work; each has an ID, description, and trigger conditions (e.g., `session-startup`, `codegraph_explore`, `gitnexus_impact`) |
| **Tool** | Low-level API call; e.g., `codegraph_explore`, `gitnexus_impact`, `gitnexus_context` — invoked by skills or directly by the agent |
| **Agent** | The LLM instance running within OpenCode; responds to prompts, calls skills/tools, maintains state across turns |
| **Context Window** | The amount of conversation/history the agent can reference; limited per session; governed by `session-startup` dashboard |
| **Hallucination** | When the AI generates plausible-sounding but incorrect information; mitigated by grounding in codegraph/gitnexus data |
| **Prompt Injection** | When user input overrides or confuses the system prompt; handled by guardrails and skill boundaries |
| **Session Startup** | Initial health check at session beginning; verifies git branch, version drift, working tree cleanliness, proposal status, spec counts |
| **Unlazy** | Completion discipline skill; enforces gates/GATES.md before reporting task completion; prevents incomplete work |
| **GATES.md** | Gates definition file; runnable checks per phase; must be met before task completion can be reported |
| **Glide** | Not applicable; placeholder |
| **Agent Memory** | Persistent context across sessions; stored in `.unlazy/` directory; includes G1 (version drift) through G6 (no unarchived proposals) |
| **Runnability** | Whether a gate/check can be executed (has required files, dependencies, environment) |
| **Gate-check** | Script: `node ~/.agents/skills/unlazy/scripts/gate-check.mjs`; checks status, lints, reverifies, approves gates |
| **Linter** | Static code analysis tool (ruff for Python, eslint for JS/TS); enforced in CI/CD and `docs/contributing/code-style.md` |
| **Formatter** | Code beautifier (black for Python, prettier for JS/TS); enforced in CI/CD |
| **Type Check** | `npm run type-check` (TypeScript compiler); ensures type safety in frontend code |
| **Pyright** | Alternative Python type checker; not currently used (ruff handles Python linting) |
| **Mermaid** | Diagram syntax rendered via JavaScript; used in documentation for flowcharts, sequence diagrams, gantt charts |
| **Markdown** | Lightweight markup language; used for all documentation files (`*.md`) |
| **YAML** | Human-readable data serialization; used in `.env.example`, `dependabot.yml`, `github/workflows/ci.yml` |
| **JSON** | JavaScript Object Notation; data interchange format; used in API requests/responses, Pydantic models, `.env.example` |
| **Frontmatter** | Markdown YAML at top of some docs; not heavily used in this project but noted for consistency |

---

## 📄 File & Format Acronyms

| Term | Definition |
|------|------------|
| **.gitignore** | File specifying intentionally untracked files to ignore in Git (e.g., `database.db`, `.venv/`, `node_modules/`) |
| **.env** | Environment variable file; `KEY=VALUE` pairs loaded via `python-dotenv`; **never committed** to git |
| **.env.example** | Template `.env` file committed to git; users copy to `.env` and fill real values; checked into version control |
| **requirements.txt** | Python runtime dependencies; `pip install -r requirements.txt` installs all needed packages |
| **requirements-dev.txt** | Python development dependencies; `pip install -r requirements-dev.txt` installs linting/testing tools |
| **pyproject.toml** | Modern Python project config (PEP 518); manages build system, dependencies, project metadata (ruff, black, pytest config) |
| **Pipfile / Pipfile.lock** | Not used by this project; pip/uv package resolution preferred |
| **Vite** | Frontend build tool + dev server; `npm run dev` starts HMR (Hot Module Replacement) React development server |
| **TAO** | Not applicable; placeholder |
| **CSS** | Cascading Style Sheets; styling language for Web UIs; sc-oam-app uses Tailwind CSS utility classes |
| **HTML** | HyperText Markup Language; page structure; `web/index.html` is the React root container |
| **JS** | JavaScript; programming language for web interactivity (some usage in Vite config, but project favors TypeScript) |
| **TS** / **TypeScript** | Typed superset of JavaScript; `web/tsconfig.json` + `*.tsx` files; provides compile-time type checking |
| **JSX** | JavaScript XML; syntax for writing HTML-like code in TypeScript/React components (`*.tsx` files) |
| **Axios** | Promise-based HTTP client for the browser + Node; used in `web/src/lib/api.ts` for all API calls |
| **ESLint** | JS/TS linter; `npm run lint`; enforced in GitHub Actions CI |
| **Prettier** | Code formatter (not directly used; Python uses black, JS/TS relies on ESLint + manual standards) |
| **npm** | Node package manager; `npm install`, `npm run`, `npm ci` |
| **pnpm / Yarn** | Not used by this project; npm is the package manager |
| **Mermaid** | Diagram syntax (```flow, sequenceDiagram, gantt```) rendered via JavaScript in Markdown |
| **Markdown** | `*.md` files; documentation format; supported by GitHub, OpenCode, most editors |
| **YAML** | `*.yml` / `*.yaml`; key-value pairing; used in `dependabot.yml`, `github/workflows/ci.yml`, `.env.example` |
| **JSON** | `*.json`; data interchange; API request/response bodies, Pydantic model config, `package.json`, `vite.config.js` |
| **Tauri** | Not used; Electron alternative for desktop apps with Rust backend |
| **Electron** | Not used; framework for desktop GUI apps with web technologies |
| **POSIX** | Portability Operating System Interface; Unix-like OS conventions; relevant for cross-platform compatibility |

---

## 🗺️ Quick Reference Index

| Category | First Page Line |
|----------|-----------------|
| Project-Specific Terms | 1 |
| Software & Architecture Terms | ~50 |
| AI Agent Terms | ~120 |
| File & Format Acronyms | ~180 |

## 🔍 How to Use This Glossary

| Situation | Look Up |
|-----------|---------|
| "What does 'ILG' mean in this project?" | `Project-Specific Terms` → ILG |
| "What's the difference between SQLite and PostgreSQL here?" | `Software & Architecture Terms` → SQLite / PostgreSQL |
| "What does 'DATABASE_URL' configure?" | `Software & Architecture Terms` → DATABASE_URL |
| "What's `scdatatools` used for?" | `Project-Specific Terms` → scdatatools |
| "What's the commit message format?" | `Software & Architecture Terms` → Conventional Commits |
| "How do I read the .p4k archives?" | `Project-Specific Terms` → p4k / scdatatools / svarog |
| "What's VITE_API_BASE_URL?" | `AI Agent Terms` → VITE_API_BASE_URL (or Software terms) |
| "What does 'from_attributes' mean in Pydantic?" | `Software & Architecture Terms` → Pydantic |
| "What's in the .env.example?" | `File & Format Acronyms` → .env / .env.example |
| "What's the CI/CD matrix?" | `AI Agent Terms` → GitHub Actions |

---
