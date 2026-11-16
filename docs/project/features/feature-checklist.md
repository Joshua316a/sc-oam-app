# 📋 Feature Checklist — sc-oam-app v0.1.0

## **Purpose**
Map old Tkinter OAM features to new sc-oam-app v0.1.0 implementation status. Track which features are implemented, planned, or out of scope.

## **📊 Feature Status Matrix**

| # | Old OAM Feature | sc-oam-app v0.1.0 Feature | Status | Category |
|---|----------------|---------------------------|--------|----------|
| **1** | **Ship Management** (4 of 200+ from old Tk DB) | Ship management system | ✅ **Complete** | Core |
| **2** | **Inventory Management** (2 of 5K+ from old Tk DB) | Inventory/warehouse management | ✅ **Complete** | Core |
| **3** | **Blueprint CRUD** | Blueprint create, read, update, delete | ✅ **Complete** | Core |
| **4** | **Crafting Quality** (0-1000 scale with tier tiers) | Crafting quality calculation | ✅ **Complete** | Core |
| **5** | **Warehouse Management** (items with quality field) | Warehouse inventory management | ✅ **Complete** | Core |
| **6** | **Database Pluggability** (SQLite ↔ PostgreSQL) | Database pluggability via DATABASE_URL | ✅ **Complete** | Core |
| **7** | **API Health Check** | API health check endpoint | ✅ **Complete** | Core |
| **8** | **CORS Configuration** (cross-origin settings) | CORS configuration | ✅ **Complete** | Core |
| **9** | **Error Responses** (standard error format) | Error responses using {detail: "..."} convention | ✅ **Complete** | Core |
| **10** | **API Versioning** (future /api/v1/... endpoints) | API versioning | ⏳ **Planned** | Future (v1.1.0+) |
| **11** | **Search/Filtering** (category query parameters) | Search/filtering with ?category=... query params | ⏳ **Planned** | Future (v1.1.0+) |
| **12** | **Multi-user Authentication** (OAuth + OS keychain) | Multi-user authentication | ❌ **Out of Scope** | Future (v1.1.0) |
| **12b** | **Token Vault / Keychain** (encrypted token storage) | Token vault / keyring integration | ⏳ **Planned** | Future (v1.1.0) |
| **13** | **Drag-and-Drop Blueprint Editing** (keyboard + forms) | Drag-and-drop blueprint editing | ❌ **Out of Scope** | Future (v1.2.0+) |
| **14** | **Advanced Reporting/Analytics** (CSV export only) | Advanced reporting/analytics | ❌ **Out of Scope** | Future (v1.2.0+) |
| **14b** | **JSON/CSV Export/Import** (download endpoints) | JSON/CSV export/import endpoints | ❌ **Out of Scope** | Future (separate utility) |
| **15** | **Real-time Collaboration** (multi-user support) | Real-time collaboration | ❌ **Out of Scope** | Future (v1.2.0+) |

## **📊 Status Summary**

| Status | Count | Percentage |
|--------|-------|------------|
| ✅ **Complete v0.1.0** | 8 | 44% |
| ⏳ **Planned v1.1.0+** | 7 | 39% |
| ❌ **Out of Scope v0.1.0** | 5 | 28% |
| **Total** | **18** | **100%** |

## **📋 Migration Note: Pilot Data Scaffold**

**⚠️ Important:** The 4 Ships and 2 Inventory Items migrated in v0.1.0 are **pilot migration data** from the old Tkinter OAM database, used for scaffold validation and API endpoint testing. The full game universe contains 200+ ships and 5,000+ inventory items, which are out of scope for v0.1.0 and planned for v1.1.0+ full data migration via the extraction pipeline.

| Status | Count | Percentage |
|--------|-------|------------|
| ✅ **Complete v0.1.0** | 8 | 44% |
| ⏳ **Pilot v0.1.0** | 2 | (subset of core features) |
| ⏳ **Planned v1.1.0+** | 2 | full data migration roadmap |
| ❌ **Out of Scope v0.1.0** | 5 | future considerations |
| **Total** | **15** | **100%** |

## **📦 Core v0.1.0 Features (Implemented)**

| # | Feature | sc-oam-app Endpoint | Test Status |
|---|---------|-------------------|-------------|
| **1** | 4 Ships → `/api/hangar/` | GET /api/hangar/ | ✅ 4 tests passing |
| **2** | 2 Inventory Items → `/api/warehouse/` | GET/POST/DELETE /api/warehouse/ | ✅ 4 tests passing |
| **3** | Blueprint CRUD → `/api/blueprints/` | Full CRUD endpoints | ✅ 4 tests passing |
| **4** | Quality Calculation 0-1000 | `/api/crafting/quality` | ✅ Implemented |
| **5** | Warehouse quality field (default 500) | `quality: Optional[int]` in models | ✅ Verified |
| **5** | Database Pluggability | SQLite ↔ PostgreSQL via `DATABASE_URL` | ✅ Verified (4 tests) |

## **🟡 Planned for v1.1.0+**

| # | Feature | Target Version | Dependencies |
|---|---------|----------------|--------------|
| **10** | API Versioning (`/api/v1/...`) | v1.1.0 | No breaking changes in v0.1.0 |
| **11** | Search/Filtering (`?category=...`) | v1.1.0 | UI + API enhancements |
| **12** | Multi-user Authentication | v1.1.0 | Google OAuth + keyring |
| **12b** | Token Vault / Fernet Encryption | v1.1.0 | `SC_OAM_TOKEN_KEY` env var |
| **13** | Full Ship Inventory Migration (pilot → v1.1.0+) | v1.1.0 | Extraction pipeline, .p4k parsing |
| **14** | Full Inventory Items Migration (pilot → v1.1.0+) | v1.1.0 | Extraction pipeline, .p4k parsing |
| **15** | User Authentication System | v1.1.0 | Google OAuth + keyring, OS keychain |
| **16** | Theming / Customization | v1.1.0 | Tailwind theme extended |
| **17** | User Preferences & Settings | v1.1.0 | User profiles, saved states |
| **18** | Event Planning / Calendar | v1.1.0 | API endpoints, scheduling |
| **19** | Print / Export Formats | v1.1.0 | PDF, CSV, JSON export |

## **❌ Out of Scope for v0.1.0**

| # | Feature | Reason for Scope Limitation |
|---|---------|-----------------------------|
| **O1** | Multi-user authentication | Requires PostgreSQL + auth system (v1.1.0) |
| **O1b** | Token Vault / Keyring integration | Depends on O1 + keyring library maturity |
| **O2** | Advanced reporting/analytics | Can be separate tool; CSV export sufficient v0.1.0; ⏳ Planned v1.1.0+ |
| **O3** | Drag-and-drop blueprint editing | Keyboard+form editing sufficient v0.1.0; v1.2.0+ |
| **O4** | Real-time collaboration | Single-user scope; multi-user v1.1.0+ |
| **O4b** | Real-time sync / conflict resolution | Requires multi-user auth (v1.1.0+) |
| **O4c** | Collaborative editing | Requires backend + frontend coordination v1.2.0+ |
| **O4d** | Presence / online indicators | Requires multi-user auth (v1.1.0+) |
| **O5** | Custom themes / branding | Default Tailwind theme sufficient v0.1.0 |
| **O5b** | Dark mode / light mode | Can be added v1.1.0 without breaking v0.1.0 |
| **O6** | Export/import JSON/CSV | Basic API handling sufficient v0.1.0 |
| **O6b** | JSON/CSV download endpoints | Can be separate utility endpoint |
| **O7** | Knowledge & Reference Materials | Knowledge base, recipes, guides | ⏳ **Planned** | Future (v1.1.0+) |
| **O7b** | Dedicated mobile app | Future consideration post-v1.0 |

## **📊 Feature Development Status Summary**

| Category | Count | Percentage |
|----------|-------|------------|
| ✅ Implemented in v0.1.0 | 8 | 50% |
| ⏳ Planned for v1.1.0+ | 10 | 56% |
| ❌ Out of scope v0.1.0 | 5 | 28% |
| **Total** | **18** | **100%** |

## **📋 Feature Mapping Old → New OAM**

| Old OAM Feature | New sc-oam-app Feature | Migration Status | Data Mapped |
|-----------------|-----------------------|----------------|-------------|
| **4 Ships** → `/api/hangar/` ships | ✅ Direct field mapping | ✅ Complete | 4 ships mapped |
| **2 Inventory Items** → `/api/warehouse/` items | ✅ Direct field mapping + quality field | ✅ Complete | 2 items mapped + quality=500 default |
| **Blueprints** → `/api/blueprints/` blueprints | ✅ Direct field mapping | ✅ Complete | Blueprint schema matches |
| **Quality Calculation** 0-1000 | ✅ Same scale, new formula | ✅ Complete | Formula: `base = q/1000`, `adj = (q-500)*0.001` |
| **Database pluggability** | ✅ Same models, different DB | ✅ Complete | `DATABASE_URL` switch |
| **Quality default 500** | ✅ New field with default | ✅ Complete | Default maps to "Uncommon" tier |
| **API Health Check** → `/api/health` | ✅ Direct endpoint mapping | ✅ Complete | Health check endpoint |
| **CORS Configuration** → `.env` `BACKEND_CORS_ORIGINS` | ✅ Config environment variable | ✅ Complete | CORS settings |
| **Error Responses** → `{detail: "..."}` convention | ✅ FastAPI convention | ✅ Complete | `{detail: "..."}` format |
| **Knowledge & Reference Materials** → Knowledge base, recipes, guides | ⏳ Planned v1.1.0+ | ⏳ Planned | Knowledge base planned for v1.1.0+ |
| **Multi-user Authentication** → OAuth 2.0 + OS keychain | ❌ Out of scope v0.1.0 | ❌ Out of scope | Requires PostgreSQL + auth system (v1.1.0) |
| **Token Vault / Keychain** → Fernet encryption + keyring | ❌ Out of scope v0.1.0 | ❌ Out of scope | Depends on multi-user auth + keyring maturity |
| **Advanced Reporting/Analytics** → CSV export only | ⏳ Planned v1.1.0+ | ⏳ Planned | Can be separate tool; CSV export sufficient v0.1.0 |
| **Drag-and-Drop Blueprint Editing** → Keyboard+form editing only | ❌ Out of scope v0.1.0; ⏳ v1.2.0+ | ❌ Out of scope v0.1.0; ⏳ v1.2.0+ | Keyboard+form editing sufficient v0.1.0 |
| **Real-time Collaboration** → Single-user scope | ❌ Out of scope v0.1.0 | ❌ Out of scope | Single-user scope; multi-user v1.1.0+ |
| **Custom themes / branding** → Default Tailwind theme | ✅ Sufficient v0.1.0 | ✅ Complete | Default Tailwind theme sufficient v0.1.0 |
| **Dark mode / light mode** → Theme switching | ⏳ Planned v1.1.0+ | ⏳ Planned | Can be added v1.1.0 without breaking v0.1.0 |
| **Export/import JSON/CSV** → Basic API handling | ✅ Sufficient v0.1.0 | ✅ Complete | Basic API handling sufficient v0.1.0 |
| **JSON/CSV download endpoints** → Separate utility endpoint | ⏳ Planned v1.1.0+ | ⏳ Planned | Can be separate utility endpoint |
| **Real-time sync / conflict resolution** → Requires multi-user auth | ❌ Out of scope v0.1.0 | ❌ Out of scope | Requires multi-user auth (v1.1.0+) |
| **Presence / online indicators** → Requires multi-user auth | ❌ Out of scope v0.1.0 | ❌ Out of scope | Requires multi-user auth (v1.1.0+) |
| **User Preferences & Settings** → User profiles, saved states | ⏳ Planned v1.1.0+ | ⏳ Planned | User profiles, saved states planned v1.1.0+ |
| **Event Planning / Calendar** → API endpoints, scheduling | ⏳ Planned v1.1.0+ | ⏳ Planned | API endpoints, scheduling planned v1.1.0+ |
| **Print / Export Formats** → PDF, CSV, JSON export | ⏳ Planned v1.1.0+ | ⏳ Planned | PDF, CSV, JSON export planned v1.1.0+ |

## **📋 Feature Checklist Usage**

- **For AI Agents**: Reference this checklist when implementing new features to ensure consistency with v0.1.0 scope
- **For Human Collaborators**: Use the checkboxes (`☐` / `✅`) to track feature implementation progress
- **For Roadmap Planning**: Use the "Planned" and "Out of Scope" categories to prioritize future sprints
- **For Feature Requests**: Check the matrix before submitting a new feature request to avoid duplication

**Last Updated**: 2026-11-12  
**Maintained by**: Primary User  
**Version**: v0.1.0 feature checklist  

