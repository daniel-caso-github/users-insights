import type { UserProfile, SummaryStats } from '../types/github'
import { useApp } from '../context/AppContext'

interface ProfileHeaderProps {
  profile: UserProfile
  summaryStats: SummaryStats | null
}

export function ProfileHeader({ profile, summaryStats }: ProfileHeaderProps) {
  const { t } = useApp()

  return (
    <div className="flex gap-8 items-start p-6 rounded-2xl bg-surface-container-low">
      {profile.avatar_url && (
        <a href={profile.html_url ?? '#'} target="_blank" rel="noreferrer" className="shrink-0">
          <img
            src={profile.avatar_url}
            alt={profile.name ?? 'avatar'}
            className="w-24 h-24 rounded-xl"
            style={{ boxShadow: '0 0 80px rgba(0,105,218,0.4)' }}
          />
        </a>
      )}

      <div className="flex-1 min-w-0">
        <h1
          className="text-3xl font-semibold text-on-surface mb-1"
          style={{ letterSpacing: '-0.02em' }}
        >
          {profile.name ?? 'Unknown'}
        </h1>
        {profile.bio && (
          <p className="text-on-surface-variant text-sm mb-3 line-clamp-2">{profile.bio}</p>
        )}

        <div className="flex flex-wrap gap-2 mb-4">
          {profile.location && (
            <span className="text-xs text-on-surface-variant px-3 py-1 rounded-full bg-surface-container-high">
              {profile.location}
            </span>
          )}
          {profile.company && (
            <span className="text-xs text-on-surface-variant px-3 py-1 rounded-full bg-surface-container-high">
              {profile.company}
            </span>
          )}
        </div>

        <div className="flex gap-4 flex-wrap">
          <Stat label={t.followers} value={profile.followers} />
          <Stat label={t.following} value={profile.following} />
          <Stat label={t.repos} value={profile.public_repos} />
          {summaryStats && (
            <>
              <Stat label={t.prsMerged} value={summaryStats.total_prs_merged} />
              <Stat label={t.mergeRate} value={`${summaryStats.merge_rate}%`} />
            </>
          )}
        </div>
      </div>
    </div>
  )
}

function Stat({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="flex flex-col items-center px-4 py-2 rounded-xl bg-surface-container-high min-w-[64px]">
      <span className="text-base font-semibold text-on-surface">{value}</span>
      <span className="text-xs text-on-surface-variant uppercase tracking-wide mt-0.5">{label}</span>
    </div>
  )
}
