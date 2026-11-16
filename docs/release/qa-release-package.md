# 📦 sc-oam-app QA Release Package

**Phase:** v0.1.0  
**Purpose:** Production-ready build setup for Quality Assurance testing  
**Developer → QA Handoff**  

---

## 🎯 Overview

This release package provides QA with a **black-box** test environment for sc-oam-app. QA receives a configured application where:

- **White-box knowledge**: QA understands the internal architecture, test levels (L1-L5), and integration testing methodology (Phase 1/Phase 2)
- **Black-box testing**: QA tests the application as an end-user would, without needing to modify source code or backend configuration beyond what's provided
- **Role boundary**: Release Manager (QA) takes over from Developer at the deployment boundary — QA handles environment setup, smoke tests, and release sign-off; Developer owns the code and mockup/production service transition

---

## 📋 Contents of Release Package

| Item | Description | QA Responsibility |
|------|-------------|-------------------|
| **Built Docker Image** | `sc-oam-app:prod` image (or Docker Compose config) | Load and run |
| **Environment Configuration** | `.env.production` with placeholders | Fill in credentials for testing |
| **Authentication Setup Guide** | See section below | Configure OAuth/RSI/local auth |
| **Test Instructions** | Step-by-step QA test scenarios | Execute test cases |
| **Smoke Test Checklist** | Pre-release verification items | Validate before sign-off |
| **Rollback Instructions** | How to stop/uninstall | Clean environment reset |

---

## 🔐 Authentication Setup for QA

QA needs to configure exactly **one** authentication method to fully test the application. The application ships with **graceful sandbox defaults** — all three auth methods work without configuration but show "not configured/inactive" status.

### **Option 1: Local/OS Keychain (Easiest — No Config Needed)**

| **What QA Gets** | OS Keychain login card in prototype UI |
|------------------|----------------------------------------|
| **Setup Required** | None — works out of the box |
| **Test Path** | 1. Open `http://localhost:3000/auth-prototype.html`<br>2. Enter test user identifier (e.g., "testuser")<br>3. Click "Test OS Keychain Login"<br>4. Observe graceful sandbox message |
| **Expected Result** | Success message + auth status updates to "Active" for OS tier |
| **Use Case** | Quick verification; no external dependencies |

### **Option 2: Google OAuth (Requires Google Cloud Credentials)**

| **What QA Gets** | Auth prototype with Client ID/Secret input fields |
|------------------|---------------------------------------------------|
| **Setup Required** | 1. Create Google Cloud Console project<br>2. Add OAuth 2.0 credentials<br>3. Add values to `.env.production` |
| **Test Path** | 1. Open `http://localhost:3000/auth-prototype.html`<br>2. Enter Google Client ID & Secret in the OAuth card<br>3. Enter scope (optional, default: "profile email")<br>4. Click "Initiate Google OAuth"<br>5. Observe initiation message (mockup returns test user data) |
| **Expected Result** | Success message + auth status updates to "Active" for Google tier + user profile displayed |
| **Use Case** | Full OAuth flow testing; requires Google Cloud project |

**To Configure Google OAuth:**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Navigate to **APIs & Services → Credentials**
4. Click **Create Credentials → OAuth 2.0 Client ID**
5. Select **Web application**
6. Authorized redirect URIs: `http://localhost:8000/api/auth/google/callback`
7. Note down:
   - **Client ID**: `123456789-app.apps.googleusercontent.com`
   - **Client Secret**: `GOCSPX-...`
8. Add to `.env.production`:
   ```env
   GOOGLE_CLIENT_ID="123456789-app.apps.googleusercontent.com"
   GOOGLE_CLIENT_SECRET="GOCSPX-..."
   ```
9. Restart the backend: `docker restart sc-oam-app-backend-1`

### **Option 3: RSI Account (Requires RSI Package + Token Key)**

| **What QA Gets** | Auth prototype with SC_OAM_TOKEN_KEY input field |
|------------------|--------------------------------------------------|
| **Setup Required** | 1. Install `rsi` Python package<br>2. Generate SC_OAM_TOKEN_KEY<br>3. Add to `.env.production` |
| **Test Path** | 1. Open `http://localhost:3000/auth-prototype.html`<br>2. Enter SC_OAM_TOKEN_KEY in the RSI card<br>3. Enter RSI username & password<br>4. Select mode: "standard", "refresh", or "hangar"<br>5. Click "Test RSI Login" |
| **Expected Result** | Login result based on mode (standard: auth success/failure; refresh: cached credentials; hangar: ship data) |
| **Use Case** | RSI pledge hangar data testing; requires `rsi` package installed |

**To Configure RSI Integration:**

1. Install the rsi package:
   ```bash
   pip install rsi
   ```
2. Generate a fernet key (or use existing):
   ```bash
   .venv/bin/python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
   ```
   Or use existing key from `.pyrsi_session`
3. Add to `.env.production`:
   ```env
   SC_OAM_TOKEN_KEY="your-fernet-key-base64-string-here"
   ```
4. Restart the backend: `docker restart sc-oam-app-backend-1`

### **Option 4: No Authentication (Sandbox Mode — Default)**

| **What QA Gets** | All three auth cards visible; status shows "inactive/not configured" |
|------------------|---------------------------------------------------------------------|
| **Setup Required** | None — application runs immediately |
| **Test Path** | 1. Open `http://localhost:3000/auth-prototype.html`<br>2. Click any auth method button<br>3. Observe sandbox graceful messages |
| **Expected Result** | Informational messages; auth status tri-tier shows all tiers inactive |
| **Use Case** | Initial verification; no config needed; demonstrates graceful degradation |

---

## 🏗️ Build Management Instructions

### **For QA to Create Test Environment from Sources**

#### **Prerequisites**

| **Requirement** | **Version** | **Installation** |
|----------------|-------------|------------------|
| Docker Desktop / Engine | 20.10+ | docker.com |
| Docker Compose | v2+ | Included with Docker Desktop |
| Node.js | 18+ | nodejs.org |
| Python 3.10+ | 3.10+ | python.org |
| Git | Latest | git-scm.com |

#### **Step 1: Clone the Repository**

```bash
git clone https://github.com/your-org/sc-oam-app.git
cd sc-oam-app
```

#### **Step 2: Build the Development Environment**

```bash
# From project root
docker build -t sc-oam-app:dev .
```

#### **Step 2: Start the Services**

```bash
# Start Docker Compose (recommended for QA)
docker-compose up -d

# Or start manually:
# Backend
docker run -d \
  -p 8000:8000 \
  -v $(pwd):/app \
  -e ENVIRONMENT=development \
  --name sc-oam-dev \
  sc-oam-app:dev

# Frontend (separate terminal)
cd web && npm run dev
# Access at: http://localhost:3000
```

#### **Step 3: Configure Authentication**

QA selects **one** of the four options above:

- **No config needed**: OS Keychain works immediately
- **Google OAuth**: Fill `.env.production` with Google Cloud credentials
- **RSI Integration**: Install `rsi` package + configure token key
- **Sandbox mode**: No config needed — default behavior

#### **Step 4: Verify Environment**

```bash
# Check backend health
curl -s http://localhost:8000/health

# Check auth status
curl -s http://localhost:8000/api/auth/status

# Frontend should be at http://localhost:3000/auth-prototype.html
```

---

## 📝 QA Test Scenarios

### **Functional Testing**

| **Scenario** | **Auth Method** | **Expected** |
|-------------|-----------------|-------------|
| **Q1: Login via OS Keychain** | Local/OS | Success message + status updates |
| **Q2: Initiate Google OAuth** | Google (with creds) | OAuth initiation message + status update |
| **Q3: Test RSI Login (standard mode)** | RSI (with token key) | Login result based on credentials |
| **Q4: View Auth Status** | Any | Tri-tier status displayed (OS, Google, RSI) |
| **Q5: Blueprint CRUD** | Any (unauthenticated or auth) | Create/Read/Update/Delete blueprints |
| **Q6: Extraction Pipeline** | Any | Run extraction, verify database persistence |

### **Error Handling Testing**

| **Scenario** | **Expected Behavior** |
|-------------|----------------------|
| **Q7: Invalid Google Credentials** | Error message + status stays "not configured" |
| **Q8: Missing RSI credentials** | "RSI integration not available" message |
| **Q9: Empty credential fields** | Validation error (422) |
| **Q10: Network failure** | Graceful error message; app doesn't crash |

### **White Box Context for QA**

QA has been briefed on the following internal knowledge (from test plan):

- **L1-L4 test levels** and what they cover
- **Phase 1/Phase 2 integration methodology** — understands mockup vs production
- **L5 External Service Integration** — knows mockup contract testing was done
- **Test pyramid** — 70% unit/integration, 20% component, 10% end-to-end
- **Database agnosticism** — tests run against SQLite (default) or PostgreSQL
- **AI-friendly test patterns** — QA can read and understand test fixtures

### **Black Box Testing Boundary**

QA treats the application as a black box:

- ✅ Can start/stop the environment
- ✅ Can configure authentication methods
- ✅ Can execute test scenarios and verify outcomes
- ✅ Can report bugs/issues
- ❌ Should NOT modify source code
- ❌ Should NOT change backend configuration beyond `.env.production`
- ❌ Should NOT alter test fixtures or pytest/vitest configurations
- ❌ Should NOT access internal API docs beyond provided endpoints

---

## 🔄 Release Package Handover Boundary

### **Developer (Completed Before Handover)**

| **Done** | **Artifact** |
|----------|--------------|
| ✅ Source code tagged at v0.1.0 | `git tag v0.1.0` |
| ✅ Docker image built | `sc-oam-app:prod` |
| ✅ Test plan updated | `docs/project/testing/test-plan.md` |
| ✅ QA release package created | `docs/release/qa-release-package.md` |
| ✅ Authentication options documented | Above + inline in prototype |
| ✅ Smoke test checklist prepared | See below |
| ✅ CI/CD passing | GitHub Actions on v0.1.0 tag |

### **QA (Takes Over at Handover)**

| **Starts Here** | **Responsibility** |
|-----------------|-------------------|
| ✅ Load Docker image / docker-compose | Environment setup |
| ✅ Configure `.env.production` | Authentication credentials |
| ✅ Execute smoke test checklist | Validate environment |
| ✅ Run functional test scenarios | Functional verification |
| ✅ Report issues/bugs | GitHub Issues |
| ✅ Validate release readiness | Sign-off or request fixes |
| ✅ Deploy to production (if applicable) | Production deployment |
| ✅ Final release sign-off | CHANGE-LOG + version tag |

### **Smoke Test Checklist (QA Pre-Sign-off)**

| **#** | **Check** | **Pass** |
|------|-----------|----------|
| **S1** | Docker compose `up -d` starts without errors | ☐ |
| **S2** | Backend health: `http://localhost:8000/health` returns OK | ☐ |
| **S3** | Frontend at `http://localhost:3000/auth-prototype.html` loads | ☐ |
| **S4** | Auth status API: `http://localhost:8000/api/auth/status` responds | ☐ |
| **S5** | OS Keychain login produces a message (sandbox) | ☐ |
| **S6** | Google OAuth card visible with input fields | ☐ |
| **S7** | RSI token key input field visible | ☐ |
| **S8** | Navigation between Blueprints/Crafting/Warehouse/Hangar pages works | ☐ |
| **S8** | Pytest: `5/5 tests passing` (verify with `.venv/bin/pytest -q tests/api/test_blueprints.py`) | ☐ |

---

## 📬 QA Feedback Loop

### **When QA Finds Issues**

1. **Document** the issue in GitHub Issues with:
   - Title: `QA: [Area] - [Description]`
   - Environment: Docker version, OS, credentials used (if auth-related)
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots/logs if applicable

2. **Developer** addresses the issue:
   - Pushes fix to v0.1.0 branch
   - May rebuild Docker image if backend changes
   - Updates `.env.production` if auth config changes

3. **QA** re-verifies:
   - Re-runs smoke test checklist
   - Confirms fix resolves the issue
   - Verifies no regressions

4. **Release Sign-off**:
   - QA confirms all P0/P1 objectives met
   - CHANGE-LOG v0.1.0 updated
   - Version tag `v0.1.0-final` created
   - Release package handed to operations/production

---

## 📞 QA Contact & Support

| **Role** | **Contact** | **Response Time** |
|----------|-------------|-------------------|
| **Developer** (source code, mockup/production service questions) | Developer session lead | Within 24 hours |
| **Release Manager** (environment setup, deployment) | QA lead | Within 24 hours |
| **CI/CD System** (build failures, test regressions) | GitHub Actions | Immediate (auto-blocks PRs) |

---

## 🎯 QA Exit Criteria

The QA release package is considered **complete** when **all** of the following are met:

- [ ] Docker environment running and accessible (backend + frontend)
- [ ] Authentication configured (at least one method working or sandbox mode verified)
- [ ] Smoke test checklist: all items pass
- [ ] Functional test scenarios: all scenarios executed
- [ ] Error handling verified (invalid inputs, missing configs)
- [ ] Database agnosticity verified (SQLite works; PostgreSQL optional)
- [ ] CHANGE-LOG v0.1.0 updated
- [ ] Version tagged `v0.1.0-final`
- [ ] QA sign-off documented

---

*This release package is the boundary between developer-owned code/mockups and QA-owned testing environment. Beyond this point, QA is responsible for environment management, test execution, and release sign-off.*