import type { HourlyActivityItem } from '../types/github'
import { useApp } from '../context/AppContext'

interface HoursActivityChartProps {
  activity: HourlyActivityItem[]
}

export function HoursActivityChart({ activity }: HoursActivityChartProps) {
  const { t } = useApp()

  if (!activity.length) return null

  const max = Math.max(...activity.map((a) => a.count), 1)

  return (
    <div className="p-5 rounded-2xl bg-surface-container">
      <h2 className="text-sm font-semibold text-on-surface-variant uppercase tracking-wider mb-4">
        {t.activityByTime}
      </h2>
      <div className="flex flex-col gap-4">
        {activity.map((item) => {
          const pct = Math.round((item.count / max) * 100)
          return (
            <div key={item.period}>
              <div className="flex justify-between items-center mb-1.5">
                <span className="text-sm font-medium text-on-surface capitalize">{item.period}</span>
                <span className="text-xs text-on-surface-variant">
                  {item.count} {t.events}
                </span>
              </div>
              <div className="h-3 rounded-full bg-surface-container-high overflow-hidden">
                <div
                  className="h-full rounded-full transition-all duration-500"
                  style={{
                    width: `${pct}%`,
                    background:
                      'linear-gradient(135deg, var(--color-primary), var(--color-primary-container))',
                  }}
                />
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
