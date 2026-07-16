import { data } from '../../data/types'
import { IconMoon, IconSun } from '../ui/Icons'
import './topbar.css'

interface TopbarProps {
  title: string
  subtitle: string
  theme: 'light' | 'dark'
  onToggleTheme: () => void
}

export function Topbar({ title, subtitle, theme, onToggleTheme }: TopbarProps) {
  return (
    <header className="topbar">
      <div className="title-block">
        <h1>{title}</h1>
        <div className="subtitle">{subtitle}</div>
      </div>
      <div className="controls">
        <div className="chip">
          <span className="label">Date range</span>
          {data.meta.window}
        </div>
        <div className="chip">
          <span className="label">Dataset</span>
          Online Retail II · {data.kpis.total.countries} countries
        </div>
        <button
          type="button"
          className="theme-btn"
          onClick={onToggleTheme}
          aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
        >
          {theme === 'light' ? <IconMoon /> : <IconSun />}
        </button>
      </div>
    </header>
  )
}
