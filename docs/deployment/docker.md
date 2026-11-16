# Docker Deployment

Containerized deployment of sc-oam-app using FastAPI + React in a multi-stage Docker build.

## 🐳 Prerequisites

- Docker Desktop or Engine installed and running
- Docker Compose (v2+, included with Docker Desktop)

## 📦 Docker Development Build

### Build the Image

```bash
# From the project root
docker build -t sc-oam-app:dev .
```

### Run in Development Mode

```bash
# Mount current directory for live reload
docker run -d \
  -p 8000:8000 \
  -p 3000:3000 \
  -v $(pwd):/app \
  -e ENVIRONMENT=development \
  --name sc-oam-dev \
  sc-oam-app:dev
```

### Access Services

| Service | URL |
|---------|-----|
| **FastAPI + Docs** | http://127.0.0.1:8000/docs |
| **React Dev Server** | http://127.0.0.1:3000 |
| **Health Check** | http://127.0.0.1:8000/health |

### Stop Development Container

```bash
docker stop sc-oam-dev && docker rm sc-oam-dev
```

## 🏭 Docker Production Build

### Multi-Stage Dockerfile

The project uses a multi-stage build:

1. **Stage 1 (Build):** Python dependencies + FastAPI app
2. **Stage 2 (Build):** Node + React + Tailwind
3. **Stage 3 (Runtime):** Combined static serving + API

### Build Production Image

```bash
docker build -t sc-oam-app:prod .
```

### Run Production Container

```bash
docker run -d \
  -p 80:8000 \
  -e ENVIRONMENT=production \
  -e DATABASE_URL="postgresql://user:password@host:5432/sc_oam_db" \
  -e SECRET_KEY="your-super-secret-key-change-in-production" \
  --name sc-oam-prod \
  sc-oam-app:prod
```

### Production Access

| Service | URL |
|---------|-----|
| **API** | http://127.0.0.1:8000/docs |
| **Health** | http://127.0.0.1:8000/health |

## 📊 Docker Compose

### `docker-compose.yml`

```yaml
version: "3.9"

services:
  backend:
    build:
      context: .
      target: python
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - ENVIRONMENT=development
      - DEBUG=True
    command: uvicorn app:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build:
      context: ./web
      target: node
    ports:
      - "3000:3000"
    volumes:
      - ./web:/app
    environment:
      - VITE_API_URL=http://localhost:8000/api
    ports:
      - "3000:3000"

  # Optional: PostgreSQL
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: sc_oam_db
      POSTGRES_USER: oam_user
      POSTGRES_PASSWORD: password
    volumes:
      - pg_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  pg_data:
```

### Run with Compose

```bash
docker-compose up -d          # Start all services
docker-compose down           # Stop all services
docker-compose logs -f      # Follow logs
```

## 🔄 Development Workflow with Docker

```bash
# 1. Start all services
docker-compose up -d

# 2. Access in browser
# - FastAPI: http://localhost:8000/docs
# - React: http://localhost:3000

# 3. Make code changes — hot reload works via volume mounts

# 4. When done
docker-compose down
```

## 🌐 Production Deployment Tips

| Tip | Description |
|-----|-------------|
| **Use `.env.production`** | Never commit real secrets to repo |
| **Health checks** | Add `HEALTHCHECK` to Dockerfile for orchestration |
| **Resource limits** | Add `--memory` and `--cpus` to `docker run` |
| **Log rotation** | Configure Docker logging or use external logger |
| **Backup database** | `docker exec sc-oam-prod pg_dump ... > backup.sql` |
| **Update strategy** | Use `docker pull` + `docker restart` for zero-downtime |

## 🔧 Customizing the Docker Image

### Add Python Dependencies

Modify `requirements.txt` or `requirements-dev.txt`, then rebuild:

```bash
docker build -t sc-oam-app:latest .
```

### Add Node Dependencies

Modify `web/package.json`, then rebuild the Node stage:

```bash
docker build --target node -t sc-oam-app:latest .
```

### Change Ports

Modify `docker-compose.yml` or `docker run -p` flags.

### Environment Variables

Set at runtime or in `.env` file:

```bash
# .env file (not committed)
DATABASE_URL="postgresql://..."
SECRET_KEY="..."
ENVIRONMENT="production"
BACKEND_CORS_ORIGINS="https://your-domain.com"
```

## 🗄️ Database Persistence

### SQLite (Development)

```yaml
# In docker-compose.yml or run with:
-e DATABASE_URL="sqlite:///./database.db"
```

SQLite data persists in the container's filesystem. For development only.

### PostgreSQL (Production)

```yaml
# docker-compose.yml includes PostgreSQL service
# Set DATABASE_URL in backend service:
#   DATABASE_URL="postgresql://oam_user:password@db:5432/sc_oam_db"
```

### Migration Strategy SQLite → PostgreSQL

1. **Development:** Use SQLite via `.env.example`
2. **Test:** Switch `DATABASE_URL` to PostgreSQL in `.env`
3. **Data export:** `pg_dump sc_oam_db > backup.sql` (from old SQLite if needed)
4. **Import:** Run backup into new PostgreSQL database
5. **Verify:** Run API tests against new database
6. **Deploy:** Use PostgreSQL in production Docker Compose

## 📈 Health Monitoring

### Container Health Check

Add to Dockerfile:

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s \
  CMD curl -f http://localhost:8000/health || exit 1
```

### Ports to Monitor

| Port | Service | Purpose |
|------|---------|---------|
| 8000 | FastAPI | API + docs |
| 3000 | React | Frontend |
| 5432 | PostgreSQL | Database (if used) |

### Logs

```bash
# View all container logs
docker-compose logs -f

# View specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Real-time tail
docker logs -f sc-oam-prod
```
