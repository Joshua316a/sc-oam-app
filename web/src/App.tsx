import { BrowserRouter } from 'react-router-dom'
import { Dashboard } from './components/Dashboard'
import { BlueprintsList } from './components/blueprint-list'
import { CraftingCalculator } from './components/quality-calculator'
import { FleetTable } from './components/fleet-table'
import { InventoryTable } from './components/inventory-table'

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-background text-foreground">
        <nav className="p-4 border-b border-border">
          <h1 className="text-2xl font-bold">sc-oam-app</h1>
          <div className="flex gap-6">
            <a href="/blueprints" className="hover:text-primary">Blueprints</a>
            <a href="/crafting" className="hover:text-primary">Crafting</a>
            <a href="/warehouse" className="hover:text-primary">Warehouse</a>
            <a href="/hangar" className="hover:text-primary">Hangar</a>
          </div>
        </nav>

        <main className="p-6">
          <hr className="my-6" />
          {window.location.pathname === '/blueprints' && <BlueprintsList />}
          {window.location.pathname === '/crafting' && <CraftingCalculator />}
          {window.location.pathname === '/warehouse' && <InventoryTable />}
          {window.location.pathname === '/hangar' && <FleetTable />}
          <Dashboard />
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App
