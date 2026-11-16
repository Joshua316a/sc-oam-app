# CHANGE-LOG-v0.1.md
# v0.1.0 (2026-11-16) — Initial QA-Validated Release

## ✨ Features (Inception → v1.0)
- Multi-environment distributed architecture prototype
- Base-port scheme with profile offsets (dev=+1, qa=+2, prod=+0)
- Docker compose configurations (dev/qa/prod/agent profiles)
- Entrypoint scripts (dev_entrypoint.sh, game_entrypoint.sh, prod_entrypoint.sh)
- Unified run.sh entry point: `./run.sh [dev|qa|prod] [core|gameagnt|web]`
- Architecture documentation with port scheme, agent/profile matrix, checklists
- 5/5 pytest tests passing (tests/api/test_blueprints.py)

## 🐛 Fixes
(None — initial release)

---
*This file is linked from CHANGE-LOG.md: [v0.1.0](CHANGE-LOG.md)*
