# Code Style & Conventions

Consistent code style makes this project readable and maintainable for both human and AI collaborators.

## 🐍 Python — Ruff + Black + Isort

### Ruff (Linting)

```bash
# Check style (CI will also check)
ruff check .

# Auto-fix what Ruff can fix
ruff check . --fix

# Fix imports with Ruff
ruff check . --select I
ruff check . --select I --fix
```

### Black (Formatter)

```bash
# Check format (CI will also check)
black --check .

# Auto-format
black .
```

### Isort (Import ordering)

```bash
# Check import order
isort --check .

# Auto-fix
isort .
```

### Combined Check (recommended)

```bash
# Run all style checks
ruff check . && black --check . && isort --check .
```

## 📁 Python File Structure

```
modules/
├── __init__.py         # Package exports (controlled)
├── app.py              # FastAPI entry point
├── data_access.py      # Core data access layer
├── oam_categories.py   # 22 item categories + "All"
├── categories.py       # Category definitions
├── catalogue_builder.py# Catalogue building logic
├── blueprint_pool.py   # Blueprint pool management
├── full_extractor.py   # Data extraction from SC formats
├── deep_dive_query.py  # Advanced querying
├── log_analytics.py    # Log analysis and reporting
├── modes/              # Panel modes (base_mode.py + mixes)
├── panels/             # UI panels (template + implementations)
├── widgets/            # Reusable UI components
├── themes/             # Color/theme system
└── utils/              # Utility functions
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| **Modules** | `snake_case`, `lowercase` | `data_access.py` |
| **Classes** | `CamelCase` | `PlayerBlueprintsPanel` |
| **Functions** | `snake_case` | `calculate_quality()` |
| **Constants** | `UPPER_SNAKE_CASE` | `MAX_RETRIES = 60` |
| **Variables** | `lowercase_snake_case` | `blueprint_id` |
| **Enumerations** | `UPPER_SNAKE_CASE` | `class CraftingTier(Enum):` |
| **Files** | `lowercase_snake_case.py` | `player_blueprints_panel.py` |

### Type Hints

```python
# ✅ Preferred — always use type hints
def calculate_quality(
    base_quality: float,
    resource_qualities: dict[str, float],
    resource_weights: dict[str, float],
) -> float:
    ...

# ✅ OK — optional types where makes sense
def create_blueprint(
    blueprint_id: str,
    bp_name: str,
    category: str = "uncategorized",
    **kwargs: Any,
) -> BlueprintResponse:
    ...

# ❌ Avoid — bare types without hints
def old_style(data):
    return data[0]
```

### Docstrings

```python
"""
Follows numpy/docstring format.

Example
-------
>>> calculate_quality(500.0, {"element": 550.0}, {"element": 0.2})
525.0

Returns
-------
float: The calculated quality score (0-1000 range)
"""
```

## ⚛️ React + TypeScript

### File Structure

```
web/src/
├── App.tsx             # Main app component
├── main.tsx            # ReactDOM root
├── index.css           # Tailwind directives
├── index.html          # HTML entry point
├── components/
│   ├── Dashboard.tsx
│   ├── BlueprintList.tsx
│   ├── QualityCalculator.tsx
│   ├── FleetTable.tsx
│   ├── InventoryTable.tsx
│   └── (more components)
├── pages/              # Page-level components
│   ├── BlueprintsPage.tsx
│   ├── CraftingPage.tsx
│   ├── WarehousePage.tsx
│   └── HangarPage.tsx
├── hooks/              # Custom React hooks
├── lib/                # API clients, utils
├── types/              # TypeScript type definitions
│   └── api.ts          # API response types
├── App.css             # Component-specific styles (rare, use Tailwind instead)
└── main.css            # Global styles (use Tailwind)
```

### Component Naming

| Component | File | Exports |
|-----------|------|---------|
| **BlueprintList** | `BlueprintList.tsx` | `export const BlueprintsList = ...` |
| **QualityCalculator** | `QualityCalculator.tsx` | `export const CraftingCalculator = ...` |
| **FleetTable** | `FleetTable.tsx` | `export const FleetTable = ...` |
| **InventoryTable** | `InventoryTable.tsx` | `export const InventoryTable = ...` |

### Type Definitions

```typescript
// web/src/types/api.ts
export interface Blueprint {
  id: number
  blueprint_id: string
  bp_name: string
  category: string
  subcategory: string
  craft_type: string
  output_item_name: string
  quality_min: number
  quality_max: number
  craft_time_seconds: number
  ilg_label: string
  owner_handle: string
  acquired_date: string
  is_learned: boolean
  notes: string
}

export interface QualityCalculation {
  base_quality: number
  resource_qualities: Record<string, number>
  resource_weights: Record<string, number>
  final_quality: number
}

export interface ResourceRequirement {
  type: string
  amount: number
  count: number
  quality_selector: number
}
```

### Component Standards

```tsx
// ✅ Good — PascalCase component, camelCase props
interface QualityCalculatorProps {
  blueprintId: number
  onResult: (result: QualityCalculation) => void
}

export const QualityCalculator: React.FC<QualityCalculatorProps> = ({
  blueprintId,
  onResult,
}) => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const calculate = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`/api/crafting/quality`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          blueprintId,
          // ... other params
        }),
      })
      const data = await response.json()
      onResult(data)
    } catch (err) {
      setError("Calculation failed")
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <Spinner />

  return (
    <div className="p-6 bg-card border border-border">
      <h2 className="text-xl font-medium mb-3">Quality Calculator</h2>
      <button onClick={calculate} className="btn-primary">
        Calculate Quality
      </button>
      {error && <p className="text-destructive mt-2">{error}</p>}
    </div>
  )
}
```

## 🌿 Git Workflow

### Branch Naming

| Branch Type | Naming Pattern | Example |
|-------------|----------------|---------|
| **Feature** | `feature/<short-description>` | `feature/blueprint-crud` |
| **Bug fix** | `fix/<issue-description>` | `fix/quality-calculation` |
| **Documentation** | `docs/<topic>` | `docs/api-reference` |
| **Hotfix** | `hotfix/<urgent-fix>` | `hotfix/security-patch` |
| **Release** | `release/vX.Y.Z` | `release/v0.1.0` |
| **Development** | `develop` | Default integration branch |

### Commit Messages

```
# ✅ Conventional Commits Format
<type>(<scope>): <description>

# Types
- feat:     New feature
- fix:      Bug fix
- docs:     Documentation changes
- style:    Formatting, missing semi-colons, etc.
- refactor: Code refactoring
- test:     Adding missing tests
- chore:    Routine maintenance

# Examples
feat(blueprints): add create blueprint endpoint
fix(crafting): correct quality calculation formula
docs(readme): update quick-start section
refactor(api): restructure route modules
test(blueprints): add create blueprint tests
chore(deps): update ruff config
```

### Pull Request Process

1. **Create branch** from `develop` (or `main` for hotfixes)
2. **Implement feature** with commits following conventions
3. **Add/tests** where applicable
4. **Update documentation** alongside code changes
5. **Push branch** to fork/remote
6. **Open PR** using the `.github/PULL_REQUEST_TEMPLATE.md`
7. **Address review feedback**
8. **Merge** after CI passes (lint + test)

### PR Checklist

- [ ] Code follows `ruff` + `black` + `isort` style
- [ ] TypeScript compiles (`npm run type-check`)
- [ ] All tests pass (`pytest -v` + `npm test`)
- [ ] README.md updated if user-facing changes
- [ ] API docs updated (`/docs` when server running)
- [ ] No breaking changes (or documented breaking changes)
- [ ] Dependabot alerts addressed (if applicable)

## 🧪 Testing Guidelines

### Backend (pytest)

```python
# tests/api/test_blueprints.py
def test_list_blueprints(client):
    """GET /api/blueprints/ returns empty list initially."""
    response = client.get("/api/blueprints/")
    assert response.status_code == 200
    assert len(response.json()) == 0

def test_create_blueprint(client, blueprint_factory):
    """POST /api/blueprints/ creates a new blueprint."""
    blueprint = blueprint_factory()
    response = client.post("/api/blueprints/", json=blueprint.model_dump())
    assert response.status_code == 201
    assert response.json()["bp_name"] == blueprint.bp_name

def test_get_blueprint(client, blueprint_factory):
    """GET /api/blueprints/{id} returns correct blueprint."""
    blueprint = blueprint_factory()
    client.post("/api/blueprints/", json=blueprint.model_dump())
    response = client.get("/api/blueprints/1")
    assert response.status_code == 200
    assert response.json()["bp_name"] == blueprint.bp_name
```

### Frontend (Vitest + React Testing Library)

```tsx
// web/src/components/__tests__/BlueprintList.test.tsx
import { render, screen } from "@testing-library/react"
import { BlueprintsList } from "../BlueprintList"

describe("BlueprintsList", () => {
  it("renders heading", () => {
    render(<BlueprintsList />)
    expect(screen.getByRole("heading", { level: 2 })).toBeInTheDocument()
  })

  it("shows placeholder when no data", () => {
    render(<BlueprintsList />)
    expect(screen.getByText("Blueprint management grid")).toBeInTheDocument()
  })
})
```

### Test Configuration

```bash
# Run all backend tests
pytest -v

# Run tests in specific directory
pytest tests/api/ -v

# Run all frontend tests
cd web && npm test

# Run tests with coverage
pytest --cov=.
```

## 📦 Versioning

| Version | Description |
|---------|-------------|
| **0.1.0** | Initial release — API + Web UI scaffold |
| **0.2.0** | Blueprint CRUD + quality calculation |
| **1.0.0** | Stable release — production-ready |
| **1.1.0** | PostgreSQL pluggability + auth |
| **2.0.0** | Major overhaul or API-breaking changes |

Versioning follows [Semantic Versioning](https://semver.org/) (MAJOR.MINOR.PATCH).

## 🏷️ Labels & Tags

| Git Tag | Description |
|---------|-------------|
| `v0.1.0` | Initial scaffold |
| `v0.1.1` | Bug fixes |
| `v0.2.0` | Feature complete |
| `main` | Development branch |
| `release/v0.1.0` | Release candidate |

## 🎯 Novice-Friendly Onboarding

### First-Time Contributor

1. **Read** `README.md` + `docs/getting-started/overview.md`
2. **Set up** following the OS-specific guide in `docs/ai-agents/platforms.md`
3. **Run** `ruff check . && black . && isort .` — fix any issues
4. **Run** `pytest -v` + `npm test` — verify all tests pass
5. **Pick a simple issue** — `docs/contributing/good-first-issue.md` (if exists)
6. **Create branch** `feature/your-feature-name`
7. **Implement** + **test** + **document**
8. **Open PR** using the template
9. **Address feedback** — iterate until CI passes
10. **Celebrate** — your first merge! 🎉

### Expert Contributor

1. **Review** architecture docs in `docs/architecture/`
2. **Discuss** design decisions in `docs/contributing/`
3. **Propose** RFCs for major changes
4. **Optimize** performance, scalability, maintainability
5. **Mentor** newer contributors
6. **Drive** the project vision forward

## 🆘 Getting Help

| Resource | When to Use |
|----------|-------------|
| **GitHub Issues** | Bug reports, feature requests, questions |
| **GitHub Discussions** | Design discussions, "how would I..." questions |
| **CODEOWNERS** | Specific reviewers for certain file areas |
| **CI/CD failures** | Check GitHub Actions logs first |
| **AI agents** | Use the `docs/ai-agents/` guides for agent-specific help |

---

**Questions?** Open a GitHub Discussion or check the `docs/` directory for more details.
