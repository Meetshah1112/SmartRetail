import {
  CartesianGrid,
  ComposedChart,
  Line,
  ReferenceArea,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { makeTooltip } from '../components/charts/ChartTooltip'
import { ChartCard } from '../components/ui/ChartCard'
import { data } from '../data/types'
import { money, pct } from '../lib/format'
import './pages.css'

const { forecast, models } = data
const CurrencyTooltip = makeTooltip((v) => money(v))

/* Split the fitted series so the forecast tail renders in its own color. */
const series = forecast.map((point) => ({
  ...point,
  fittedActual: point.kind === 'actual' ? point.fitted : null,
  fittedFuture: point.kind === 'forecast' ? point.fitted : null,
}))
const firstForecastMonth = forecast.find((p) => p.kind === 'forecast')?.month

export function Forecast() {
  return (
    <div className="page grid" style={{ gap: 'var(--gap)' }}>
      <div className="metric-tiles">
        <div className="card metric-tile">
          <div className="big">{pct(models.forecast.mape)}</div>
          <div className="small">MAPE on 3-month holdout</div>
        </div>
        <div className="card metric-tile">
          <div className="big">{money(models.forecast.mae)}</div>
          <div className="small">Mean absolute error</div>
        </div>
        <div className="card metric-tile">
          <div className="big">{models.forecast.r2Train.toFixed(3)}</div>
          <div className="small">R² (train)</div>
        </div>
        <div className="card metric-tile">
          <div className="big">3 mo</div>
          <div className="small">Forecast horizon</div>
        </div>
      </div>

      <ChartCard
        title="Sales Forecast — Linear Regression"
        subtitle={`${models.forecast.algorithm}. Shaded region = forecast horizon (Dec 2011 – Feb 2012).`}
      >
        <ResponsiveContainer width="100%" height={360}>
          <ComposedChart data={series} margin={{ top: 10, right: 12, bottom: 0, left: 0 }}>
            <CartesianGrid vertical={false} strokeDasharray="3 4" />
            <XAxis dataKey="month" tickLine={false} axisLine={false} interval={1} />
            <YAxis tickLine={false} axisLine={false} width={56} tickFormatter={(v: number) => money(v, 1)} />
            <Tooltip content={<CurrencyTooltip />} />
            {firstForecastMonth && (
              <ReferenceArea
                x1={firstForecastMonth}
                fill="var(--accent)"
                fillOpacity={0.06}
                strokeOpacity={0}
              />
            )}
            <Line isAnimationActive={false} type="monotone" dataKey="sales" name="Actual sales" stroke="#6c4ee0" strokeWidth={2.6} dot={{ r: 2.5 }} connectNulls={false} />
            <Line isAnimationActive={false} type="monotone" dataKey="fittedActual" name="Model fit" stroke="#2e9bf0" strokeWidth={1.6} strokeDasharray="6 4" dot={false} />
            <Line isAnimationActive={false} type="monotone" dataKey="fittedFuture" name="Forecast" stroke="#f0862e" strokeWidth={2.6} strokeDasharray="7 4" dot={{ r: 3.5 }} />
          </ComposedChart>
        </ResponsiveContainer>
      </ChartCard>

      <div className="grid cols-2">
        <ChartCard title="How the model works">
          <div style={{ fontSize: 12.5, color: 'var(--ink-2)', lineHeight: 1.7 }}>
            <p style={{ marginTop: 0 }}>
              Monthly sales are modelled as <strong>linear trend + month-of-year seasonality</strong>{' '}
              (11 seasonal dummy variables). The model is trained on 24 complete months and
              validated on the last 3 held-out months before refitting on everything.
            </p>
            <p>
              The dominant pattern is the <strong>Sep–Nov gift-season surge</strong> — both years
              peak in November at ~2× the spring baseline. The forecast expects the usual
              post-Christmas cooldown through Feb 2012.
            </p>
            <p style={{ marginBottom: 0 }}>
              Holdout accuracy of <strong>{pct(models.forecast.mape)} MAPE</strong> means predictions
              were off by about {pct(models.forecast.mape)} on average — strong for a linear model
              on retail data.
            </p>
          </div>
        </ChartCard>

        <ChartCard title="Forecast values">
          <div className="table-scroll">
          <table className="data-table">
            <thead>
              <tr><th>Month</th><th>Type</th><th className="num">Sales / Prediction</th></tr>
            </thead>
            <tbody>
              {forecast.slice(-6).map((p) => (
                <tr key={p.month}>
                  <td>{p.month}</td>
                  <td>
                    <span
                      className="badge"
                      style={{
                        background: p.kind === 'forecast' ? 'color-mix(in srgb, var(--c-orange) 16%, transparent)' : 'color-mix(in srgb, var(--accent) 12%, transparent)',
                        color: p.kind === 'forecast' ? 'var(--c-orange)' : 'var(--accent)',
                      }}
                    >
                      {p.kind}
                    </span>
                  </td>
                  <td className="num">{money(p.kind === 'forecast' ? p.fitted : (p.sales ?? 0))}</td>
                </tr>
              ))}
            </tbody>
          </table>
          </div>
        </ChartCard>
      </div>
    </div>
  )
}
