import { money, truncate } from '../../lib/format'

interface HBarsProps {
  data: { label: string; value: number; hint?: string }[]
  color?: string | ((index: number) => string)
  format?: (v: number) => string
  maxLabel?: number
}

/** Lightweight horizontal bar list (CSS-based) — crisper than a chart lib for top-N lists. */
export function HBars({ data, color = 'var(--accent)', format = (v) => money(v, 1), maxLabel = 30 }: HBarsProps) {
  const max = Math.max(...data.map((d) => d.value), 1)
  const colorOf = (i: number) => (typeof color === 'function' ? color(i) : color)

  return (
    <div style={{ display: 'grid', gap: 7 }}>
      {data.map((row, i) => (
        <div key={row.label} title={row.hint ?? row.label}>
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              fontSize: 11.5,
              marginBottom: 2.5,
            }}
          >
            <span style={{ color: 'var(--ink-2)', fontWeight: 600 }}>{truncate(row.label, maxLabel)}</span>
            <span style={{ fontWeight: 700, fontVariantNumeric: 'tabular-nums' }}>{format(row.value)}</span>
          </div>
          <div
            style={{
              height: 7,
              borderRadius: 4,
              background: 'var(--surface-2)',
              overflow: 'hidden',
            }}
          >
            <div
              style={{
                width: `${(row.value / max) * 100}%`,
                height: '100%',
                borderRadius: 4,
                background: colorOf(i),
                transition: 'width 600ms cubic-bezier(0.22,1,0.36,1)',
              }}
            />
          </div>
        </div>
      ))}
    </div>
  )
}
