interface IconProps {
  size?: number
}

function svgProps(size: number) {
  return {
    width: size,
    height: size,
    viewBox: '0 0 24 24',
    fill: 'none',
    stroke: 'currentColor',
    strokeWidth: 2,
    strokeLinecap: 'round',
    strokeLinejoin: 'round',
  } as const
}

export const IconBag = ({ size = 18 }: IconProps) => (
  <svg {...svgProps(size)}>
    <path d="M6 7h12l1 13H5L6 7z" />
    <path d="M9 10V5a3 3 0 0 1 6 0v5" />
  </svg>
)

export const IconCoins = ({ size = 18 }: IconProps) => (
  <svg {...svgProps(size)}>
    <circle cx="12" cy="12" r="9" />
    <path d="M12 7v10M15.5 9.5c-.8-1-2.1-1.5-3.5-1.5-1.9 0-3.5 1-3.5 2.5S10 13 12 13s3.5.9 3.5 2.5-1.6 2.5-3.5 2.5c-1.4 0-2.7-.5-3.5-1.5" />
  </svg>
)

export const IconReceipt = ({ size = 18 }: IconProps) => (
  <svg {...svgProps(size)}>
    <path d="M5 3h14v18l-2.3-1.5L14.4 21l-2.4-1.5L9.6 21l-2.3-1.5L5 21V3z" />
    <path d="M9 8h6M9 12h6" />
  </svg>
)

export const IconUsers = ({ size = 18 }: IconProps) => (
  <svg {...svgProps(size)}>
    <circle cx="9" cy="8" r="3.2" />
    <path d="M3.5 19c.6-3 2.9-4.6 5.5-4.6s4.9 1.6 5.5 4.6" />
    <circle cx="17" cy="9" r="2.4" />
    <path d="M15.8 14.6c2.3.2 4.1 1.6 4.7 4" />
  </svg>
)

export const IconPercent = ({ size = 18 }: IconProps) => (
  <svg {...svgProps(size)}>
    <path d="M19 5 5 19" />
    <circle cx="7.5" cy="7.5" r="2.5" />
    <circle cx="16.5" cy="16.5" r="2.5" />
  </svg>
)

export const IconHome = ({ size = 17 }: IconProps) => (
  <svg {...svgProps(size)}>
    <path d="M3 11 12 4l9 7" />
    <path d="M5 10v10h14V10" />
  </svg>
)

export const IconChart = ({ size = 17 }: IconProps) => (
  <svg {...svgProps(size)}>
    <path d="M4 20V10M10 20V4M16 20v-9M21 20H3" />
  </svg>
)

export const IconBox = ({ size = 17 }: IconProps) => (
  <svg {...svgProps(size)}>
    <path d="m12 3 8 4.5v9L12 21l-8-4.5v-9L12 3z" />
    <path d="m4 7.5 8 4.5 8-4.5M12 12v9" />
  </svg>
)

export const IconWarehouse = ({ size = 17 }: IconProps) => (
  <svg {...svgProps(size)}>
    <path d="M3 9.5 12 4l9 5.5V20h-4v-6H7v6H3V9.5z" />
    <path d="M7 20h10" />
  </svg>
)

export const IconTrend = ({ size = 17 }: IconProps) => (
  <svg {...svgProps(size)}>
    <path d="m3 16 5.5-5.5 3.5 3.5L20 6" />
    <path d="M15 6h5v5" />
  </svg>
)

export const IconInfo = ({ size = 17 }: IconProps) => (
  <svg {...svgProps(size)}>
    <circle cx="12" cy="12" r="9" />
    <path d="M12 11v5M12 8h.01" />
  </svg>
)

export const IconMoon = ({ size = 16 }: IconProps) => (
  <svg {...svgProps(size)}>
    <path d="M20 13.5A8 8 0 0 1 10.5 4 7 7 0 1 0 20 13.5z" />
  </svg>
)

export const IconSun = ({ size = 16 }: IconProps) => (
  <svg {...svgProps(size)}>
    <circle cx="12" cy="12" r="4" />
    <path d="M12 2v2m0 16v2M4.9 4.9l1.4 1.4m11.4 11.4 1.4 1.4M2 12h2m16 0h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" />
  </svg>
)

export const IconCart = ({ size = 22 }: IconProps) => (
  <svg {...svgProps(size)}>
    <circle cx="9" cy="20" r="1.6" />
    <circle cx="17" cy="20" r="1.6" />
    <path d="M3 4h2.2l2.2 11.5a1.5 1.5 0 0 0 1.5 1.2h7.9a1.5 1.5 0 0 0 1.5-1.2L20 8H6" />
  </svg>
)

export const IconBulb = ({ size = 16 }: IconProps) => (
  <svg {...svgProps(size)}>
    <path d="M9 18h6M10 21h4" />
    <path d="M12 3a6 6 0 0 0-3.5 10.9c.8.6 1.5 1.6 1.5 2.6V17h4v-.5c0-1 .7-2 1.5-2.6A6 6 0 0 0 12 3z" />
  </svg>
)
