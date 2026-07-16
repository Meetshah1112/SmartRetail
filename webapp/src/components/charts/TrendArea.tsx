import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { money } from '../../lib/format'
import { makeTooltip } from './ChartTooltip'

interface TrendAreaProps {
  data: object[]
  xKey: string
  yKey: string
  name: string
  color: string
  height?: number
  tickEvery?: number
}

const CurrencyTooltip = makeTooltip((v) => money(v))

export function TrendArea({ data, xKey, yKey, name, color, height = 230, tickEvery = 2 }: TrendAreaProps) {
  const gradientId = `grad-${yKey}-${color.replace('#', '')}`
  return (
    <ResponsiveContainer width="100%" height={height}>
      <AreaChart data={data} margin={{ top: 8, right: 8, bottom: 0, left: 0 }}>
        <defs>
          <linearGradient id={gradientId} x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={color} stopOpacity={0.35} />
            <stop offset="100%" stopColor={color} stopOpacity={0.02} />
          </linearGradient>
        </defs>
        <CartesianGrid vertical={false} strokeDasharray="3 4" />
        <XAxis dataKey={xKey} tickLine={false} axisLine={false} interval={tickEvery} />
        <YAxis
          tickLine={false}
          axisLine={false}
          width={52}
          tickFormatter={(v: number) => money(v, 1)}
        />
        <Tooltip content={<CurrencyTooltip />} cursor={{ stroke: color, strokeOpacity: 0.25 }} />
        <Area isAnimationActive={false}
          type="monotone"
          dataKey={yKey}
          name={name}
          stroke={color}
          strokeWidth={2.4}
          fill={`url(#${gradientId})`}
          dot={false}
          activeDot={{ r: 4 }}
        />
      </AreaChart>
    </ResponsiveContainer>
  )
}
