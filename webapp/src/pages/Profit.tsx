import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { makeTooltip } from '../components/charts/ChartTooltip'
import { HBars } from '../components/charts/HBars'
import { TrendArea } from '../components/charts/TrendArea'
import { ChartCard } from '../components/ui/ChartCard'
import { IconCoins, IconPercent, IconReceipt, IconTrend } from '../components/ui/Icons'
import { KpiCard } from '../components/ui/KpiCard'
import { data } from '../data/types'
import { money, pct } from '../lib/format'
import './pages.css'

const { kpis, monthly, categories, discountBands, countries } = data
const MarginTooltip = makeTooltip((v, name) => (name === 'Margin' ? pct(v) : money(v)))

export function Profit() {
  const t = kpis.total

  return (
    <div className="page grid" style={{ gap: 'var(--gap)' }}>
      <div className="grid kpi-row" style={{ gridTemplateColumns: 'repeat(4, minmax(0,1fr))' }}>
        <KpiCard label="Estimated Profit" value={t.profit} format={(v) => money(v)} delta={kpis.delta.profit} tint="var(--c-green)" icon={<IconCoins />} />
        <KpiCard label="Profit Margin" value={t.margin} format={(v) => pct(v)} delta={kpis.delta.margin} tint="var(--c-teal)" icon={<IconPercent />} />
        <KpiCard label="Avg Profit / Order" value={t.profit / t.orders} format={(v) => money(v)} tint="var(--accent)" icon={<IconReceipt />} />
        <KpiCard label="Returned Value" value={t.returnedValue} format={(v) => money(v)} tint="var(--c-pink)" icon={<IconTrend />} />
      </div>

      <div className="grid cols-2">
        <ChartCard title="Monthly Profit Trend" subtitle="Estimated profit follows the seasonal sales curve">
          <TrendArea data={monthly} xKey="month" yKey="profit" name="Profit" color="#17b8a0" />
        </ChartCard>

        <ChartCard
          title="Profit Margin by Discount Band"
          subtitle="Margins collapse once discounts pass 30% — the t-test says this is no accident"
        >
          <ResponsiveContainer width="100%" height={230}>
            <BarChart data={discountBands} margin={{ top: 8, right: 8, bottom: 0, left: 0 }}>
              <CartesianGrid vertical={false} strokeDasharray="3 4" />
              <XAxis dataKey="band" tickLine={false} axisLine={false} />
              <YAxis tickLine={false} axisLine={false} width={48} tickFormatter={(v: number) => pct(v, 0)} />
              <Tooltip content={<MarginTooltip />} cursor={{ fill: 'var(--accent-soft)' }} />
              <ReferenceLine y={0} stroke="var(--ink-3)" />
              <Bar isAnimationActive={false} dataKey="margin" name="Margin" radius={[5, 5, 0, 0]}>
                {discountBands.map((band) => (
                  <Cell key={band.band} fill={band.margin >= 0 ? '#17b8a0' : '#e04e7a'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      <div className="grid cols-2">
        <ChartCard title="Profit by Category">
          <HBars
            data={[...categories]
              .sort((a, b) => b.profit - a.profit)
              .map((c) => ({ label: c.name, value: c.profit }))}
            color="var(--c-green)"
          />
        </ChartCard>
        <ChartCard title="Profit by Country (Top 8)" subtitle="Assuming uniform cost ratio across markets">
          <HBars
            data={countries.slice(0, 8).map((c) => ({ label: c.name, value: c.sales * t.margin }))}
            color="var(--c-teal)"
          />
        </ChartCard>
      </div>
    </div>
  )
}
