# 🎯 sc-oam-apps Aspirations Tracker

**Purpose:** Track general ideas, aspirations, and future enhancement directions for the Star Citizen Organisation Asset Management application. These are conceptual goals that may become features in future versions.

---

## 📋 Overview

This document tracks aspirations and potential future developments for sc-oam-app. Each entry represents a concept that could enhance the application's capabilities, improve the user experience, or address architectural scalability. 

Aspirations are categorized by domain:
- **UI/UX** — User interface and experience enhancements
- **Architecture** — System design and distribution improvements  
- **Integration** — Third-party service connections
- **Features** — New functional capabilities

---

## 🌐 UI: Public/Private Split

### **Aspiration A1: Public Landing Page with Authenticated Private Section**

| **Aspect** | **Description** |
|------------|-----------------|
| **Goal** | Create a clear separation between public-facing content and authenticated-only features |
| **User Flow** | 1. Visit `/` → see public landing page<br>2. Click "Sign in" → redirected to auth flow<br>3. After auth → access private features |
| **Public Features** | - Help/About materials<br>- Guides and documentation<br>- Static content<br>- Guest preview of blueprints |
| **Private Features** | - Full blueprint CRUD<br>- Authentication-dependent data<br>- Personal configuration<br>- RSI hangar data<br>- Extraction pipeline |
| **Technical Implementation** | - Route protection middleware<br>- Auth guard on private routes<br>- Public routes unauthenticated<br>- Session management for authenticated flow |
| **Status** | 📝 Planned — UI redesign required |

### **Mockup Description**

```
+=================================================================+
|  PUBLIC LANDING PAGE                                            |
+=================================================================+
|  [Header]  [Help]  [About]  [Guides]  [Sign in]                |
|                                                                 |
|  ███████████████████████████████████████████████████████████  |
|  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█  |
|  █  Welcome to sc-oam-app  █  "Your Org Asset Manager"         █  |
|  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█  |
|  █  • Blueprint library preview  █  • Quality calculator      █  |
|  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█  |
|  █  • Extraction overview        █  • API status dashboard   █  |
|  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█  |
|  [Sign in]  [Register]  [Learn more]                            |
+=================================================================+

+=================================================================+
|  AUTHENTICATED SECTION (after Sign in)                          |
+=================================================================+
|  Welcome, [Username]!  |  [Logout]                           |
|                                                                 |
|  ███████████████████████████████████████████████████████████  |
|  █  My Blueprints  █  • Create new blueprint                   █  |
|  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█  |
|  █  My Hangar (RSI)  █  • View ships & items                    █  |
|  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█  |
|  █  Extraction  █  • Run pipeline  █  • View status            █  |
|  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█  |
|  [Account Settings]  [Auth Status]  [Logout]                    |
+=================================================================+
```

---

## 🏗️ Architecture: Distributed Agent Network

### **Aspiration A2: Distributed Agent Network Across Physical Hosts**

| **Aspect** | **Description** |
|------------|-----------------|
| **Goal** | Distribute OAM services across multiple physical machines, each hosting self-contained features |
| **Architecture** | - **Primary Host** (this Mac): Core services, database, authentication<br>- **Agent Nodes** (Windows gaming PC, other systems): Feature-specific services, game data, configuration<br>- **Communication**: Secured connections via Model Context Protocol, gRPC, or HTTPS REST |
| **Agent Assignments** | Each agent assigned one or more of: <br>- Blueprint service<br>- Crafting/Quality service<br>- Warehouse inventory service<br>- Hangar/RSI data service<br>- Extraction pipeline service |
| **Data Distribution** | - Game data resides on agent nodes where users play<br>- Primary host coordinates, aggregates, and provides central UI<br>- Synchronization via secured APIs |
| **Security Model** | - MCP (Model Context Protocol) or gRPC with mutual TLS<br>- Agent authentication via tokens/certificates<br>- Role-based access per agent<br>- Data encryption in transit |
| **Network Topology** | ```<br>                                  +------------------+\n</br>                                  |  Primary Host    |\n</br>                                  |  (this Mac)      |\n</br>                                  +------------------+\n</br>                                  +--------+---------+\n</br>                                  +--+  +  +--+    |\n</br>                                  |  |  |  |    |    |\n</br>                                  +--+  +  +--+    |\n</br>                                  |  |  |  |    |    |\n</br>                                  +--+  +  +--+    |\n</br>                                  +--------+---------+\n</br>                                  |       |         |\n</br>                                  |  Agent 1     |\n</br>                                  | (Windows PC)   |\n</br>                                  |  (Gaming)      |\n</br>                                  +----------------+\n</br>                                  +--------+---------+\n</br>                                  |  Agent 2     |\n</br>                                  | (Other system) |\n</br>                                  +----------------+```\n| **Status** | 📝 Planned — requires architecture redesign and Model Context Protocol/gRPC integration |
| **Key Challenges** | - Cross-platform agent compatibility (macOS/Windows)<br>- Secure inter-process communication<br>- Data consistency across distributed nodes<br>- Agent discovery and registration<br>- Network topology management |

### **Mockup Description**

```
+=================================================================+
|  DISTRIBUTED OAM ARCHITECTURE                                  |
+=================================================================|
|  +------------------+    HTTPS/gRPC    +------------------+|
|  |  Primary Host    | ---------------> |  Agent Node 1    || 
|  |  (this Mac)      |                |  (Windows PC)    || 
|  |  Core + DB + UI  |                |  (Gaming System) ||
|  +------------------+                +------------------|| 
|           |                           |                  |
|           |   HTTPS/gRPC      |                  |
|           |                           |                  |
|  +------------------+    HTTPS/gRPC  +------------------+|
|  |  Agent Node 2    |                |  Agent Node 3    || 
|  |  (Other System)  |                |  (Other System)  || 
|  +------------------+                +------------------+|
+=================================================================+

|  Communication Flow:                                            |
|  1. Agent 1 requests blueprint data from Primary Host           |
|  2. Primary Host queries database, returns formatted data        |
|  3. Agent 2 pushes warehouse updates to Primary Host            |
|  3. Primary Host aggregates all agent data for UI display        |
|  4. User interacts with UI → Primary Host → Agent(s) → Response  |
+=================================================================+
```

---

## 📦 Feature Aspirations

### **Aspiration F1: Extraction Pipeline Enhancement**

| **Aspect** | **Description** |
|------------|-----------------|
| **Goal** | Enhance the `.p4k` extraction pipeline to support more file types and edge cases |
| **Current** | Basic `.p4k` parsing for ships, inventory, blueprints |
| **Future** | - Additional `.p4k` format support<br>- Malformed file handling<br>- Incremental extraction<br>- Progress indicators<br>- Batch processing |
| **Status** | 📝 Idea |

### **Aspiration F2: Quality Calculator Enhancement**

| **Aspect** | **Description** |
|------------|-----------------|
| **Goal** | Expand quality calculation to include more resource types and weighting algorithms |
| **Current** | Basic quality calculation with min/max resources |
| **Future** | - Additional resource types<br>- Weighted algorithms<br>- Historical quality tracking<br>- User-configurable formulas<br>- Integration with crafting system |
| **Status** | 📝 Idea |

### **Aspiration F3: Blueprint Import/Export**

| **Aspect** | **Description** |
|------------|-----------------|
| **Goal** | Allow blueprint data exchange between OAM instances |
| **Current** | Local blueprint storage only |
| **Future** | - JSON import/export<br>- Shareable blueprint links<br>- Version tracking<br>- Community blueprint library |
| **Status** | 📝 Idea |

### **Aspiration F4: User Account System**

| **Aspect** | **Description** |
|------------|-----------------|
| **Goal** | Enhanced user account management with profiles, preferences, and settings |
| **Current** | Basic authentication (OS Keychain, Google OAuth, RSI) |
| **Future** | - User profiles with avatars<br>- Preferred settings per user<br>- Login history<br>- Session management<br>- Password recovery |
| **Status** | 📝 Idea |

---

## 📊 Prioritization Matrix

| **Aspiration** | **Impact** | **Complexity** | **Priority** | **Effort** |
|---------------|-----------|---------------|-------------|------------|
| A1: Public/Private UI | High | Medium | Medium | Medium |
| A2: Distributed Agents | Very High | Very High | Low | Very High |
| F1: Extraction Enhancement | Medium | Medium | Low | Medium |
| F2: Quality Calculator | Medium | Low | Medium | Low |
| F3: Blueprint Import/Export | Medium | Medium | Low | Medium |
| F4: User Account System | High | High | Medium | High |

**Priority Formula:** `(Impact × 2 - Complexity) / Effort`

---

## 🚀 Next Steps

### **Short-term (0-3 months)**
- [ ] Refine A1: Public/Private UI mockup and begin UI redesign
- [ ] Document A2: Detail agent communication protocols and security requirements
- [ ] Implement F2: Quality calculator enhancements (low complexity, high impact)

### **Medium-term (3-6 months)**
- [ ] Begin A2: Prototype agent-to-primary communication (gRPC/HTTPS)
- [ ] Implement F1: Extraction pipeline edge case handling
- [ ] Begin F3: Blueprint import/export basic functionality

### **Long-term (6+ months)**
- [ ] Complete A2: Full distributed agent network prototype
- [ ] Implement F4: User account system with preferences
- [ ] Evaluate all aspirations for v1.0 or v2.0 roadmap

---


## ⚙️ Aspiration F5: Modular Code Organization (500-Line Cap)

### **Aspiration F5: Modular Code Organization with 500-Line Cap**

| **Aspect** | **Description** |
|------------|-----------------|
| **Goal** | Enforce a maximum file size of 500 lines per source file while maintaining full functionality and reusability. This improves navigation, testing, and maintenance. |
| **Modular Architecture** | Split the codebase into focused modules, each responsible for a single concern: |
| | • **Core API routes** — HTTP endpoints and request validation (< 500 lines) |
| | • **Service logic** — Business rules and data processing (< 500 lines) |
| | • **Data access** — Database queries and operations (< 500 lines) |
| | • **Utility functions** — Shared helpers and types (< 500 lines) |
| | • **UI components** — React components (< 500 lines) |
| **Reusability** | • Each module can be imported and used independently<br>• Common utilities extracted to shared modules<br>• No duplicated logic across files<br>• Clear dependency boundaries |
| **File Structure Example** | ```<br>api/<br>├── routes/<br>│   ├── blueprints.py     # 380 lines — CRUD endpoints<br>│   ├── auth.py           # 420 lines — auth flows<br>│   └── extraction.py     # 290 lines — pipeline control<br>│<br>├── services/<br>│   ├── blueprints.py     # 350 lines — business logic<br>│   ├── extraction.py     # 310 lines — pipeline implementation<br>│   └── quality.py        # 180 lines — quality calculations<br>│<br>└── models/<br>    ├── blueprint.py      # 250 lines — SQLAlchemy model<br>    └── quality.py        # 120 lines — quality types<br>``` |
| **Import Strategy** | • Explicit imports: `from api.services.blueprints import get_blueprints`<br>• Barrel modules (index.py style) for clean imports<br>• Type-safe interfaces between modules<br>• No circular dependencies |
| **Testing Benefits** | • Each module can be tested in isolation<br>• Mock only the specific module needed<br>• Faster test execution (only relevant modules)<br>• Clear test boundaries |
| **Status** | 📝 Planned — requires refactoring of existing code |

### **Implementation Path**

| **Phase** | **Action** | **Timeline** |
|----------|-----------|------------|
| **Phase 1: Analysis** | Profile current file sizes, identify >500-line files | 0-2 weeks |
| **Phase 2: Refactor** | Split largest files into modules, create import structure | 2-4 weeks |
| **Phase 3: Tooling** | Add import linter, enforce 500-line cap in CI | 4-6 weeks |
| **Phase 4: Migrate** | Move all files under cap, update all imports | 6-8 weeks |
| **Phase 5: Maintain** | Regular profiling, refactor as code grows | Ongoing |

### **Expected Benefits**

| **Benefit** | **Description** |
|------------|-----------------|
| **Navigate faster** | Find code quickly without scrolling through 500+ lines |
| **Test easier** | Isolate and test small, focused modules |
| **Refactor confidently** | Clear boundaries reduce ripple effects |
| **Onboard faster** | New developers understand small, focused modules |
| **Reduce bloat** | Natural limit on feature creep per file |
| **Improve readability** | Each file has a single, clear responsibility |

### **Challenges to Address**

| **Challenge** | **Mitigation** |
|-------------|---------------|
| **Initial refactor time** | Schedule as a dedicated sprint |
| **Import complexity** | Use barrel modules (`index.py`) for clean imports |
| **Dependency management** | Track module dependencies explicitly |
| **Partial refactoring risk** | Complete the refactor in one sprint, don't mix old/new |
| **Third-party library limits** | Some libraries naturally have large files; document exceptions |



## ⚡ Early Adoption Decision: F5 and Development UI

### **Decision: Adopt Aspiration F5 Now**

| **Reason** | **Explanation** |
|-----------|-----------------|
| **Early Development Stage** | Project is at v0.1.0 with minimal codebase size. Refactoring now avoids technical debt later. |
| **Low Refactor Cost** | Current file sizes are well under 500 lines. No existing files need breaking changes. |
| **Future-Proofing** | Establishing modular structure now prevents bloat as features (Phase 1/2, F1-F4) are added. |
| **UI Early Stage** | Prototype UI is still evolving. Having a 'Development' section built-in makes it easy to exclude when packaging production releases. |

### **Development UI Section Concept**

| **Aspect** | **Description** |
|------------|-----------------|
| **Purpose** | Separate prototype/test UI endpoints from production release packaging |
| **Development Section** | - `/dev/` route prefix in the FastAPI app<br>- Contains: Auth prototype, test endpoints, debug tools<br>- Only included in development/deployment target<br>- Omitted from production Docker image/tag |
| **Public vs Development** | - Public routes: `/api/blueprints`, `/api/health`, `/` <br>- Development routes: `/dev/auth-prototype`, `/dev/test-*` <br>- Both served by same codebase, different `ENVIRONMENT` flag |
| **Packaging Exclusion** | - Dockerfile: `FROM ...` with `ENVIRONMENT=production` omits dev routes<br>- `docker compose up` with `ENVIRONMENT=development` includes them<br>- Git: dev routes commented or in separate branch/tag |
| **Benefits** | - QA can test prototype features (`/dev/auth-prototype.html`)<br>- Production releases have no prototype UI endpoints exposed<br>- Single codebase, different deployment configs<br>- Easy to toggle `ENVIRONMENT=development|production` |

### **Implementation Sketch**

```python
# app.py — Environment-based route inclusion
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")

# Development routes — only included when ENVIRONMENT != "production"
if ENVIRONMENT != "production":
    app.include_router(dev_router, prefix="/dev", tags=["dev"])

# Existing routes always included
app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(blueprints_router, prefix="/api")
# ... etc
```

### **Status**

| **Item** | **Decision** |
|----------|-------------|
| **Adopt F5 (500-line cap)** | ✅ **Now** — Early development, low refactor cost |
| **Development UI Section** | 📝 Decide — UI still evolving, want input before implementing |
| **ENVIRONMENT flag** | 📝 To decide — `development` vs `production` toggle |

### **Next Steps**

1. **Adopt F5 immediately** — Begin modularizing files over 500 lines (currently none, but preventative)
2. **Decide on Development UI section** — Want input on whether to implement the `ENVIRONMENT` flag approach
3. **Update aspirations tracker** — Mark both as adopted/decided
4. **Communicate decision** — To all contributors and QA

---

*This decision record ensures clarity on why we're adopting F5 now and provides a framework for the Development UI section that can be implemented later based on team input.*

### **How to Contribute**

1. **Format** - Follow the template above
2. **Impact** - Describe the user or system benefit
3. **Complexity** - Rough estimate of development effort
4. **Priority** - Your assessment of importance
5. **Effort** - Estimated person-hours

Submit additions via:
- GitHub Discussion: "Aspiration: [title]"
- OR add directly to `docs/aspirations/aspirations-tracker.md`

---

*This aspiration complements the distributed agent architecture (A2) by ensuring that even when features are split across physical hosts, each host's codebase remains modular, testable, and maintainable with clear file size boundaries.*

---### **Status: Early Adoption Decisions**

| **Item** | **Decision** | **Rationale** |
|----------|-------------|---------------|
| **Adopt F5 (500-line cap)** | ✅ **Now adopted** | Project at v0.1.0, minimal codebase (~). Refactoring now avoids technical debt. Low cost to establish modular structure early. |
| **Development UI Section** | 📝 **Decide based on workflow** | QA workflow: Landing page → Dev section → Feature page → Setup env → Run test. Single-page-per-feature approach. Still evolving, input needed on implementation. |
| **ENVIRONMENT flag** | 📝 **Use Docker COMPOSE ENVIRONMENT** | Docker compose with Docker Desktop for manual control. No existing conventions—fresh start. Will use `ENVIRONMENT=development|production` toggle via docker compose variable. |

### **Next Steps**

1. ✅ **F5 adopted** — Begin modularizing (currently no files over 500 lines, but preventative; complements distributed agent architecture A2)
2. 📝 **Decide Development UI implementation** — Based on their workflow: Landing page → Dev section → Feature page → Setup env → Run test. Will use `ENVIRONMENT=development|production` via docker compose variable.
3. 📝 **Communicate decision** — To all contributors and QA (just the two of us, simple and scalable approach)

### **Development UI Workflow Details**

| **Step** | **Action** | **URL/Endpoint** | **Notes** |
|----------|------------|------------------|-----------|
| **a) Browse to Landing page** | Access root | `http://localhost:8000/` | Public landing page with overview |
| **b) Access Development section** | Click nav link | `http://localhost:8000/dev` | Dev-only route prefix |
| **c) Select feature 'page'** | Choose feature | `http://localhost:8000/dev/auth-prototype` | Single feature per page |
| **d) Setup environment for test** | Docker compose pull & start | `docker compose up -d` | Cross-platform check for Docker, pull pre-built containers |
| **e) Initiate test and view results** | Run the feature | Feature-specific URLs | Results displayed in UI |

### **Implementation Plan**

| **Aspect** | **Decision** |
|-----------|------------|
| **ENVIRONMENT variable** | `docker compose -f docker-compose.yml up -d` with `ENVIRONMENT=development` in docker-compose.yml (or override via `-e ENVIRONMENT=development`) |
| **Dev route prefix** | `/dev` prefix for all development routes |
| **Public routes** | `/api/blueprints`, `/api/health`, `/` — always included |
| **Dev routes** | `/dev/auth-prototype`, `/dev/test-*` — included when `ENVIRONMENT=development` |
| **Docker compose** | Add `ENVIRONMENT=development` to `docker-compose.yml` services, or override at runtime |
| **Production packaging** | `ENVIRONMENT=production` omits dev routes; `docker compose up` with prod tag |
| **QA workflow** | Land → Dev section → Feature page → `docker compose up` → Run test → View results |
| **Cross-platform setup** | Setup script checks Docker Desktop, pulls pre-built containers, starts compose |

### **Aspiration Adoption Summary**

| **Aspiration** | **Decision** | **Timing** |
|-------------|-------------|------------|
| **F5: 500-line cap** | ✅ Adopted now | Early development, preventative |
| **Dev UI Section** | 📝 Decided approach | Based on their workflow and Docker compose |
| **Production exclusion** | ✅ Will implement | Via `ENVIRONMENT` variable in docker compose |

### **Action Items**

1. **Adopt F5 immediately** — Begin modular code organization (preventative, low cost at v0.1.0)
2. **Implement Development UI section** — Add `/dev/` route prefix, ENVIRONMENT toggle, and single-feature-per-page design per their workflow
3. **Update Docker compose** — Add `ENVIRONMENT` variable configuration
4. **Communicate to QA** — Single developer scale, workflow as described
5. **Update aspirations tracker** — Mark both as adopted/decided, capture workflow details

---

*Decision recorded: Early adoption of F5 enabled by v0.1.0 stage. Development UI section designed around their Docker compose + single-feature-per-page workflow. Production exclusion via ENVIRONMENT variable. Simple and scalable for single-developer team.*




## ⚡ Aspiration F6: UI Style Guide and Theming

### **Aspiration F6: UI Style Guide and Theming**

| **Aspect** | **Description** |
|------------|-----------------|
| **Goal** | Establish a comprehensive UI style guide addressing control usage, theming, visual consistency, and accessibility for the sc-oam-app Web UI. This ensures a cohesive user experience across all pages and future features. |
| **Basis** | Assess the existing original UI as the foundation style guide, documenting: |
| | • Current color palette and typography<br>• Button styles and states (default, hover, active, disabled)<br>• Form field layouts and validation states<br>• Navigation menu structure and hierarchy<br>• Iconography and imagery conventions<br>• Dark/light theme considerations<br>• Responsive breakpoints and grid system<br>• Accessibility contrast ratios and ARIA labels |
| **Current UI Assessment** | Evaluate the prototype UI at `http://localhost:3000/auth-prototype.html` against the style guide criteria, documenting strengths and areas for improvement. |
| **Style Guide Sections** | 1. **Color System** - Primary, secondary, accent colors; dark/light mode<br>2. **Typography** - Font families, sizes, line heights, heading hierarchy<br>3. **Component Library** - Buttons, forms, modals, tables, navigation<br>4. **Spacing** - Margin/padding scales, grid gutters<br>5. **Accessibility** - Contrast ratios (WCAG AA/AAA), focus states, keyboard navigation<br>6. **Dark/Light Mode** - Color scheme switcher, prefers-color-scheme media query<br>7. **Icon System** - Custom icons, font icons, or SVG sprite usage |
| **Reusability** | • Style guide components can be reused across all pages<br>• Consistent theming ensures brand coherence<br>• Accessibility compliance reduces legal risk<br>• Documentation speeds up new feature development |
| **Tools** | • Storybook for component documentation<br>• Jest for visual regression testing<br>• Lighthouse for accessibility/performance scores<br>• CSS custom properties for theming |
| **Status** | 📝 Planned — UI already in use, style guide would formalize and future-proof |

### **Implementation Path**

| **Phase** | **Action** | **Timeline** |
|----------|-----------|--------------|
| **Phase 1: Assessment** | Document existing UI elements from prototype; identify inconsistencies | 1-2 weeks |
| **Phase 2: Documentation** | Write style guide with current UI as basis; add missing elements | 2-4 weeks |
| **Phase 3: Component Library** | Extract UI components to reusable library; add theming support | 4-6 weeks |
| **Phase 4: Integration** | Integrate style guide into all new features; deprecate inconsistent patterns | 6-8 weeks |
| **Phase 5: Maintenance** | Regular style guide updates; add new components as features grow | Ongoing |

### **Expected Benefits**

| **Benefit** | **Description** |
|------------|-----------------|
| **Visual Consistency** | All pages and features share the same design language |
| **Faster Development** | New features reference the style guide instead of reinventing styling |
| **Accessibility** | Formal compliance reduces risk and improves usability |
| **Brand Coherence** | Consistent theming reinforces product identity |
| **Faster Onboarding** | New developers can reference the style guide immediately |
| **Easier Refactoring** | Clear guidelines prevent accidental style drift |

### **Challenges to Address**

| **Challenge** | **Mitigation** |
|-------------|---------------|
| **Initial time investment** | Schedule as a dedicated 2-4 week sprint |
| **Existing inconsistency** | Style guide documents current state; future work fixes violations |
| **Tooling setup** | Storybook + Lighthouse setup requires initial configuration |
| **Dark mode complexity** | May require design system changes for color palettes |

### **Related Aspirations**

| **Aspiration** | **Connection** |
|---------------|----------------|
| **F5: Modular Code Organization** | Style guide components should be modular modules (< 500 lines) |
| **A1: Public/Private UI** | Style guide applies to both public landing and authenticated sections |
| **A2: Distributed Agents** | Consistent theming across all agent host UIs |
| **F2: Quality Calculator** | Style guide ensures consistent look for quality calculation results |

### **Priority**

| **Impact** | **Complexity** | **Priority** | **Effort** |
|-----------|---------------|-------------|------------|
| High | Medium | Medium | Medium |

### **Last Updated**

*Date*: [Current Date]

---

### **How to Contribute**

1. **Format** - Follow the template above
2. **Impact** - Describe the user or system benefit
3. **Complexity** - Rough estimate of development effort
4. **Priority** - Your assessment of importance
5. **Effort** - Estimated person-hours

Submit additions via:
- GitHub Discussion: "Aspiration: [title]"
- OR add directly to `docs/aspirations/aspirations-tracker.md`

---

*This aspiration establishes the visual and stylistic foundation for the application, ensuring consistency, accessibility, and maintainability as the UI evolves. It provides a single source of truth for all UI-related decisions and serves as the reference for implementing new features with consistent styling.*

---

---### **How to Contribute**

1. **Format** - Follow the template above
2. **Impact** - Describe the user or system benefit
3. **Complexity** - Rough estimate of development effort
4. **Priority** - Your assessment of importance
5. **Effort** - Estimated person-hours

Submit additions via:
- GitHub Discussion: "Aspiration: [title]"
- OR add directly to `docs/aspirations/aspirations-tracker.md`

---

*This document is a living tracker. Aspirations may be completed, revised, or removed as the project evolves. Last updated: *Date*"

---

## 📚 Related Documents

- [Test Plan](docs/project/testing/test-plan.md) — Testing strategy and levels
- [Release Package](docs/release/qa-release-package.md) — QA environment setup
- [Feature Handoff](FEATURE_HANDOFF.md) — Initial feature documentation
- [Architecture Overview](docs/architecture/overview.md) — System architecture

---

*This tracker is intended to complement, not replace, the formal test plan and development roadmap. It captures visionary ideas that may require significant redesign or may be deferred to future major versions.*

---



## ⚙️ A2: Distributed Agent Network for Extraction Pipeline

### **Aspiration A2: Distributed Agent Network for Extraction Pipeline**

| **Aspect** | **Description** |
|------------|-----------------|
| **Goal** | Set up a remote agent on a PC with the Game client installed that monitors game environment status and runs the extraction pipeline no earlier than 1 hour after a new update is made (ensuring installation has completed before running the extraction) and builds a local database for each environment. |
| **Architecture** | - **Remote Agent PC**: Runs the game client and extraction monitoring<br>- **Primary Host**: Coordinates extraction, hosts database, handles database replication<br>- **Communication**: HTTPS/REST or gRPC for status checks and pipeline triggers<br>- **Database**: PostgreSQL with built-in replication vs. SQLite (current 4GB+ size expected to grow)<br>- **Backup/Transfer**: DB-to-DB backup using native database replication instead of file copies |
| **Extraction Pipeline** | - Monitors game environment status<br>- Triggers extraction pipeline after 1-hour cooldown after update completion<br>- Builds local database for each environment<br>- Packages user configuration and game logs for transfer/backup |
| **Database Considerations** | - **SQLite**: Current OAMv1 database ~4GB, expected to grow; not ideal for network replication<br>- **PostgreSQL**: Supports native streaming replication, better for concurrent access, suitable for distributed setup<br>- **Replication**: Built-in PostgreSQL streaming replication vs. SQLite file copies |
| **Status** | 📝 Planned — requires remote agent setup, database architecture decision (SQLite vs. PostgreSQL), and 1-hour cooldown implementation |

### **Implementation Path**

| **Phase** | **Action** | **Timeline** |
|----------|-----------|------------|
| **Phase 1: Agent Setup** | Deploy remote agent on PC with game client; implement status monitoring | 2-4 weeks |
| **Phase 2: Extraction Trigger** | Implement 1-hour cooldown after update completion; trigger extraction pipeline | 4-6 weeks |
| **Phase 3: Database Architecture** | Evaluate SQLite vs. PostgreSQL; decide on retention vs. replication strategy | 6-8 weeks |
| **Phase 4: Configuration & Logs** | Implement configuration and log packaging for transfer/backup | 8-10 weeks |
| **Phase 5: Integration** | Integrate with existing extraction pipeline and agent network | 10-12 weeks |

### **Expected Benefits**

| **Benefit** | **Description** |
|------------|-----------------|
| **Automated Extraction** | No manual trigger needed; pipeline runs after 1-hour cooldown after update completion |
| **Database Scalability** | PostgreSQL replication supports growth beyond 4GB SQLite limit |
| **Data Safety** | Configuration and logs packaged alongside database for backup/transfer |
| **Distributed Operations** | Agent on game PC handles local data; primary host coordinates and aggregates |
| **Reduced Manual Overhead** | Automated pipeline vs. manual extraction triggers after each update |

### **Challenges to Address**

| **Challenge** | **Mitigation** |
|-------------|---------------|
| **Database Choice** | Evaluate PostgreSQL vs. SQLite based on growth expectations and replication needs |
| **Cooldown Implementation** | Ensure 1-hour cooldown after update completion before extraction triggers |
| **Agent Deployment** | Deploy and configure remote agent on game PC; ensure network connectivity |
| **Data Transfer** | Determine: keep databases on agent vs. transfer to primary host via replication |
| **Log Management** | Package and transfer game logs without impacting performance |

### **Related Aspirations**

| **Aspiration** | **Connection** |
|---------------|----------------|
| **F5: Modular Code Organization** | Extraction pipeline modules should adhere to 500-line cap |
| **A1: Public/Private UI** | Extraction results can be gated behind authenticated sections |
| **F1: Extraction Enhancement** | This aspiration extends the extraction pipeline with agent monitoring and cooldown |
| **F5: Code Organization** | Code modules for extraction, database, and agent communication should adhere to 500-line cap |

### **Priority**

| **Impact** | **Complexity** | **Priority** | **Effort** |
|-----------|---------------|-------------|------------|
| High | High | Medium | High |

### **Last Updated**

*Date*: [Current Date]

### **How to Contribute**

1. **Format** - Follow the template above
2. **Impact** - Describe the user or system benefit
3. **Complexity** - Rough estimate of development effort
4. **Priority** - Your assessment of importance
5. **Effort** - Estimated person-hours

Submit additions via:
- GitHub Discussion: "Aspiration: [title]"
- OR add directly to `docs/aspirations/aspirations-tracker.md`

---

*This aspiration complements the distributed agent architecture (A1) and the modular code organization (F5). It addresses the practical implementation of running extraction pipelines on remote agent PCs with proper cooldown, database architecture decisions, and configuration/log packaging.*

---
## 📝 How to Contribute

Aspirations are community-informed. To add a new aspiration:

1. **Format** - Follow the template above
2. **Impact** - Describe the user or system benefit
3. **Complexity** - Rough estimate of development effort
4. **Priority** - Your assessment of importance
5. **Effort** - Estimated person-hours

Submit additions via:
- GitHub Discussion: "Aspiration: [title]"
- OR add directly to `docs/aspirations/aspirations-tracker.md`

---

*This document is a living tracker. Aspirations may be completed, revised, or removed as the project evolves. Last updated: *Date*"

---

## 📚 Related Documents

- [Test Plan](docs/project/testing/test-plan.md) — Testing strategy and levels
- [Release Package](docs/release/qa-release-package.md) — QA environment setup
- [Feature Handoff](FEATURE_HANDOFF.md) — Initial feature documentation
- [Architecture Overview](docs/architecture/overview.md) — System architecture

---

*This tracker is intended to complement, not replace, the formal test plan and development roadmap. It captures visionary ideas that may require significant redesign or may be deferred to future major versions.*