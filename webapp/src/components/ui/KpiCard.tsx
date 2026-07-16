import type { ReactNode } from 'react'
import { useCountUp } from '../../hooks/useCountUp'
import { signedPct } from '../../lib/format'
import './kpi.css'

interface KpiCardProps {
  label: string
  value: number
  format: (v: number) => string
  delta?: number
  deltaSuffix?: string
  tint: string
  icon: ReactNode
}

export function KpiCard({ label, value, format, delta, deltaSuffix, tint, icon }: KpiCardProps) {
  const animated = useCountUp(value)
  const isUp = (delta ?? 0) >= 0

  return (
    <div className="card kpi" style={{ '--kpi-tint': tint } as React.CSSProperties}>
      <div className="icon-chip">{icon}</div>
      <div>
        <div className="kpi-label">{label}</div>
        <div className="kpi-value">{format(animated)}</div>
        {delta !== undefined && (
          <span className={`kpi-delta ${isUp ? 'up' : 'down'}`}>
            {isUp ? '▲' : '▼'} {signedPct(delta)}
            {deltaSuffix && <span className="vs">{deltaSuffix}</span>}
          </span>
        )}
      </div>
    </div>
  )
}
