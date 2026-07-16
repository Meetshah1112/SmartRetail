import { HashRouter, Route, Routes, useLocation } from 'react-router-dom'
import { Sidebar } from './components/layout/Sidebar'
import { Topbar } from './components/layout/Topbar'
import { useTheme } from './hooks/useTheme'
import { About } from './pages/About'
import { Customers } from './pages/Customers'
import { Executive } from './pages/Executive'
import { Forecast } from './pages/Forecast'
import { Inventory } from './pages/Inventory'
import { Products } from './pages/Products'
import { Profit } from './pages/Profit'
import { Sales } from './pages/Sales'

const PAGE_META: Record<string, { title: string; subtitle: string }> = {
  '/': { title: 'Executive Dashboard', subtitle: 'Overview of Sales, Profit, Customers & Orders' },
  '/sales': { title: 'Sales Dashboard', subtitle: 'Trends, seasonality and market breakdown' },
  '/customers': { title: 'Customer Dashboard', subtitle: 'RFM segmentation, lifetime value and behaviour' },
  '/products': { title: 'Product Dashboard', subtitle: 'Category performance and best sellers' },
  '/profit': { title: 'Profit Dashboard', subtitle: 'Estimated margins and the cost of discounting' },
  '/inventory': { title: 'Inventory Dashboard', subtitle: 'Movement classes, restocking and dead stock' },
  '/forecast': { title: 'Forecast Dashboard', subtitle: 'Machine-learning sales prediction' },
  '/about': { title: 'About Project', subtitle: 'Dataset, pipeline, models and assumptions' },
}

function Shell() {
  const { theme, toggle } = useTheme()
  const { pathname } = useLocation()
  const meta = PAGE_META[pathname] ?? PAGE_META['/']

  return (
    <div className="app-shell">
      <Sidebar />
      <main className="app-main">
        <Topbar title={meta.title} subtitle={meta.subtitle} theme={theme} onToggleTheme={toggle} />
        <Routes>
          <Route path="/" element={<Executive />} />
          <Route path="/sales" element={<Sales />} />
          <Route path="/customers" element={<Customers />} />
          <Route path="/products" element={<Products />} />
          <Route path="/profit" element={<Profit />} />
          <Route path="/inventory" element={<Inventory />} />
          <Route path="/forecast" element={<Forecast />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </main>
    </div>
  )
}

export default function App() {
  return (
    <HashRouter>
      <Shell />
    </HashRouter>
  )
}
