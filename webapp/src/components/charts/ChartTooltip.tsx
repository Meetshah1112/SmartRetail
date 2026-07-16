import type { TooltipProps } from 'recharts'

type Formatter = (value: number, name: string) => string

const wrapStyle: React.CSSProperties = {
  background: 'var(--surface)',
  border: '1px solid var(--border-strong)',
  borderRadius: 10,
  boxShadow: 'var(--shadow-2)',
  padding: '8px 12px',
  fontSize: 12,
}

export function makeTooltip(format: Formatter) {
  return function ChartTooltip({ active, payload, label }: TooltipProps<number, string>) {
    if (!active || !payload?.length) return null
    return (
      <div style={wrapStyle}>
        {label !== undefined && (
          <div style={{ fontWeight: 700, color: 'var(--ink)', marginBottom: 4 }}>{label}</div>
        )}
        {payload.map((entry) => (
          <div key={entry.dataKey as string} style={{ color: 'var(--ink-2)', display: 'flex', gap: 8, alignItems: 'center' }}>
            <span
              style={{
                width: 8,
                height: 8,
                borderRadius: 2,
                background: entry.color ?? 'var(--accent)',
                display: 'inline-block',
              }}
            />
            <span>{entry.name}</span>
            <strong style={{ marginLeft: 'auto', color: 'var(--ink)' }}>
              {format(Number(entry.value), String(entry.name))}
            </strong>
          </div>
        ))}
      </div>
    )
  }
}
