#!/bin/bash
# ============================================================================
# dev_entrypoint.sh - Development Shim Entrypoint
#
# Purpose: Runs the OAMv2 backend application from mounted host source code
#          with auto-reload capability for "edit on the fly" development.
#
# Key Behavior:
#   - Code lives on host, mounted into container via :ro volume
#   - uvicorn with --reload watches /app directory
#   - Any save on host triggers auto-reload (3-5 second delay)
#   - Frontend (Vite) runs on host with its own HMR
#
# Usage: This is set as the `entrypoint` in docker-compose.dev.yml
#        and the `command` includes --reload --reload-dir /app
# ============================================================================

set -e  # Exit on any error

echo "🔧 Starting OAMv2 backend (development mode with reload)..."

# Ensure /app directory exists (safety)
mkdir -p /app

# Run uvicorn with reload capability
# --reload: enables auto-reload on file changes
# --reload-dir /app: watches the /app directory (mounted from host)
# The app module is 'app:app' (from FastAPI app:app)
exec python -m uvicorn app:app \
  --host 0.0.0.0 \
  --port 8000 \
  --reload \
  --reload-dir /app \
  --log-level info