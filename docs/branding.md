# sc-oam-app Branding Guidelines

## 🎨 Visual Identity

### Project Name
- **Full name**: `sc-oam-app`
- **Styling**: Lowercase, hyphenated, no quotes
- **Abbreviation**: `sc-oam` (use full name for formal contexts)
- **Trademark**: © 2026 Your Organization. All rights reserved.

### Version Format
- **Scheme**: `major.minor.patch` (e.g., `0.1.0`, `1.0.0`, `0.2.0`)
- **Displayed as**: `sc-oam-app v0.1.0` (spoken: "sc-oam-app version nought point one zero")
- **Git tags**: `v0.1.0`, `v1.0.0` (with `v` prefix)

### Logo / Symbol
- **Current**: Text-based: `sc-oam-app` in project's distinctive typography
- **Usage**: GitHub Wiki header, README badges, Docker labels
- **Minimum size**: 16x16 pixels at readable scale
- **Clearspace**: Minimum clear space around logo equal to the `x` height of the lowercase `a`
- **Backgrounds**: Works on white (`#F8FAFC`) and teal (`#0D9488`) backgrounds
- **Do NOT**: Rotate, outline, or add effects to the wordmark

### Color Palette
| **Purpose** | **Color** | **Hex** | **RGB** | **Usage** |
|-------------|-----------|---------|---------|-----------|
| **Primary** | Deep Teal | `#0D9488` | 13, 148, 136 | Buttons, active states, headers, main accents |
| **Secondary** | Citrus Orange | `#F97316` | 249, 115, 22 | Accents, highlights, link colors, call-to-action |
| **Accent** | Slate Gray | `#64748B` | 100, 116, 139 | Secondary text, dividers, inactive states |
| **Background** | Neutral White | `#F8FAFC` | 248, 250, 252 | Wiki pages, documentation backgrounds, modals |
| **Success** | Emerald Green | `#10B981` | 16, 185, 129 | Health check passing, successful operations |
| **Error** | Rose Red | `#EF4444` | 239, 68, 68 | Failed states, error messages, validation failures |
| **Warning** | Amber | `#F59E0B` | 245, 158, 11 | Warnings, caution notices, deprecated features |

**Color Usage Rules:**
- Primary dominates 60% of UI, secondary 30%, accent 10%
- Never use Primary and Error simultaneously in same context
- Accessibility: Minimum contrast ratio 4.5:1 for normal text, 3:1 for large text
- Dark mode compatible: All primary/secondary colors have light-on-dark variants

### Typography
- **Primary font**: System font stack (preferred: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`)
- **Headers**: Bold weight, maximum 75 characters per line
- **Body text**: Regular weight, 16px base size for web, 14px for CLI
- **Monospace**: `Fira Code`, `Consolas`, or `Source Code Pro` for code snippets

## 📦 Asset Specifications

### Logo Files (Create These)
| **File** | **Format** | **Dimensions** | **Purpose** |
|----------|-----------|---------------|-------------|
| `logo-primary.svg` | SVG | 256x256 px | Wiki header, release packages, README |
| `logo-icon.png` | PNG | 64x64 px | Favicons, small UI contexts |
| `logo-monochrome.svg` | SVG | 256x256 px | Dark mode, low-contrast contexts |

**SVG Content (text-based wordmark):**
```svg
<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256">
  <text x="0" y="160" font-family="system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="140" font-weight="bold" fill="#0D9488">
    sc-oam-app
  </text>
</svg>
```

### Badge Templates (Markdown)
Insert these into Wiki pages or README.md:

```markdown
<!-- Version Badge -->
[![version](https://img.shields.io/badge/v-0.1.0-0D9488)](https://github.com/your-org/sc-oam-app/releases)

<!-- License Badge -->
[![license](https://img.shields.io/badge/license-MIT-64748B)](LICENSE)

<!-- Python Badge -->
[![python](https://img.shields.io/badge/python-3.14-0D9488)](https://www.python.org)

<!-- FastAPI Badge -->
[![fastapi](https://img.shields.io/badge/fastapi-0.111+-009432)](https://fastapi.tiangolo.com)
```

### Icon Usage
- **Favicon**: `favicon.ico` (16x16 or 32x32) or `favicon.svg`
- **Apple Touch**: `apple-touch.png` (180x180)
- **Tile**: `mstile-150x150.png` (for Windows tiles)
- Place in repo root, reference from Wiki `img/` directory or HTML head

## 📄 Documentation Branding

### Wiki Home Page Structure
```markdown
# sc-oam-app

**Org Asset Manager — Distributed Development Architecture v0.1.0**

```bash
# Quickstart
./run.sh dev core
```

[![version](https://img.shields.io/badge/v-0.1.0-0D9488)](https://github.com/your-org/sc-oam-app/releases)
[![license](https://img.shields.io/badge/license-MIT-64748B)](LICENSE)
[![python](https://img.shields.io/badge/python-3.14-0D9488)](https://www.python.org)
```

## 🌐 Application Branding (Internal)

### FastAPI `/health` Endpoint Response
```json
{
  "status": "ok",
  "service": "sc-oam-app",
  "version": "0.1.0"
}
```

### Entrypoint Launch Banner
```bash
./run.sh dev core
# 🚀 sc-oam-app dev/core
# Base PORT: 8001  |  Frontend PORT: 3001
```

### Environment Variable Prefix
- All env vars referencing the app use `SC_OAM_` prefix for consistency
  - `SC_OAM_APP_NAME` = "sc-oam-app"
  - `SC_OAM_APP_VERSION` = "0.1.0"
  - `SC_OAM_DEPLOY_ENV` = "dev|qa|prod"

## 📦 Release Package Branding

### Archive Naming
- `sc-oam-app-v0.1.0.tar.gz` (source distributions)
- `sc-oam-app-0.1.0/` (extracted directory name)

### LOST+FOUND (Assets Included in Release)
```
sc-oam-app-v0.1.0/
├── LICENSE          ← MIT license text
├── README.md        ← Branded with badges, quickstart
├── docker-compose.yml
├── docker-compose.dev.yml
├── docker-compose.qa.yml
├── docker-compose.prod.yml
├── run.sh
├── app.py           ← FastAPI with title/version
├── Dockerfile
├── .env.example
└── docs/
    └── architecture/
        └── deployment.md
```

### Excluded from Release
- `.env` files (never commit secrets)
- `db/` directory (SQLite host persistence)
- `web/dist/` (built artifacts, regenerate via `npm run build`)
- `node_modules/` (install with `npm install`)
- `.pytest_cache/` (test artifacts)
- Large binary blobs

## 🎯 Brand Voice & Tone

| **Scenario** | **Voice** | **Example** |
|-------------|-----------|-------------|
| **Success/Health** | Optimistic, concise | `"sc-oam-app v0.1.0 — All systems operational"` |
| **Error/Failed** | Direct, solution-oriented | `"sc-oam-app: Validation failed — check input format"` |
| **Documentation** | Helpful, instructional | `"To get started with sc-oam-app, run: ./run.sh dev core"` |
| **CLI/Entrypoint** | Brief, action-oriented | `"🚀 sc-oam-app dev/core launching on ports 8001/3001"` |

### Do's and Don'ts
| **Do** | **Don't** |
|--------|----------|
| Use `sc-oam-app` (lowercase, hyphenated) | Use `SC-OAM-APP` or `ScOamApp` |
| Reference version as `v0.1.0` | Reference as `0.1.0` without context |
| Use primary color `#0D9488` for positive actions | Use red `#EF4444` for positive messaging |
| Keep brand mentions concise | Overbrand every sentence |
| Maintain consistent capitalization | Mix `SC-oam-app`, `sc-oam-app`, `Sc-oam-app` |

## 📏 Brand Compliance Checklist

Before releasing v0.x.y, verify:
- [ ] Logo files exist and are legible at small sizes
- [ ] Color palette is applied consistently across all assets
- [ ] Badges use correct hex codes and point to valid URLs
- [ ] Version strings follow `major.minor.patch` scheme
- [ ] `sc-oam-app` appears uniformly (no variant capitalizations)
- [ ] MIT license is included in release archives
- [ ] `/health` endpoint returns `{"status": "ok", "service": "sc-oam-app", "version": "0.1.0"}`
- [ ] `run.sh` banner includes app name and version
- [ ] Wiki home page has branding badges and project overview
- [ ] No IP-covered content in public-facing docs

## 🔄 Brand Evolution

### v0.1.0 (Current) — Foundation
- Text-based wordmark `sc-oam-app`
- Primary palette: teal `#0D9488` + orange `#F97316`
- Basic badge set (version, license, python, fastapi)
- `/health` endpoint with basic info
- `run.sh` with name + port info

### v1.0.0 (Planned) — Expanded
- Full logo asset suite (SVG + PNG variants)
- Extended color palette (including success/grey/warning)
- Additional badges (Docker pulls, test coverage)
- Comprehensive brand guidelines v2.0
- Potential merchandise consideration

### Future Considerations
- Wordmark animation for Wiki header
- Dark mode color palette variants
- Localization of brand materials
- Brand usage analytics (if open-source telemetry is desired)
- Community contribution brand guidelines

