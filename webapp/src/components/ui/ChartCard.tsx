import type { CSSProperties, ReactNode } from 'react'

interface ChartCardProps {
  title: string
  subtitle?: string
  children: ReactNode
  style?: CSSProperties
  className?: string
}

export function ChartCard({ title, subtitle, children, style, className }: ChartCardProps) {
  return (
    <section className={`card ${className ?? ''}`} style={style}>
      <h2 className="card-title">
        <span className="bar" />
        {title}
      </h2>
      {subtitle && <div className="card-sub">{subtitle}</div>}
      {children}
    </section>
  )
}
