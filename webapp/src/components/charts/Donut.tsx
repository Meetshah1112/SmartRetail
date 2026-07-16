import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from 'recharts'
import { money, pct } from '../../lib/format'
import { makeTooltip } from './ChartTooltip'

interface DonutProps {
  data: { name: string; value: number }[]
  colors: string[] | ((name: string) => string)
  height?: number
  centerLabel?: string
  centerValue?: string
  maxLegend?: number
}

const CurrencyTooltip = makeTooltip((v) => money(v))

export function Donut({ data, colors, height = 230, centerLabel, centerValue, maxLegend = 6 }: DonutProps) {
  const total = data.reduce((sum, d) => sum + d.value, 0)
  const colorOf = (name: string, i: number) =>
    typeof colors === 'function' ? colors(name) : colors[i % colors.length]

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
      <div style={{ position: 'relative', width: '55%', minWidth: 150 }}>
        <ResponsiveContainer width="100%" height={height}>
          <PieChart>
            <Tooltip content={<CurrencyTooltip />} />
            <Pie isAnimationActive={false}
              data={data}
              dataKey="value"
              nameKey="name"
              innerRadius="62%"
              outerRadius="88%"
              paddingAngle={2}
              strokeWidth={0}
            >
              {data.map((entry, i) => (
                <Cell key={entry.name} fill={colorOf(entry.name, i)} />
              ))}
            </Pie>
          </PieChart>
        </ResponsiveContainer>
        {centerValue && (
          <div
            style={{
              position: 'absolute',
              inset: 0,
              display: 'grid',
              placeItems: 'center',
              pointerEvents: 'none',
            }}
          >
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: 17, fontWeight: 800 }}>{centerValue}</div>
              <div style={{ fontSize: 10, color: 'var(--ink-3)' }}>{centerLabel}</div>
            </div>
          </div>
        )}
      </div>
      <ul style={{ listStyle: 'none', margin: 0, padding: 0, flex: 1, fontSize: 11.5 }}>
        {data.slice(0, maxLegend).map((entry, i) => (
          <li
            key={entry.name}
            style={{ display: 'flex', alignItems: 'center', gap: 7, padding: '3.5px 0' }}
          >
            <span
              style={{
                width: 9,
                height: 9,
                borderRadius: 3,
                background: colorOf(entry.name, i),
                flex: 'none',
              }}
            />
            <span style={{ color: 'var(--ink-2)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
              {entry.name}
            </span>
            <span style={{ marginLeft: 'auto', fontWeight: 700, fontVariantNumeric: 'tabular-nums' }}>
              {pct(entry.value / total)}
            </span>
          </li>
        ))}
      </ul>
    </div>
  )
}
