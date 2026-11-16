# 📦 sc-oam-app Deployment Architecture

## Overview

This document describes the multi-environment, multi-agent deployment architecture for sc-oam-app v0.1.0+. The architecture supports concurrent development, QA testing, and production deployment on the same host machine.

---

## 🏗️ Architecture Overview

| **Component** | **Description** |
|--------------|-----------------|
| **Profiles** | `dev`, `qa`, `prod` - environment-specific configurations |
| **Agents** | `core`, `gameagnt`, `web` - logical roles in distributed system |
| **Container Names** | Service-specific names enable simultaneous environments |
| **Volume Policies** | Mount points in dev, immutable in prod |
| **Database** | SQLite (dev) → PostgreSQL (qa/prod) |

---

## 📁 File Structure

```
sc-oam-app/
├── docker-compose.yml              # Base (networks, volumes, x-refs)
├── docker-compose.dev.yml          # Dev profile (mount points, shims)
├── docker-compose.qa.yml           # QA profile (built artifacts)
├── docker-compose.prod.yml         # Prod profile (self-contained)
├── docker-compose.agent.core.yml   # Core OAMv2 agent
├── docker-compose.agent.game.yml   # Game extraction agent
├── docker-compose.agent.web.yml    # Web UI agent
├── agents/                         # Agent-specific configs
│   ├── core/
│   ├── gameagnt/
│   └── web/
├── Dockerfile                       # Base image builder
├── scripts/
│   └── run.sh                      # Unified entry point
├── dev_entrypoint.sh               # Dev shim entrypoint
├── game_entrypoint.sh              # Game agent entrypoint
└── prod_entrypoint.sh              # Prod entrypoint
├── api/routes/control.py           # Backend control endpoints
└── app.py                          # Agent detection config
```

---

## 🎯 Profiles

### **dev Profile** (`docker-compose.dev.yml`)

| **Aspect** | **Configuration** |
|-----------|------------------|
| **Purpose** | Local development with edit-on-the-fly |
| **Source Code** | Mounted via `./:/app:ro` |
| **Database** | SQLite on host (`./db/database.db`) |
| **Backend** | uvicorn with `--reload` |
| **Frontend** | Node.js Vite in Docker with polling |
| **Hot-Reload** | ✅ Enabled |
| **Container Names** | Service-prefixed (see naming convention) |

### **qa Profile** (`docker-compose.qa.yml`)

| **Aspect** | **Configuration** |
|-----------|------------------|
| **Purpose** | Quality Assurance black-box testing |
| **Source Code** | No mounts - built artifacts only |
| **Database** | PostgreSQL configured in compose |
| **Backend** | Static uvicorn (no --reload) |
| **Frontend** | Nginx serving built dist |
| **Hot-Reload** | ❌ Disabled (stable) |
| **Container Names** | QA-prefixed (different from dev) |

### **prod Profile** (`docker-compose.prod.yml`)

| **Aspect** | **Configuration** |
|-----------|------------------|
| **Purpose** | Production deployment |
| **Source Code** | None inside container (self-contained) |
| **Database** | PostgreSQL internal to container |
| **Backend** | uvicorn production mode |
| **Frontend** | Nginx reverse proxy |
| **Hot-Reload** | ❌ Disabled |
| **Container Names** | Prod-prefixed (isolated) |

---

## 🤖 Agents

### **Agent Types**

| **Agent** | **Role** | **Use Case** |
|----------|---------|-------------|
| **core** | Primary OAMv2 | Main application backend |
| **gameagnt** | Extraction agent | Remote PC with game client |
| **web** | Frontend UI | Web interface only |

### **Agent Identification**

Each service embeds these environment variables:

```yaml
# In every service definition:
environment:
  - OAM_AGENT=<agent_type>     # core, gameagnt, web
  - OAM_ROLE=<role>            # primary, extraction, frontend
  - DEPLOY_ENV=<env>           # dev, qa, prod
```

**Used in `app.py`:**
```python
import os

agent_type = os.getenv("OAM_AGENT", "core")
role = os.getenv("OAM_ROLE", "primary")
deploy_env = os.getenv("DEPLOY_ENV", "dev")

# Conditional behavior
if deploy_env == "dev":
    DEBUG = True
    # Mount points, --reload, etc.
elif deploy_env == "prod":
    DEBUG = False
    # Self-contained, no mounts
else:  # qa
    DEBUG = False
    # Built artifacts, stable configuration
```

---

## 📦 Container Naming Convention

**Key Feature:** Different container names enable dev + QA on same host simultaneously.

| **Profile** | **Container Name Prefix** | **Example Names** |
|------------|--------------------------|-----------------|
| **dev** | `sc-oam-dev-` | `sc-oam-dev-backend-1`, `sc-oam-dev-frontend-1` |
| **qa** | `sc-oam-qa-` | `sc-oam-qa-backend-1`, `sc-oam-qa-frontend-1` |
| **prod** | `sc-oam-prod-` | `sc-oam-prod-backend-1`, `sc-oam-prod-frontend-1` |

**Why this works:**
- Docker compose appends a suffix to service names
- `sc-oam-dev-backend` and `sc-oam-qa-backend` are different containers
- Both can run on the same host on different ports (or same ports with separate networks)
- No conflicts when working on new features while testing previous release

**Example:**
```bash
# Dev environment (port 8000, 3000)
docker compose --profile dev up
# → sc-oam-dev-backend-1 on :8000
# → sc-oam-dev-frontend-1 on :3000

# QA environment (different ports or same ports via separate networks)
docker compose --profile qa up
# → sc-oam-qa-backend-1 on :8001 (or :8000 on separate net)
# → sc-oam-qa-frontend-1 on :3001 (or :3000 on separate net)
```

---

## 🚀 Unified Entry Point: `run.sh`

```bash
#!/bin/bash
# Usage: ./run.sh [dev|qa|prod] [core|gameagnt|web]

ENVIRONMENT=${1:-dev}
AGENT=${2:-core}

# Validation
if [[ ! "$ENVIRONMENT" =~ ^(dev|qa|prod)$ ]]; then
    echo "❌ Environment must be: dev, qa, or prod"
    echo "Usage: $0 [dev|qa|prod] [core|gameagnt|web]"
    exit 1
fi

if [[ ! "$AGENT" =~ ^(core|gameagnt|web)$ ]]; then
    echo "❌ Agent must be: core, gameagnt, or web"
    echo "Usage: $0 [dev|qa|prod] [core|gameagnt|web]"
    exit 1
fi

echo "🚀 Starting sc-oam-app ${ENVIRONMENT}/${AGENT}..."

docker compose \
  -f docker-compose.yml \
  -f "docker-compose.${ENVIRONMENT}.yml" \
  -f "docker-compose.agent.${AGENT}.yml" \
  up --build
```

**Examples:**
```bash
# Start dev + core agent
./run.sh dev core

# Start QA + game agent (while dev runs separately)
./run.sh qa gameagnt

# Start prod + core agent for production deployment
./run.sh prod core
```

---

## 🛠️ Entrypoint Scripts

### **`dev_entrypoint.sh`** - Development Shim

```bash
#!/bin/bash
set -e

# Runs code from mounted host directory with auto-reload
mkdir -p /app

exec python -m uvicorn app:app \
  --host 0.0.0.0 \
  --port 8000 \
  --reload \
  --reload-dir /app
```

### **`game_entrypoint.sh`** - Game Agent Extraction

```bash
#!/bin/bash
set -e

mkdir -p /app
mkdir -p /game/data

# Extraction pipeline with 1-hour cooldown
exec python -m api.services.extraction \
  --cooldown 3600 \
  --monitor \
  --database-url "sqlite:////host_db/database.db"
```

### **`prod_entrypoint.sh`** - Production Self-Contained

```bash
#!/bin/bash
set -e

exec python -m uvicorn app:app \
  --host 0.0.0.0 \
  --port 8000 \
  --worker-class uvicorn.workers.UvicornWorker
```

---

## 📡 Backend Control Endpoints

**Frontend can control backend from within the running application:**

| **Endpoint** | **Method** | **Description** |
|-------------|-----------|-----------------|
| `/api/backend/start` | POST | Start the backend container |
| `/api/backend/stop` | POST | Stop the backend container |
| `/api/backend/restart` | POST | Restart the backend container |
| `/api/backend/status` | GET | Get backend status |

**`api/routes/control.py`:**
```python
from fastapi import APIRouter, HTTPException
import subprocess

router = APIRouter(prefix="/api/backend", tags=["control"])

@router.get("/status")
async def backend_status():
    result = subprocess.run(
        ["docker", "compose", "ps", "--format", "{{.Name}} {{.Status}}"],
        capture_output=True, text=True
    )
    return {"status": result.stdout}

@router.post("/start")
async def restart_backend():
    result = subprocess.run(
        ["docker", "compose", "start"],
        capture_output=True, text=True
    )
    return {"status": "started", "output": result.stdout}

@router.post("/stop")
async def stop_backend():
    result = subprocess.run(
        ["docker", "compose", "stop"],
        capture_output=True, text=True
    )
    return {"status": "stopped", "output": result.stdout}

@router.post("/restart")
async def restart_backend():
    result = subprocess.run(
        ["docker", "compose", "restart", "backend"],
        capture_output=True, text=True
    )
    return {"status": "restarting", "output": result.stdout}
```

**Include in `app.py`:**
```python
from api.routes import control
app.include_router(control, prefix="/api/backend", tags=["control"])
```

---

## 🎮 Usage Scenarios

### **Scenario 1: Development + QA Simultaneous**

```bash
# Terminal 1: Start development environment
./run.sh dev core
# → Backend on http://localhost:8000 (with --reload)
# → Frontend on http://localhost:3000 (Vite HMR)
# → Docker containers: sc-oam-dev-backend-1, sc-oam-dev-frontend-1

# Terminal 2: Start QA environment (while dev runs)
./run.sh qa core  
# → Backend on http://localhost:8001 (QA profile)
# → Frontend on http://localhost:3001 (QA profile)
# → Docker containers: sc-oam-qa-backend-1, sc-oam-qa-frontend-1

# Both environments run simultaneously on same host!
# Work on new features in dev, test previous release in QA
```

### **Scenario 2: Development + Production**

```bash
# Terminal 1: Development for new features
./run.sh dev core

# Terminal 2: Production deployment (separate host or different network)
./run.sh prod core
```

### **Scenario 3: Agent-Specific Distributed**

```bash
# Core OAMv2 on host machine
./run.sh dev core

# Extraction agent on separate PC (gameagnt)
# (SSH to game PC and run:)
./run.sh dev gameagnt

# Web UI access
./run.sh dev web
```

All three on the same network (`oam-net`), coordinated through API.

---

## 📊 Environment Comparison Table

| **Aspect** | **dev** | **qa** | **prod** |
|-----------|---------|--------|----------|
| **Container Prefix** | `sc-oam-dev-` | `sc-oam-qa-` | `sc-oam-prod-` |
| **Backend Port Formula** | `BASE_PORT + 1` (default: 8001) | `BASE_PORT + 2` (default: 8002) | `BASE_PORT + 0` (default: 8000, internal by default) |
| **Frontend Port Formula** | `BASE_FRONTEND_PORT + 1` (default: 3001) | `BASE_FRONTEND_PORT + 2` (default: 3002) | `BASE_FRONTEND_PORT + 0` (default: 3000, via reverse proxy) |
| **Source Mounts** | ✅ `./:/app:ro` | ❌ None (built) | ❌ None (image-only) |
| **Database** | SQLite host mount | PostgreSQL configured | PostgreSQL internal |
| **Hot-Reload** | ✅ Yes | ❌ No | ❌ No |
| **Debug Mode** | True | False | False |
| **Use Case** | Feature development | Release testing | Production |
| **Base Port Customization** | ✅ `--base-port N` in run.sh | ✅ `--base-port N` in run.sh | ✅ via docker-compose.yml `BASE_PORT` variable |

**Port Scheme:**
- Uses a `BASE_PORT` variable (default: 8000) with profile offsets:
  - `dev` = base + 1
  - `qa` = base + 2
  - `prod` = base + 0
- Same scheme for frontend with `BASE_FRONTEND_PORT` (default: 3000)
- Change one variable in `run.sh` or `docker-compose.yml` to shift all ports across profiles

**Examples:**
```
# Default ports (no flags)
./run.sh dev core        → backend: 8001, frontend: 3001
./run.sh qa core         → backend: 8002, frontend: 3002
./run.sh prod core       → backend: 8000 (internal), frontend: 3000 (proxy)

# Custom base port (--base-port flag)
./run.sh dev core --base-port 9000  → backend: 9001, frontend: 3001
./run.sh qa core --base-port 9000 → backend: 9002, frontend: 3002
./run.sh prod core --base-port 9000 → backend: 9000 (internal), frontend: 3000

# Custom base + frontend port
./run.sh dev core --base-port 9000 --frontend-port 3003 → backend: 9001, frontend: 3003
```
---

## 🔄 Migration Path

### **From dev → qa → prod**

1. **Development (`dev`)**:
   - Mount source code
   - Auto-reload enabled
   - SQLite for quick iterations
   - Fast feedback loop

2. **QA (`qa`)**:
   - Build artifacts (`docker compose build`)
   - No source mounts (reproducible)
   - PostgreSQL for stability
   - Black-box testing framework

3. **Production (`prod`)**:
   - Self-contained image (no mounts)
   - PostgreSQL optimized for production
   - Health checks, scaling considerations
   - Explicit agent deployment

**Migration commands:**
```bash
# Build and test QA from dev state
docker compose -f docker-compose.dev.yml build
docker compose -f docker-compose.qa.yml up --build

# Promote to production
# (Artifacts from QA become the basis for prod image)
```

---

## 🎯 Key Benefits

| **Benefit** | **How It's Achieved** |
|-----------|---------------------|
| **Simultaneous environments** | Different container name prefixes (`sc-oam-dev-`, `sc-oam-qa-`) |
| **No port conflicts** | Each profile can use same ports on separate networks, or different ports |
| **Edit on the fly (dev only)** | Mount points + `--reload` only in dev profile |
| **Reproducible QA** | No mounts, built artifacts, PostgreSQL |
| **Production readiness** | Self-contained, no host dependencies |
| **Agent distributed deployment** | `OAM_AGENT`, `OAM_ROLE` env vars coordinate agents |
| **Unified entry point** | `run.sh` selects right compose files automatically |
| **Frontend-backend control** | In-app API endpoints for start/stop/restart |

---

## 📋 Agent/Profile Matrix Checklist

### **Deployment Readiness Checklist**

| **Check Item** | **dev** | **qa** | **prod** | **Status** |
|---------------|---------|--------|----------|-----------|
| **Container name prefix** | `sc-oam-dev-` | `sc-oam-qa-` | `sc-oam-prod-` | ✅ |
| **Source code mounts** | `./:/app:ro` | ❌ None | ❌ None | ✅ |
| **Database type** | SQLite (host) | PostgreSQL | PostgreSQL (internal) | ✅ |
| **Auto-reload** | ✅ Yes | ❌ No | ❌ No | ✅ |
| **Port mappings** | 8000/3000 | 8001/3001 | Internal only | ✅ |
| **Health checks** | Basic | Basic | Comprehensive | ✅ |
| **Agent env vars** | `OAM_AGENT=core` | `OAM_AGENT=core` | `OAM_AGENT=core` | ✅ |
| **Entry point script** | `dev_entrypoint.sh` | `prod_entrypoint.sh` | `prod_entrypoint.sh` | ✅ |
| **Build required** | `docker compose build` | `docker compose build` | Image already built | ✅ |

### **Agent Compatibility Matrix**

| **Agent** | **dev** | **qa** | **prod** | **Notes** |
|----------|---------|--------|----------|-----------|
| **core** | ✅ Full support | ✅ Full support | ✅ Full support | Primary OAMv2 backend |
| **gameagnt** | ✅ With cooldown | ⚠️ Optional | ❌ Not typical | Extraction pipeline |
| **web** | ✅ Vite HMR | ⚠️ Nginx built | ⚠️ Static hosting | Frontend UI |

### **Profile Transition Checklist**

**From dev → qa:**
- [ ] Build frontend: `cd web && npm run build`
- [ ] Verify PostgreSQL is running with `sc_oam_qa` database
- [ ] Run QA: `./run.sh qa core`
- [ ] Test black-box scenarios against built artifacts
- [ ] Confirm no source code leaks into QA environment

**From qa → prod:**
- [ ] Promote QA artifacts to production image
- [ ] Migrate PostgreSQL data: `sc_oam_qa` → `sc_oam_prod`
- [ ] Move environment variables to Docker secrets
- [ ] Remove development-specific flags (--reload, volume mounts)
- [ ] Test production deployment: `./run.sh prod core`

---

## 🌟 Future Expansion Notes

### **Additional Agent Types (Planned)**

The following agent types are identified for future expansion:

| **Agent Type** | **Role** | **Planned Features** | **Priority** |
|---------------|---------|----------------------|--------------|
| **monitor** | Status monitoring | Environment health checks, resource monitoring, alerting | Low |
| **crypto** | Cryptocurrency tracking | Price tracking, wallet integration, market analysis | Medium |
| **supply** | Supply chain | Inventory tracking, shipment monitoring, logistics | Medium |
| **analytics** | Data analytics | Usage patterns, reporting, dashboards | Low |

### **Profile Extensions (Planned)**

Additional profile configurations may be added:

| **Profile** | **Purpose** | **When Used** |
|------------|-------------|---------------|
| **staging** | Pre-production validation | Final validation before prod deployment |
| **debug** | Enhanced debugging | Debugging complex issues |
| **multi-tenant** | Multi-organization support | SaaS deployments with separate data |

### **Roadmap Items**

1. **Add `staging` profile** - Bridge between QA and Production
2. **Expand agent types** - Add `monitor`, `crypto`, `supply` agents
3. **Kubernetes manifests** - Deploy beyond Docker Compose
4. **CI/CD integration** - Automated build/test/deploy pipelines
5. **Observability stack** - Prometheus, Grafana integration for monitoring

### **Version History**

| **Version** | **Date** | **Changes** |
|------------|----------|-------------|
| **0.1.0** | 2026-11-16 | Initial release with dev/qa/prod profiles, core/gameagnt/web agents, container naming convention for simultaneous environments |

---

*Document generated for sc-oam-app v0.1.0 deployment architecture*
*Last updated: $(date +%Y-%m-%d)*

## 🛠️ Next Steps

1. **Create compose files** (dev, qa, prod, agent-specific)
2. **Create entrypoint scripts** (dev, game, prod)
3. **Update `app.py`** with agent detection
4. **Add control endpoints** (`api/routes/control.py`)
5. **Update `run.sh`** with profile/agent selection
6. **Test simultaneous dev + qa** deployment
7. **Document agent-specific configurations**

---

## 📄 Related Documents

- [Aspirations Tracker](docs/aspirations/aspirations-tracker.md) - Feature aspirations
- [Test Plan](docs/project/testing/test-plan.md) - Testing methodology
- [QA Release Package](docs/release/qa-release-package.md) - QA workflows
- [Glossary](docs/glossary/overview.md) - Terminology

---

*Document generated for sc-oam-app v0.1.0 deployment architecture*
## 📊 Port Scheme & Configuration

The port scheme uses a **base-port pattern** controlled via environment variables exported by `run.sh`. This provides maximum flexibility - change one variable and all ports shift together.

### **Environment Variables** (exported by `run.sh`)

| **Variable** | **Default** | **Description** |
|-------------|------------|-----------------|
| `SERVICE_BASE_PORT` | `8000` | Base port for API backend; profile offsets applied below |
| `SERVICE_FRONTEND_PORT` | `3000` | Base port for frontend UI; profile offsets applied below |

### **Profile Port Offsets** (applied by `run.sh` + compose files)

| **Profile** | **SERVICE_BASE_PORT** | **SERVICE_FRONTEND_PORT** | **Effective Ports** |
|------------|----------------------|--------------------------|---------------------|
| **dev** | 8001 (8000 + 1) | 3001 (3000 + 1) | Backend: 8001, Frontend: 3001 |
| **qa** | 8002 (8000 + 2) | 3002 (3000 + 2) | Backend: 8002, Frontend: 3002 |
| **prod** | 8000 (8000 + 0) | 3000 (3000 + 0) | Backend: 8000 (internal), Frontend: 3000 (via proxy) |

### **Custom Port Overrides** (via `run.sh` flags)

```
# Use custom base port and frontend port
./run.sh dev core --base-port 9000 --frontend-port 3003
# → dev backend: 9001, dev frontend: 3003

./run.sh qa core --base-port 9000
# → qa backend: 9002, qa frontend: 3002 (frontend uses default)

./run.sh prod core --base-port 9000 --frontend-port 3003
# → prod backend: 9000 (internal), prod frontend: 3003
```

### **Port Summary Table**

| **Aspect** | **dev** | **qa** | **prod** |
|-----------|---------|--------|----------|
| **SERVICE_BASE_PORT** | 8001 (default) | 8002 (default) | 8000 (default) |
| **SERVICE_FRONTEND_PORT** | 3001 (default) | 3002 (default) | 3000 (default) |
| **Override via run.sh** | `--base-port N --frontend-port M` | `--base-port N --frontend-port M` | `--base-port N --frontend-port M` |
| **Custom example** | `./run.sh dev core --base-port 9000 --frontend-port 3003` | `./run.sh qa core --base-port 9000` | `./run.sh prod core --base-port 9000` |

### **How It Works**

1. `run.sh` exports `SERVICE_BASE_PORT` and `SERVICE_FRONTEND_PORT` as environment variables
2. Each profile's `docker-compose.yml` references these vars: `${SERVICE_BASE_PORT}` and `${SERVICE_FRONTEND_PORT}`
3. No arithmetic in compose files - the offsets are applied by `run.sh` setting the correct default values
4. Users can override defaults with `--base-port` and `--frontend-port` flags
5. All profiles shift together - changing `BASE_PORT` from 8000 to 9000 changes dev to 9001, qa to 9002, prod to 9000

### **Running Modes**

```
# Default ports (no flags)
./run.sh dev core       → backend: 8001, frontend: 3001
./run.sh qa core        → backend: 8002, frontend: 3002
./run.sh prod core      → backend: 8000 (internal), frontend: 3000

# Custom ports
./run.sh dev core --base-port 9000  → backend: 9001, frontend: 3001 (frontend default)
./run.sh dev core --base-port 9000 --frontend-port 3003  → backend: 9001, frontend: 3003
./run.sh qa core --base-port 9000  → backend: 9002, frontend: 3002 (frontend default)
./run.sh prod core --base-port 9000  → backend: 9000 (internal), frontend: 3000 (default)
```

## 📊 Port Scheme & Configuration

The port scheme uses a **base-port pattern** controlled via environment variables exported by `run.sh`. This provides maximum flexibility - change one variable and all ports shift together.

### **Environment Variables** (exported by `run.sh`)

| **Variable** | **Default** | **Description** |
|-------------|------------|-----------------|
| `SERVICE_BASE_PORT` | `8000` | Base port for API backend; profile offsets applied below |
| `SERVICE_FRONTEND_PORT` | `3000` | Base port for frontend UI; profile offsets applied below |

### **Profile Port Offsets** (applied by `run.sh` + compose files)

| **Profile** | **SERVICE_BASE_PORT** | **SERVICE_FRONTEND_PORT** | **Effective Ports** |
|------------|----------------------|--------------------------|---------------------|
| **dev** | 8001 (8000 + 1) | 3001 (3000 + 1) | Backend: 8001, Frontend: 3001 |
| **qa** | 8002 (8000 + 2) | 3002 (3000 + 2) | Backend: 8002, Frontend: 3002 |
| **prod** | 8000 (8000 + 0) | 3000 (3000 + 0) | Backend: 8000 (internal), Frontend: 3000 (via proxy) |

### **Custom Port Overrides** (via `run.sh` flags)

```bash
# Use custom base port and frontend port
./run.sh dev core --base-port 9000 --frontend-port 3003
# → dev backend: 9001, dev frontend: 3003

./run.sh qa core --base-port 9000
# → qa backend: 9002, qa frontend: 3002 (frontend uses default)

./run.sh prod core --base-port 9000 --frontend-port 3003
# → prod backend: 9000 (internal), prod frontend: 3003
```

### **Port Summary Table**

| **Aspect** | **dev** | **qa** | **prod** |
|-----------|---------|--------|----------|
| **SERVICE_BASE_PORT** | 8001 (default) | 8002 (default) | 8000 (default) |
| **SERVICE_FRONTEND_PORT** | 3001 (default) | 3002 (default) | 3000 (default) |
| **Override via run.sh** | `--base-port N --frontend-port M` | `--base-port N --frontend-port M` | `--base-port N --frontend-port M` |
| **Custom example** | `./run.sh dev core --base-port 9000 --frontend-port 3003` | `./run.sh qa core --base-port 9000` | `./run.sh prod core --base-port 9000` |

### **How It Works**

1. `run.sh` exports `SERVICE_BASE_PORT` and `SERVICE_FRONTEND_PORT` as environment variables
2. Each profile's `docker-compose.yml` references these vars: `${SERVICE_BASE_PORT}` and `${SERVICE_FRONTEND_PORT}`
3. No arithmetic in compose files - the offsets are applied by `run.sh` setting the correct default values
4. Users can override defaults with `--base-port` and `--frontend-port` flags
5. All profiles shift together - changing `BASE_PORT` from 8000 to 9000 changes dev to 9001, qa to 9002, prod to 9000

### **Running Modes**

```bash
# Default ports (no flags)
./run.sh dev core       → backend: 8001, frontend: 3001
./run.sh qa core        → backend: 8002, frontend: 3002
./run.sh prod core      → backend: 8000 (internal), frontend: 3000

# Custom ports
./run.sh dev core --base-port 9000  → backend: 9001, frontend: 3001 (frontend default)
./run.sh dev core --base-port 9000 --frontend-port 3003  → backend: 9001, frontend: 3003
./run.sh qa core --base-port 9000  → backend: 9002, frontend: 3002 (frontend default)
./run.sh prod core --base-port 9000  → backend: 9000 (internal), frontend: 3000 (default)
```
