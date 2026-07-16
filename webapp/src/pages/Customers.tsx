import {
  CartesianGrid,
  Cell,
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
import { ChartCard } from '../components/ui/ChartCard'
import { IconUsers } from '../components/ui/Icons'
import { KpiCard } from '../components/ui/KpiCard'
import { data } from '../data/types'
import { int, money } from '../lib/format'
import { SEGMENT_COLORS } from '../lib/palette'
import './pages.css'

const { segments, topCustomers } = data

const RfmTooltip = makeTooltip((v, name) => (name === 'Total spend' ? money(v) : `${v} days`))

const SEGMENT_BLURBS: Record<string, string> = {
  Premium: 'Recent, frequent, high-spend. Protect with VIP treatment.',
  Regular: 'Steady repeat buyers. Grow with cross-sell.',
  Occasional: 'Infrequent, lower spend. Nurture with campaigns.',
  Inactive: 'Long lapsed. Win-back offers or accept churn.',
}

export function Customers() {
  const totalCustomers = segments.profile.reduce((sum, s) => sum + s.customers, 0)

  return (
    <div className="page grid" style={{ gap: 'var(--gap)' }}>
      <div className="grid kpi-row" style={{ gridTemplateColumns: 'repeat(4, minmax(0,1fr))' }}>
        {segments.profile.map((s) => (
          <KpiCard
            key={s.name}
            label={`${s.name} customers`}
            value={s.customers}
            format={(v) => int(v)}
            tint={SEGMENT_COLORS[s.name]}
            icon={<IconUsers />}
          />
        ))}
      </div>

      <div className="grid cols-2">
        <ChartCard
          title="RFM Segmentation (K-Means, k=4)"
          subtitle="Recency vs total spend — 250 sampled customers per segment"
        >
          <ResponsiveContainer width="100%" height={300}>
            <ScatterChart margin={{ top: 8, right: 10, bottom: 4, left: 0 }}>
              <CartesianGrid strokeDasharray="3 4" />
              <XAxis
                dataKey="recency_days"
                name="Recency"
                unit=" d"
                tickLine={false}
                axisLine={false}
                type="number"
              />
              <YAxis
                dataKey="monetary"
                name="Total spend"
                tickLine={false}
                axisLine={false}
                width={56}
                scale="log"
                domain={[20, 'auto']}
                allowDataOverflow
                type="number"
                tickFormatter={(v: number) => money(v, 0)}
              />
              <Tooltip content={<RfmTooltip />} cursor={{ strokeDasharray: '4 4' }} />
              <Scatter isAnimationActive={false} data={segments.scatter} fillOpacity={0.55}>
                {segments.scatter.map((point, i) => (
                  <Cell key={i} fill={SEGMENT_COLORS[point.segment] ?? '#98a0b8'} />
                ))}
              </Scatter>
            </ScatterChart>
          </ResponsiveContainer>
        </ChartCard>

        <div className="grid" style={{ gap: 'var(--gap)' }}>
          <ChartCard title="Revenue by Segment">
            <Donut
              data={segments.profile.map((s) => ({ name: s.name, value: s.revenue }))}
              colors={(name) => SEGMENT_COLORS[name] ?? '#98a0b8'}
              centerValue={int(totalCustomers)}
              centerLabel="customers"
              height={180}
            />
          </ChartCard>
          <ChartCard title="Customer Lifetime Value (avg per segment)">
            <HBars
              data={segments.profile.map((s) => ({ label: s.name, value: s.avgSpend }))}
              color={(i) => Object.values(SEGMENT_COLORS)[i]}
            />
          </ChartCard>
        </div>
      </div>

      <div className="grid cols-2">
        <ChartCard title="Segment Profiles" subtitle="Averages per segment from the RFM table">
          <div className="table-scroll">
          <table className="data-table">
            <thead>
              <tr>
                <th>Segment</th>
                <th className="num">Customers</th>
                <th className="num">Recency (d)</th>
                <th className="num">Orders</th>
                <th className="num">Avg spend</th>
                <th className="num">Revenue</th>
              </tr>
            </thead>
            <tbody>
              {segments.profile.map((s) => (
                <tr key={s.name}>
                  <td>
                    <span
                      className="badge"
                      style={{
                        background: `color-mix(in srgb, ${SEGMENT_COLORS[s.name]} 16%, transparent)`,
                        color: SEGMENT_COLORS[s.name],
                      }}
                    >
                      {s.name}
                    </span>
                  </td>
                  <td className="num">{int(s.customers)}</td>
                  <td className="num">{s.avgRecency.toFixed(0)}</td>
                  <td className="num">{s.avgOrders.toFixed(1)}</td>
                  <td className="num">{money(s.avgSpend)}</td>
                  <td className="num">{money(s.revenue)}</td>
                </tr>
              ))}
            </tbody>
          </table>
          </div>
          <div className="card-sub" style={{ marginTop: 10 }}>
            {segments.profile.map((s) => (
              <div key={s.name} style={{ padding: '2px 0' }}>
                <strong style={{ color: SEGMENT_COLORS[s.name] }}>{s.name}:</strong>{' '}
                {SEGMENT_BLURBS[s.name]}
              </div>
            ))}
          </div>
        </ChartCard>

        <ChartCard title="Top 10 Customers by Lifetime Value">
          <HBars
            data={topCustomers.map((c) => ({
              label: `#${c.customer_id} · ${c.segment ?? '—'}`,
              value: c.sales,
              hint: `${int(c.orders)} orders`,
            }))}
            color={(i) => (i === 0 ? 'var(--accent)' : 'var(--c-violet)')}
          />
        </ChartCard>
      </div>
    </div>
  )
}
