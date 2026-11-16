#!/bin/bash
# ============================================================================
# run.sh - Unified Development/QA/Production Entry Point
#
# Purpose: Selects and starts the appropriate Docker compose configuration
#          based on environment and agent arguments.
#
# Usage:
#   ./run.sh [dev|qa|prod] [core|gameagnt|web]
#   ./run.sh [dev|qa|prod] [core|gameagnt|web] --base-port PORT --frontend-port PORT
#
#   # Development with core OAMv2 (source mounts, auto-reload, default ports)
#   ./run.sh dev core
#
#   # QA testing (built artifacts, PostgreSQL, default ports)
#   ./run.sh qa core
#
#   # Production self-contained deployment (default ports)
#   ./run.sh prod core
#
#   # Development with custom base port
#   ./run.sh dev core --base-port 9000
#
#   # QA with custom base and frontend port
#   ./run.sh qa core --base-port 9000 --frontend-port 3003
#
#   # Development with game extraction agent
#   ./run.sh dev gameagnt
#
#   # Development with web UI (starts automatically with core)
#   ./run.sh dev web
#
# Key Features:
#   - Different container name prefixes enable simultaneous environments
#     (sc-oam-dev- vs sc-oam-qa- vs sc-oam-prod-)
#   - Profiles (dev/qa/prod) control source mounts, database, reload behavior
#   - Agents (core/gameagnt/web) define role in distributed system
#   - Base port configuration: change one or both variables to shift all ports
#     across all profiles simultaneously
#   - Default port assignments (SERVICE_BASE_PORT / SERVICE_FRONTEND_PORT):
#       dev:     8001 / 3001  (offset +1 from base 8000/3000)
#       qa:      8002 / 3002  (offset +2 from base 8000/3000)
#       prod:    8000 / 3000  (offset +0 from base 8000/3000)
#   - Example: ./run.sh dev core --base-port 9000 --frontend-port 3003
#     → dev backend: 9001, dev frontend: 3003
# ============================================================================

set -e

# Version from single source of truth: _version.py
VERSION=$(python3 -c "from _version import __version__; print(__version__)")

# Color output helpers
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default base port and frontend port
DEFAULT_BASE_PORT="8000"
DEFAULT_FRONTEND_PORT="3000"

# Parse arguments
ENVIRONMENT=""
AGENT=""
BASE_PORT=""
FRONTEND_PORT=""

# Process arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        dev|qa|prod)
            if [ -z "$ENVIRONMENT" ]; then
                ENVIRONMENT="$1"
            else
                echo -e "${RED}❌ Error:${NC} Multiple environment arguments specified"
                usage
            fi
            shift
            ;;
        core|gameagnt|web)
            if [ -z "$AGENT" ]; then
                AGENT="$1"
            else
                echo -e "${RED}❌ Error:${NC} Multiple agent arguments specified"
                usage
            fi
            shift
            ;;
        --base-port)
            BASE_PORT="$2"
            shift 2
            ;;
        --frontend-port)
            FRONTEND_PORT="$2"
            shift 2
            ;;
        --help|-h)
            usage
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Error:${NC} Unknown argument: $1"
            usage
            exit 1
            ;;
    esac
done

# Validate ENVIRONMENT argument
if [ -z "$ENVIRONMENT" ]; then
    echo -e "${RED}❌ Error:${NC} Environment argument required"
    usage
fi

if [[ ! "$ENVIRONMENT" =~ ^(dev|qa|prod)$ ]]; then
    echo -e "${RED}❌ Error:${NC} Invalid environment: $ENVIRONMENT"
    echo -e "${YELLOW}Must be one of: dev, qa, prod${NC}"
    usage
fi

# Validate AGENT argument
if [ -z "$AGENT" ]; then
    echo -e "${RED}❌ Error:${NC} Agent argument required"
    usage
fi

if [[ ! "$AGENT" =~ ^(core|gameagnt|web)$ ]]; then
    echo -e "${RED}❌ Error:${NC} Invalid agent: $AGENT"
    echo -e "${YELLOW}Must be one of: core, gameagnt, web${NC}"
    usage
fi

# Set base port (use default if not specified)
if [ -z "$BASE_PORT" ]; then
    BASE_PORT="$DEFAULT_BASE_PORT"
fi

# Set frontend port (use default if not specified)
if [ -z "$FRONTEND_PORT" ]; then
    FRONTEND_PORT="$DEFAULT_FRONTEND_PORT"
fi

# Display startup banner
echo ""
VERSION=$(python3 -c "from _version import __version__; print(__version__)")
echo -e "${GREEN}🚀 sc-oam-app ${ENVIRONMENT}/${AGENT}${NC}"
echo -e "   Version: ${VERSION}"
echo -e "   Base PORT: ${BASE_PORT}  |  Frontend PORT: ${FRONTEND_PORT}"
echo -e "   Service: sc-oam-app${NC}"
echo ""

# Calculate profile-specific port offsets
# Formula: dev=1, qa=2, prod=0 (added to the BASE_PORT/FRONTEND_PORT by the compose files)
# This is handled by the compose files referencing ${SERVICE_BASE_PORT} and ${SERVICE_FRONTEND_PORT}
# which are exported as env vars below.

# Export environment variables for docker compose
export SERVICE_BASE_PORT="${BASE_PORT}"
export SERVICE_FRONTEND_PORT="${FRONTEND_PORT}"

# Build the docker compose command
COMPOSE_COMMAND="docker compose \
  -f docker-compose.yml \
  -f docker-compose.${ENVIRONMENT}.yml \
  -f docker-compose.agent.${AGENT}.yml \
  up --build"

# Display composition info
echo -e "   BLUEStarting compose with:${NC}"
echo "   - Base: docker-compose.yml (exports SERVICE_BASE_PORT, SERVICE_FRONTEND_PORT)"
echo "   - Profile: docker-compose.${ENVIRONMENT}.yml"
echo "   - Agent: docker-compose.agent.${AGENT}.yml"
echo "   - SERVICE_BASE_PORT=$BASE_PORT, SERVICE_FRONTEND_PORT=$FRONTEND_PORT"
# Determine the effective ports based on profile offset
case "$ENVIRONMENT" in
    dev) echo "   - Effective ports - backend: ${BASE_PORT} (+1 offset), frontend: ${FRONTEND_PORT} (+1 offset)" ;;
    qa) echo "   - Effective ports - backend: ${BASE_PORT} (+2 offset), frontend: ${FRONTEND_PORT} (+2 offset)" ;;
    prod) echo "   - Effective ports - backend: ${BASE_PORT} (+0 offset), frontend: ${FRONTEND_PORT} (+0 offset)" ;;
esac
echo ""

# Execute the compose command
echo -e "   ${BLUE}▶️  Launching sc-oam-app ${ENVIRONMENT}/${AGENT}...${NC}"
echo "   (Ctrl+C to stop, logs: docker compose logs -f)"
echo ""

# Run docker compose
$COMPOSE_COMMAND

# If we get here, compose was stopped
echo ""
echo -e "${YELLOW}🛑 sc-oam-app ${ENVIRONMENT}/${AGENT} stopped${NC}"
echo ""
echo "To restart with same settings:"
echo "  ./run.sh ${ENVIRONMENT} ${AGENT} --base-port ${BASE_PORT} --frontend-port ${FRONTEND_PORT}"
echo ""
echo "To restart with defaults:"
echo "  ./run.sh ${ENVIRONMENT} ${AGENT}"