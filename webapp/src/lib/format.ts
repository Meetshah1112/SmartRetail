const GBP = '£'

export function money(value: number, digits = 2): string {
  const abs = Math.abs(value)
  if (abs >= 1e9) return `${GBP}${(value / 1e9).toFixed(digits)}B`
  if (abs >= 1e6) return `${GBP}${(value / 1e6).toFixed(digits)}M`
  if (abs >= 1e3) return `${GBP}${(value / 1e3).toFixed(digits > 1 ? 1 : 0)}K`
  return `${GBP}${value.toFixed(0)}`
}

export function moneyFull(value: number): string {
  return `${GBP}${value.toLocaleString('en-GB', { maximumFractionDigits: 0 })}`
}

export function int(value: number): string {
  return value.toLocaleString('en-GB', { maximumFractionDigits: 0 })
}

export function pct(value: number, digits = 1): string {
  return `${(value * 100).toFixed(digits)}%`
}

export function signedPct(value: number, digits = 1): string {
  const sign = value >= 0 ? '+' : ''
  return `${sign}${(value * 100).toFixed(digits)}%`
}

export function truncate(text: string, max = 28): string {
  return text.length > max ? `${text.slice(0, max - 1)}…` : text
}
