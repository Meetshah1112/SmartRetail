import { useEffect, useRef, useState } from 'react'

const DURATION_MS = 900

/**
 * Animates 0 → target once on mount.
 * Falls back to the final value immediately for reduced-motion users and
 * hidden/background tabs (where requestAnimationFrame is throttled), and a
 * timeout guarantees the exact target even if frames are dropped.
 */
export function useCountUp(target: number): number {
  const [value, setValue] = useState(0)
  const frame = useRef(0)

  useEffect(() => {
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    if (reducedMotion || document.visibilityState !== 'visible') {
      setValue(target)
      return
    }

    const start = performance.now()
    const tick = (now: number) => {
      const t = Math.min((now - start) / DURATION_MS, 1)
      const eased = 1 - Math.pow(1 - t, 3)
      setValue(t < 1 ? target * eased : target)
      if (t < 1) frame.current = requestAnimationFrame(tick)
    }
    frame.current = requestAnimationFrame(tick)
    const settle = setTimeout(() => setValue(target), DURATION_MS + 150)

    return () => {
      cancelAnimationFrame(frame.current)
      clearTimeout(settle)
    }
  }, [target])

  return value
}
