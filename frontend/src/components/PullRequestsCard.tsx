import type { RepoPRs } from '../types/github'
import { useApp } from '../context/AppContext'

interface PullRequestsCardProps {
  repos: RepoPRs[]
}

export function PullRequestsCard({ repos }: PullRequestsCardProps) {
  const { t } = useApp()

  if (!repos.length) return null

  return (
    <div className="p-5 rounded-2xl bg-surface-container">
      <h2 className="text-sm font-semibold text-on-surface-variant uppercase tracking-wider mb-4">
        {t.reposWithMostPRs}
      </h2>
      <div className="flex flex-col gap-2">
        {repos.map((item) => {
          const repoName = item.repository.includes('/')
            ? item.repository.split('/').slice(-1)[0]
            : item.repository
          return (
            <div
              key={item.repository}
              className="flex items-center justify-between py-2 border-b border-outline-variant last:border-0"
            >
              <span className="text-sm text-on-surface truncate max-w-[70%]" title={item.repository}>
                {repoName}
              </span>
              <span className="text-xs font-semibold px-3 py-1 rounded-full bg-primary-container text-on-primary-container shrink-0">
                {item.count} PRs
              </span>
            </div>
          )
        })}
      </div>
    </div>
  )
}
