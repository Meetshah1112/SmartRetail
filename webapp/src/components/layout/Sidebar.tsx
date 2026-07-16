import { NavLink } from 'react-router-dom'
import { data } from '../../data/types'
import {
  IconBox,
  IconCart,
  IconChart,
  IconCoins,
  IconHome,
  IconInfo,
  IconTrend,
  IconUsers,
  IconWarehouse,
} from '../ui/Icons'
import './sidebar.css'

const NAV = [
  { to: '/', label: 'Executive Dashboard', icon: <IconHome /> },
  { to: '/sales', label: 'Sales Dashboard', icon: <IconChart /> },
  { to: '/customers', label: 'Customer Dashboard', icon: <IconUsers /> },
  { to: '/products', label: 'Product Dashboard', icon: <IconBox /> },
  { to: '/profit', label: 'Profit Dashboard', icon: <IconCoins /> },
  { to: '/inventory', label: 'Inventory Dashboard', icon: <IconWarehouse /> },
  { to: '/forecast', label: 'Forecast Dashboard', icon: <IconTrend /> },
  { to: '/about', label: 'About Project', icon: <IconInfo /> },
]

export function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="side-brand">
        <div className="logo">
          <IconCart />
        </div>
        <div>
          <div className="name">
            Retail<em>IQ</em>
          </div>
          <div className="tag">Retail Analytics &amp; Business Intelligence</div>
        </div>
      </div>

      <nav className="side-nav" aria-label="Dashboard pages">
        {NAV.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === '/'}
            className={({ isActive }) => `side-link${isActive ? ' active' : ''}`}
          >
            {item.icon}
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div className="side-footer">
        <div className="headline">RetailIQ Analytics</div>
        <div>Smart Insights, Better Decisions.</div>
        <div className="refresh">
          Data window: {data.meta.window}
          <br />
          Built: {data.meta.generated}
        </div>
      </div>
    </aside>
  )
}
