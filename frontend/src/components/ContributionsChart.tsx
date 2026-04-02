import type { MonthlyContributionItem } from '../types/github'
import { useApp } from '../context/AppContext'

interface ContributionsChartProps {
  contributions: MonthlyContributionItem[]
}

export function ContributionsChart({ contributions }: ContributionsChartProps) {
  const { t } = useApp()

  if (!contributions.length) return null

  const maxCommits = Math.max(...contributions.map((c) => c.commits), 1)

  return (
    <div className="p-5 rounded-2xl bg-surface-container">
      <h2 className="text-sm font-semibold text-on-surface-variant uppercase tracking-wider mb-4">
        {t.monthlyContributions}
      </h2>
      <div className="overflow-x-auto">
        <table className="w-full text-xs">
          <thead>
            <tr className="text-on-surface-variant uppercase tracking-wide">
              <th className="text-left pb-2 font-medium">{t.month}</th>
              <th className="text-right pb-2 font-medium">{t.prs}</th>
              <th className="text-right pb-2 font-medium">{t.issues}</th>
              <th className="text-right pb-2 font-medium">{t.commits}</th>
              <th className="pb-2 w-24" />
            </tr>
          </thead>
          <tbody>
            {contributions.map((item) => {
              const pct = Math.round((item.commits / maxCommits) * 100)
              return (
                <tr key={item.month} className="border-t border-outline-variant">
                  <td className="py-2 text-on-surface">{item.month}</td>
                  <td className="py-2 text-right text-on-surface-variant">{item.pull_requests}</td>
                  <td className="py-2 text-right text-on-surface-variant">{item.issues}</td>
                  <td className="py-2 text-right text-on-surface">{item.commits}</td>
                  <td className="py-2 pl-3">
                    <div className="h-1.5 rounded-full bg-surface-container-high overflow-hidden">
                      <div
                        className="h-full rounded-full bg-primary"
                        style={{ width: `${pct}%` }}
                      />
                    </div>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}
