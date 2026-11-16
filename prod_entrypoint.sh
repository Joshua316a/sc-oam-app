#!/bin/bash
# ============================================================================
# prod_entrypoint.sh - Production Entrypoint
#
# Purpose: Runs the OAMv2 backend application in production mode.
#          Self-contained - no external mounts, no auto-reload,
#          everything inside the Docker image.
#
# Key Behavior:
#   - No source code mounts - all code inside Docker image
#   - No --reload flag - stable, predictable production behavior
#   - Production-grade uvicorn worker configuration
#   - Designed for VPS, cloud container, or hosting deployment
#
# Usage: This is set as the `entrypoint` in docker-compose.prod.yml
#        and the `command` runs uvicorn in production mode.
# ============================================================================

set -e

echo "🚀 Starting OAMv2 backend (production mode)..."

# Ensure /app directory exists
mkdir -p /app

# Run uvicorn in production mode
# No --reload flag (production stability)
# Use production worker class for better performance
exec python -m uvicorn app:app \
  --host 0.0.0.0 \
  --port 8000 \
  --worker-class ucinfo:uvicorn.workers.UvicornWorker \
  --log-level warning