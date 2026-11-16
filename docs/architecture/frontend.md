# Frontend Architecture — React + Vite + Tailwind

Overview of the React frontend architecture, designed for maintainability, scalability, and consistency with the FastAPI backend.

## 🏗️ High-Level Design

```
sc-oam-app Frontend
┌─────────────────────────────────────────┐
│            React + Vite + Tailwind       │
│  (web/src/ + web/package.json)           │
├─────────────────────────────────────────┤
│              API Client                   │
│  (web/src/lib/api.ts)                   │
├─────────────────────────────────────────┤
│              Component Library            │
│  (web/src/components/)                  │
├─────────────────────────────────────────┤
│              Page Components            │
│  (web/src/pages/)                       │
├─────────────────────────────────────────┤
│              Shared Utilities           │
│  (web/src/hooks/, web/src/types/)       │
└─────────────────────────────────────────┘
```

## ⚛️ React Component Architecture

### Component Hierarchy

```
App.tsx
├── Navigation (top bar)
├── Route-Based Pages
│   ├── BlueprintsPage
│   ├── CraftingPage
│   ├── WarehousePage
│   └── HangarPage
│   └── Dashboard
├── Common UI Elements
│   ├── Spinner (loading state)
│   ├── ErrorBoundary (error handling)
│   ├── ConfirmDialog (modals)
│   └── Table (data table base component)
└── Page-Specific Components
    ├── BlueprintList (grid/table)
    ├── BlueprintForm (create/edit)
    ├── QualityCalculator (crafting form)
    ├── InventoryTable (warehouse items)
    └── FleetTable (hangar ships)
```

### Component Standards

#### File Naming

| Component | File | Export |
|-----------|------|--------|
| **BlueprintList** | `BlueprintList.tsx` | `export const BlueprintsList = ...` |
| **QualityCalculator** | `QualityCalculator.tsx` | `export const CraftingCalculator = ...` |
| **FleetTable** | `FleetTable.tsx` | `export const FleetTable = ...` |
| **InventoryTable** | `InventoryTable.tsx` | `export const InventoryTable = ...` |

#### Component Template

```tsx
import React, { useState } from "react"
import { Spinner } from "../Common/Spinner"
import { ErrorBoundary } from "../Common/ErrorBoundary"

interface Props {
  data: ItemType[]
  onEdit: (id: number) => void
  onDelete: (id: number) => void
}

export const BlueprintList: React.FC<Props> = ({
  data,
  onEdit,
  onDelete,
}) => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleDelete = async (id: number) => {
    try {
      setLoading(true)
      const response = await fetch(`/api/blueprints/${id}`, {
        method: "DELETE",
      })
      if (!response.ok) throw new Error("Delete failed")
      onDelete(id)
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <Spinner />

  return (
    <div className="p-6 bg-card border border-border">
      <h2 className="text-xl font-medium mb-3">Blueprints</h2>

      {/* Error display */}
      {error && <p className="text-destructive mb-2">{error}</p>}

      {/* Data table or placeholder */}
      {data.length > 0 ? (
        {/* Table rendered here */}
      ) : (
        <p className="text-muted-foreground">
          No blueprints found. Add one using the navigation.
        </p>
      )}
    </div>
  )
}
```

## 🔗 API Client

### `web/src/lib/api.ts`

```typescript
// API client with base URL from environment
import axios from "axios"

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api"

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
    // Authorization header added interceptively if token exists
  },
)

// Request interceptor — add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token")
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor — handle common errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired — clear localStorage
      localStorage.removeItem("access_token")
      // Could redirect to login
    }
    return Promise.reject(error)
  }
)

export interface Response<T> {
  data: T
  success: boolean
  message: string
}

export const get = <T>(url: string) => api.get<Response<T>>(url).then((r) => r.data.data)
export const post = <T, U>(url: string, body: U) =>
  api.post<Response<T>>(url, body).then((r) => r.data.data)
export const put = <T, U>(url: string, body: U) =>
  api.put<Response<T>>(url, body).then((r) => r.data.data)
export const del = <T>(url: string) => api.delete<Response<T>>(url).then((r) => r.data.data)
```

### Usage Example

```tsx
import { useEffect, useState } from "react"
import { BlueprintsList } from "../components/BlueprintList"
import { api } from "../lib/api"

export const BlueprintsPage = () => {
  const [blueprints, setBlueprints] = useState<Blueprint[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchBlueprints() {
      try {
        const data = await api.get<Blueprint[]>("blueprints/")
        setBlueprints(data)
      } catch (err) {
        console.error("Failed to fetch blueprints:", err)
      } finally {
        setLoading(false)
      }
    }
    fetchBlueprints()
  }, [])

  if (loading) return <Spinner />

  return <BlueprintsList data={blueprints} onEdit={...} onDelete={...} />
}
```

## 🧭 Routing

### `web/src/App.tsx`

```tsx
import { BrowserRouter, Routes, Route } from "react-router-dom"
import { BlueprintsPage } from "./pages/BlueprintsPage"
import { CraftingPage } from "./pages/CraftingPage"
import { WarehousePage } from "./pages/WarehousePage"
import { HangarPage } from "./pages/HangarPage"
import { DashboardPage } from "./pages/DashboardPage"

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-background text-foreground">
        <nav className="p-4 border-b border-border">
          <h1 className="text-2xl font-bold">sc-oam-app</h1>
          <div className="flex gap-6">
            <a href="/blueprints">Blueprints</a>
            <a href="/crafting">Crafting</a>
            <a href="/warehouse">Warehouse</a>
            <a href="/hangar">Hangar</a>
          </div>
        </nav>

        <main className="p-6">
          <hr className="my-6" />
          <Routes>
            <Route path="/blueprints" element={<BlueprintsPage />} />
            <Route path="/crafting" element={<CraftingPage />} />
            <Route path="/warehouse" element={<WarehousePage />} />
            <Route path="/hangar" element={<HangarPage />} />
            <Route path="/" element={<DashboardPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}
```

### Route Definitions

| Path | Component | Description |
|------|-----------|-------------|
| `/` | `DashboardPage` | Welcome/dashboard overview |
| `/blueprints` | `BlueprintsPage` | Blueprint management grid |
| `/crafting` | `CraftingPage` | Quality calculator + resource selector |
| `/warehouse` | `WarehousePage` | Inventory management table |
| `/hangar` | `HangarPage` | Fleet vessel list + management |

## 🧩 Shared Hooks

### `web/src/hooks/useFetch.ts`

```typescript
import { useEffect, useState } from "react"
import { api } from "../lib/api"

interface UseFetchResult<T> {
  data: T | null
  loading: boolean
  error: string | null
}

export const useFetch = <T>(url: string): UseFetchResult<T> => {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchData() {
      try {
        const result = await api.get<T>(url)
        setData(result)
      } catch (err) {
        setError((err as Error).message)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [url])

  return { data, loading, error }
}
```

### Usage

```tsx
import { useFetch } from "../hooks/useFetch"

export const SomeComponent = () => {
  const { data, loading, error } = useFetch<SomeType>("blueprints/")

  if (loading) return <Spinner />
  if (error) return <p className="text-destructive">{error}</p>

  return <div>{/* render data */}</div>
}
```

## 📦 TypeScript Type Definitions

### `web/src/types/api.ts`

```typescript
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
  created_at: string
  updated_at: string
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

export interface CraftingResult {
  blueprint_id: number
  output_item: string
  base_quality: number
  final_quality: number
  tier: string
}
```

### Type Usage

```tsx
// Fetch with typed data
const { data: blueprints, loading, error } = useFetch<Blueprint[]>("blueprints/")

// Type-safe state
const [selectedBlueprint, setSelectedBlueprint] = useState<Blueprint | null>(null)

// Type-safe form
interface BlueprintFormValues {
  blueprint_id: string
  bp_name: string
  category: string
  quality_min: number
  quality_max: number
  ilg_label: string
}
```

## 🎨 Tailwind CSS Configuration

### `web/tailwind.config.js`

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["SF Mono", "Fira Mono", "monospace"],
      },
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [require("daisyui")],
}
```

### Color Palette (Semantic)

| CSS Variable | Usage |
|--------------|-------|
| `--border` | Table borders, input borders |
| `--input` | Form input backgrounds |
| `--ring` | Focus rings, active states |
| `--background` | Page backgrounds |
| `--foreground` | Primary text color |
| `--primary` | Primary actions, links |
| `--secondary` | Secondary actions, subtler text |
| `--primary-foreground` | Text on primary backgrounds |
| `--secondary-foreground` | Text on secondary backgrounds |

### Utility Classes Reference

| Pattern | Example |
|---------|---------|
| **Spacing** | `p-6` (padding), `m-4` (margin), `px-3` (horizontal padding) |
| **Colors** | `bg-background`, `text-foreground`, `bg-primary`, `text-primary-foreground` |
| **Typography** | `text-xl`, `font-medium`, `font-bold`, `text-muted-foreground` |
| **Border** | `border`, `border-border`, `border-2`, `border-destructive` |
| **Radius** | `rounded`, `rounded-lg`, `rounded-sm` |
| **Flex** | `flex`, `flex-col`, `flex-row`, `items-center`, `justify-between` |
| **Shadow** | `shadow-sm`, `shadow`, `shadow-lg` |
| **Hover** | `hover:bg-primary`, `hover:text-primary-foreground` |
| **Active** | `active:scale-95`, `active:bg-gray-200` |

## 📱 Responsive Design

### Breakpoints (Tailwind Default)

| Breakpoint | Class Prefix | Width |
|------------|--------------|-------|
| **Sm** | `sm:` | 640px |
| **Md** | `md:` | 768px |
| **Lg** | `lg:` | 1024px |
| **Xl** | `xl:` | 1280px |
| **2xl** | `2xl:` | 1536px |

### Example Responsive Grid

```html
<div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
  <!-- 1 column < 640px -->
  <!-- 2 columns ≥ 640px -->
  <!-- 3 columns ≥ 1024px -->
</div>
```

### Responsive Text

```html
<h1 className="text-3xl md:text-4xl lg:text-5xl font-bold">
  sc-oam-app
</h1>
```

## ♿ Accessibility (a11y)

### Keyboard Navigation

```html
<!-- Focusable elements -->
<button className="focus:outline-none focus:ring-2 focus:ring-primary">
  Action
</button>

<!-- Landmarks -->
<nav aria-label="Main navigation">
  <ul className="flex">
    <li><a href="#blueprints">Blueprints</a></li>
    <li><a href="#crafting">Crafting</a></li>
  </ul>
</nav>

<!-- Color contrast -->
<p className="text-foreground bg-background p-2">
  Ensure contrast ratio ≥ 4.5:1
</p>
```

### ARIA Labels

```html
<!-- When using custom components -->
<button aria-label="Close modal">✕</button>

<!-- Tables -->
<table>
  <thead>
    <tr>
      <th scope="col">Name</th>
      <th scope="col">Category</th>
    </tr>
  </thead>
  <tbody>
    ...
  </tbody>
</table>
```

## 🧪 Frontend Testing

### Vitest + React Testing Library Setup

```bash
# Already in devDependencies
npm test          # Runs vitest
```

### Sample Component Test

```tsx
// web/src/components/__tests__/BlueprintList.test.tsx
import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { BlueprintsList } from "../BlueprintList"

describe("BlueprintsList", () => {
  it("renders heading and placeholder", () => {
    render(<BlueprintsList />)

    expect(screen.getByRole("heading", { level: 2 })).toBeInTheDocument()
    expect(screen.getByText("No blueprints found")).toBeInTheDocument()
  })

  it("fetches and displays blueprints", async () => {
    // Mock the API
    jest.spyOn(api, "get").mockResolvedValueOnce({
      data: {
        data: [
          {
            id: 1,
            blueprint_id: "bp_001",
            bp_name: "Test Missile",
            category: "weapons",
            subcategory: "missiles",
            craft_type: "missile",
            output_item_name: "missile",
            quality_min: 500,
            quality_max: 800,
            craft_time_seconds: 30,
            ilg_label: "Weapons/Missiles",
            owner_handle: "",
            acquired_date: "",
            is_learned: false,
            notes: "",
            created_at: "",
            updated_at: "",
          },
        ],
        success: true,
        message: "",
      },
    } as any)

    render(<BlueprintsList />)

    expect(screen.getByRole("heading", { level: 2 })).toBeInTheDocument()
    expect(screen.getByText("Test Missile")).toBeInTheDocument()
  })

  it("shows error when API fails", async () => {
    jest.spyOn(api, "get").mockRejectedValueOnce(new Error("Network error"))

    render(<BlueprintsList />)

    expect(screen.getByText("Network error")).toBeInTheDocument()
  })
})
```

### Test Configuration (`vitest.config.ts`)

```typescript
import { defineConfig } from "vitest/config"
import react from "@vitejs/plugin-react"

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: "./vitest.setup.ts",
    coverage: {
      enabled: true,
      provider: "v8",
      reporter: ["text", "json", "html"],
    },
  },
})
```

### Vitest Setup (`vitest.setup.ts`)

```typescript
// Common test utilities, mocks, etc.
import "@testing-library/jest-dom"
```

## 📊 Build & Optimization

### Vite Build Configuration

```js
// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    port: 3000,
    open: true,
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    minify: 'esbuild',
    rollupOptions: {
      output: {
        // Manual chunk splitting for better caching
        manualChunks: {
          vendor: ['react', 'react-dom'],
          axios: ['axios'],
        },
      },
    },
  },
})
```

### Build Commands

```bash
# Development (with hot reload)
npm run dev

# Production build
npm run build

# Preview production build locally
npm run preview
```

### Bundle Analysis (Optional)

```bash
# Analyze bundle size
npm run build && npx vite-bundle-analyzer dist/
```

## 🌍 Internationalization (i18n - Planned)

### Structure (Future)

```
src/
├── locales/
│   ├── en.json
│   ├── de.json
│   └── ...
├── useTranslation.ts  # react-i18next hook
└── i18nProvider.tsx   # React Context provider
```

### Language Files Example

```json
// locales/en.json
{
  "appName": "sc-oam-app",
  "blueprints": "Blueprints",
  "crafting": "Crafting",
  "warehouse": "Warehouse",
  "hangar": "Hangar",
  "save": "Save",
  "cancel": "Cancel",
  "delete": "Delete",
  "confirm": "Confirm",
  "error": "Error",
  "success": "Success"
}
```

## 📈 Performance Considerations

| Area | Optimization |
|------|-------------|
| **Initial Load** | Code splitting with dynamic `import()` |
| **API Caching** | Use `stale-while-revalidate` with SWR or TanStack Query |
| **Image Optimization** | Use WebP format, `loading="lazy"` on `<img>` |
| **Font Loading` | `font-display: swap` in CSS, preconnect for Google Fonts |
| **Bundle Size** | Monitor with `npm run build` + `gzip-size` |
| **Lazy Loading** | Routes via `Lazy` + `Suspense`, images, large tables |

## 🆘 Frontend Debugging

| Tool | Use Case |
|------|----------|
| **React DevTools** | Component tree, props, state inspection |
| **Vite Preview** | Test production build locally |
| **Browser DevTools** | Network tab for API calls, Performance tab |
| **React Query DevTools** (if using) | Query state, cache, refetch patterns |
| **ESLint** | Catch code errors, style violations |
| **Tailwind JIT** | See which classes are being used/purge |

## 🤝 Human + AI Collaboration Guidelines

### For Human Reviewers

1. **Check** component structure matches conventions in `docs/architecture/`
2. **Verify** TypeScript types are correct and consistent
3. **Ensure** Tailwind classes use semantic naming (not inline styles)
4. **Confirm** API client calls match `docs/api-reference/`
5. **Run** `npm run type-check` + `npm test` before PR

### For AI Agents

1. **Reference** `docs/architecture/frontend.md` for component patterns
2. **Use** `api.ts` client for all API calls (don't fetch directly)
3. **Follow** TypeScript type definitions in `src/types/`
4. **Maintain** Tailwind configuration per `tailwind.config.js`
5. **Update** `vitest.setup.ts` if adding new test utilities

---

## 📁 Summary — Frontend File Map

```
web/
├── package.json          # Dependencies + scripts
├── vite.config.js        # Vite + React + Tailwind config
├── tailwind.config.js    # Tailwind theme + content paths
├── postcss.config.js     # PostCSS + autoprefixer
├── tsconfig.json         # TypeScript strict config
├── index.html            # HTML entry point
├── src/
│   ├── main.tsx          # ReactDOM createRoot
│   ├── App.tsx           # Navigation + Routes
│   ├── index.css         # @tailwind directives
│   ├── types/            # TypeScript interfaces
│   │   └── api.ts        # API response types
│   ├── components/       # Reusable UI components
│   │   ├── BlueprintList.tsx
│   │   ├── QualityCalculator.tsx
│   │   ├── FleetTable.tsx
│   │   ├── InventoryTable.tsx
│   │   ├── Dashboard.tsx
│   │   └── Common/       # Spinner, ErrorBoundary, etc.
│   ├── hooks/            # Custom React hooks (useFetch, etc.)
│   ├── lib/              # API client (api.ts)
│   ├── pages/            # Page-level components
│   │   ├── BlueprintsPage.tsx
│   │   ├── CraftingPage.tsx
│   │   ├── WarehousePage.tsx
│   │   ├── HangarPage.tsx
│   │   └── DashboardPage.tsx
│   └── index.css         # Global styles (already at src/)
└── __tests__/            # Vitest test files
```
