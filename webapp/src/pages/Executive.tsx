import {
  CartesianGrid,
  ReferenceLine,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { makeTooltip } from '../components/charts/ChartTooltip'
import { Donut } from '../components/charts/Donut'
import { HBars } from '../components/charts/HBars'
import { TrendArea } from '../components/charts/TrendArea'
import { ChartCard } from '../components/ui/ChartCard'
import {
  IconBag,
  IconBulb,
  IconCoins,
  IconPercent,
  IconReceipt,
  IconUsers,
} from '../components/ui/Icons'
import { KpiCard } from '../components/ui/KpiCard'
import { data } from '../data/types'
import { int, money, pct } from '../lib/format'
import { SEGMENT_COLORS, SERIES } from '../lib/palette'
import './pages.css'

const { kpis, monthly, categories, products, countries, segments, inventory } = data

const ScatterTip = makeTooltip((v) => money(v))

function keyInsights() {
  const premium = segments.profile.find((s) => s.name === 'Premium')
  const totalRevenue = segments.profile.reduce((sum, s) => sum + s.revenue, 0)
  const topCategory = categories[0]
  const worstBand = [...data.discountBands].sort((a, b) => a.margin - b.margin)[0]
  const topCountry = countries[0]
  return [
    {
      color: 'var(--c-teal)',
      text: (
        <>
          Sales grew <strong>{pct(kpis.delta.sales)}</strong> vs the previous 12 months.
        </>
      ),
    },
    {
      color: 'var(--accent)',
      text: (
        <>
          <strong>Premium customers</strong> ({int(premium?.customers ?? 0)}) drive{' '}
          <strong>{pct((premium?.revenue ?? 0) / totalRevenue)}</strong> of identified revenue.
        </>
      ),
    },
    {
      color: 'var(--c-blue)',
      text: (
        <>
          <strong>{topCategory.name}</strong> is the top category at{' '}
          <strong>{money(topCategory.sales)}</strong> sales.
        </>
      ),
    },
    {
      color: 'var(--c-pink)',
      text: (
        <>
          Deep discounting destroys margin: the <strong>{worstBand.band}</strong> band runs at{' '}
          <strong>{pct(worstBand.margin)}</strong> — confirmed by a t-test (p ≈ 10⁻³¹).
        </>
      ),
    },
    {
      color: 'var(--c-orange)',
      text: (
        <>
          <strong>{topCountry.name}</strong> leads all markets with{' '}
          <strong>{money(topCountry.sales)}</strong>; {inventory.deadStock} products are dead
          stock.
        </>
      ),
    },
  ]
}

export function Executive() {
  const t = kpis.total
  const d = kpis.delta

  return (
    <div className="page">
      <div className="grid kpi-row">
        <KpiCard label="Total Sales" value={t.sales} format={(v) => money(v)} delta={d.sales} tint="var(--accent)" icon={<IconBag />} />
        <KpiCard label="Total Profit" value={t.profit} format={(v) => money(v)} delta={d.profit} tint="var(--c-green)" icon={<IconCoins />} />
        <KpiCard label="Total Orders" value={t.orders} format={(v) => int(v)} delta={d.orders} tint="var(--c-blue)" icon={<IconReceipt />} />
        <KpiCard label="Total Customers" value={t.customers} format={(v) => int(v)} delta={d.customers} tint="var(--c-orange)" icon={<IconUsers />} />
        <KpiCard label="Profit Margin" value={t.margin} format={(v) => pct(v)} delta={d.margin} tint="var(--c-teal)" icon={<IconPercent />} />
      </div>

      <div className="exec-grid mt">
        <ChartCard title="Sales Trend Over Time" subtitle="Monthly revenue, Dec 2009 – Nov 2011" className="span-2">
          <TrendArea data={monthly} xKey="month" yKey="sales" name="Sales" color="#6c4ee0" />
        </ChartCard>

        <ChartCard title="Sales by Category" subtitle="Derived from product descriptions">
          <Donut
            data={categories.slice(0, 5).map((c) => ({ name: c.name, value: c.sales }))}
            colors={SERIES}
            centerValue={money(t.sales)}
            centerLabel="total sales"
            height={210}
          />
        </ChartCard>

        <div className="rail">
          <ChartCard title="Key Insights" subtitle={kpis.deltaWindow}>
            <div className="insight-list">
              {keyInsights().map((item, i) => (
                <div className="insight" key={i}>
                  <span className="dot" style={{ background: item.color }}>
                    <IconBulb />
                  </span>
                  <span>{item.text}</span>
                </div>
              ))}
            </div>
          </ChartCard>

          <ChartCard title="Data Overview" subtitle="After cleaning pipeline">
            <div className="overview-row"><span>Total Records</span><b>{int(t.records)}</b></div>
            <div className="overview-row"><span>Total Products</span><b>{int(t.products)}</b></div>
            <div className="overview-row"><span>Total Categories</span><b>{categories.length}</b></div>
            <div className="overview-row"><span>Countries</span><b>{t.countries}</b></div>
            <div className="overview-row"><span>Avg Order Value</span><b>{money(t.aov)}</b></div>
            <div className="overview-row"><span>Returned Value</span><b>{money(t.returnedValue)}</b></div>
          </ChartCard>
        </div>

        <ChartCard title="Top 10 Products by Sales">
          <HBars
            data={products.top.map((p) => ({ label: p.name, value: p.sales }))}
            color="var(--accent)"
          />
        </ChartCard>

        <ChartCard title="Profit vs Sales" subtitle="One dot per product (sample)">
          <ResponsiveContainer width="100%" height={250}>
            <ScatterChart margin={{ top: 8, right: 10, bottom: 4, left: 0 }}>
              <CartesianGrid strokeDasharray="3 4" />
              <XAxis dataKey="sales" name="Sales" tickLine={false} axisLine={false} tickFormatter={(v: number) => money(v, 0)} type="number" />
              <YAxis dataKey="profit" name="Profit" tickLine={false} axisLine={false} width={52} tickFormatter={(v: number) => money(v, 0)} type="number" />
              <Tooltip content={<ScatterTip />} cursor={{ strokeDasharray: '4 4' }} />
              <ReferenceLine y={0} stroke="var(--down)" strokeDasharray="4 4" />
              <Scatter isAnimationActive={false} data={products.scatter} fill="#6c4ee0" fillOpacity={0.55} />
            </ScatterChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Sales by Segment" subtitle="K-Means customer segments">
          <Donut
            data={segments.profile.map((s) => ({ name: s.name, value: s.revenue }))}
            colors={(name) => SEGMENT_COLORS[name] ?? '#98a0b8'}
            centerValue={int(segments.profile.reduce((sum, s) => sum + s.customers, 0))}
            centerLabel="customers"
            height={210}
          />
        </ChartCard>

        <ChartCard title="Monthly Profit Trend" className="span-2">
          <TrendArea data={monthly} xKey="month" yKey="profit" name="Profit" color="#17b8a0" height={200} />
        </ChartCard>

        <ChartCard title="Sales by Country (Top 8)" subtitle="United Kingdom dominates — see Sales page for ex-UK view">
          <HBars
            data={countries.slice(0, 8).map((c) => ({ label: c.name, value: c.sales }))}
            color={(i) => SERIES[(i + 1) % SERIES.length]}
          />
        </ChartCard>
      </div>
    </div>
  )
}
