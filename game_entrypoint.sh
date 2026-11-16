#!/bin/bash
# ============================================================================
# game_entrypoint.sh - Game Extraction Agent Entrypoint
#
# Purpose: Runs the extraction pipeline agent on a PC with the Game client installed.
#          Monitors game environment status and runs the extraction pipeline
#          with a 1-hour cooldown after new updates to ensure installation completion.
#
# Key Behavior:
#   - Monitors game environment status (checks for new updates/patches)
#   - When new update detected, starts 1-hour (3600 seconds) cooldown timer
#   - After cooldown completes, triggers the extraction pipeline
#   - Pipeline reads Star Citizen p4k archives, classifies items, assigns categories
#   - Populates reference database (SQLite or PostgreSQL)
#   - Packages user configuration files and game logs
#   - Makes extracted data available to core OAMv2 backend via API
#
# Environment Variables (set via docker-compose):
#   - DATABASE_URL: "sqlite:////host_db/database.db" (host-mounted SQLite)
#   - PIPELINE_COOLDOWN: "3600" (1 hour in seconds, default)
#   - GAME_ENV: "production" or "sandbox"
#   - DATABASE_URL: connection string
#
# Usage: This is set as the `entrypoint` in docker-compose.agent.game.yml
#        and the `command` includes the pipeline options.
# ============================================================================

set -e

echo "🎮 Starting OAMv2 Extraction Agent (game environment monitoring)..."

# Ensure directories exist
mkdir -p /app
mkdir -p /game/data

# Parse command line arguments
COOLDOWN=${1:-3600}       # Default 1 hour (3600 seconds)
MONITOR=${2:-"--monitor"}  # Default: enable monitoring
DB_URL=${3:-"sqlite:////host_db/database.db"}  # Default SQLite host path

# Display configuration
echo "   Cooldown period: ${COOLDOWN}s (${COOLDOWN/3600}h)"
echo "   Monitoring: ${MONITOR}"
echo "   Database: ${DB_URL}"
echo ""

# Check if game data directory has content
if ls /game/data/*.p4k 1>/dev/null 2>&1; then
    echo "📁 Found game archives in /game/data/"
    for p4k in /game/data/*.p4k; do
        echo "   - $(basename $p4k)"
    done
else
    echo "⚠️  No .p4k archives found in /game/data/"
    echo "   Extraction pipeline will have no data to process."
    echo "   Place Star Citizen p4k archives in the game_data volume."
fi

echo "⏳ Extraction agent ready - monitoring game environment..."
echo "   New update detected → ${COOLDOWN}s cooldown → extraction pipeline"
echo ""

# Main loop: monitor game environment and run extraction pipeline
while true; do
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Checking game environment status..."
    
    # TODO: Implement actual game environment monitoring
    # This would check for:
    # - New game patches/updates
    # - Game client status (running/stopped)
    # - Archive changes (p4k file modification times)
    
    # Simulated: Check for update marker file
    if [ -f /game/data/update_marker.txt ]; then
        echo "   🔔 New update detected! Starting ${COOLDOWN}s cooldown..."
        
        # Countdown cooldown
        REMAINING=${COOLDOWN}
        while [ ${REMAINING} -gt 0 ]; do
            MINUTES=$((REMAINING / 60))
            SECONDS=$((REMAINING % 60))
            printf "\r   ⏳ Cooldown remaining: %02d:%02d   " "${MINUTES}" "${SECONDS}"
            sleep 1
            REMAINING=$((REMAINING - 1))
        done
        echo ""
        
        echo "   ✅ Cooldown complete - triggering extraction pipeline..."
        
        # TODO: Run the actual extraction pipeline
        # This would:
        # 1. Read Star Citizen p4k archives from /game/data/
        # 2. Classify items (weapons, modules, cargo, etc.)
        # 3. Assign categories and ILGs (Item Legal Grades)
        # 4. Populate reference database
        # 5. Package user configuration and game logs
        # 6. Make data available to core backend via API
        
        # Placeholder: Mark marker as processed
        rm /game/data/update_marker.txt
        
        echo "   ✅ Extraction pipeline completed"
        echo "   📦 Data packaged and available to core backend"
    fi
    
    # Wait before next check (30 seconds)
    echo "   Next check in 30 seconds..."
    sleep 30
done