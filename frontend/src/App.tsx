import { useState } from 'react'
import { useUserInsights } from './hooks/useUserInsights'
import { SearchBar } from './components/SearchBar'
import { LoadingSpinner } from './components/LoadingSpinner'
import { ProfileHeader } from './components/ProfileHeader'
import { LanguagesChart } from './components/LanguagesChart'
import { PullRequestsCard } from './components/PullRequestsCard'
import { ContributionsChart } from './components/ContributionsChart'
import { HoursActivityChart } from './components/HoursActivityChart'
import { useApp } from './context/AppContext'

export default function App() {
  const [searchedUser, setSearchedUser] = useState<string | null>(null)
  const { data, loading, error } = useUserInsights(searchedUser)
  const { theme, toggleTheme, lang, setLang, t } = useApp()

  const hasResults = !!data && !loading

  return (
    <div className="min-h-svh bg-surface text-on-surface">
      {/* Header */}
      <header className="sticky top-0 z-10 backdrop-blur-md bg-surface/70 border-b border-outline-variant px-6 py-4 flex items-center gap-4">
        <span className="text-primary font-semibold tracking-tight mr-auto">GitHub Insights</span>
        <SearchBar key={searchedUser === null ? 'empty' : 'filled'} onSearch={setSearchedUser} loading={loading} />

        {/* Active user chip */}
        {searchedUser && (
          <div className="flex items-center gap-1 px-3 py-1 rounded-full bg-surface-container border border-outline-variant text-sm text-on-surface-variant max-w-[160px]">
            <span className="truncate">@{searchedUser}</span>
            <button
              onClick={() => setSearchedUser(null)}
              className="ml-1 text-on-surface-variant hover:text-on-surface transition-colors cursor-pointer flex-shrink-0"
              aria-label="Clear search"
            >
              ×
            </button>
          </div>
        )}

        {/* Language selector */}
        <div className="flex items-center gap-1">
          <button
            onClick={() => setLang('en')}
            className={`text-xs px-2 py-1 rounded font-medium transition-colors cursor-pointer ${
              lang === 'en'
                ? 'text-on-primary bg-primary'
                : 'text-on-surface-variant hover:text-on-surface'
            }`}
          >
            EN
          </button>
          <button
            onClick={() => setLang('es')}
            className={`text-xs px-2 py-1 rounded font-medium transition-colors cursor-pointer ${
              lang === 'es'
                ? 'text-on-primary bg-primary'
                : 'text-on-surface-variant hover:text-on-surface'
            }`}
          >
            ES
          </button>
        </div>

        {/* Theme toggle */}
        <button
          onClick={toggleTheme}
          className="p-2 rounded-full hover:bg-surface-container-high transition-colors cursor-pointer text-on-surface-variant hover:text-on-surface"
          aria-label="Toggle theme"
        >
          {theme === 'dark' ? (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <circle cx="12" cy="12" r="4" />
              <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41" />
            </svg>
          ) : (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
            </svg>
          )}
        </button>
      </header>

      {/* Hero (estado inicial sin búsqueda) */}
      {!searchedUser && (
        <div className="flex flex-col items-center justify-center gap-8 px-6 py-32 text-center">
          <h1
            className="text-5xl font-semibold text-on-surface max-w-lg"
            style={{ letterSpacing: '-0.03em' }}
          >
            {t.heroTitle}
          </h1>
          <p className="text-on-surface-variant max-w-sm text-base">{t.heroSubtitle}</p>
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div className="px-6 py-12">
          <LoadingSpinner />
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="mx-6 mt-8 p-4 rounded-xl bg-surface-container border border-outline-variant text-error text-sm">
          {error}
        </div>
      )}

      {/* Dashboard */}
      {hasResults && (
        <main className="px-6 py-8 max-w-5xl mx-auto flex flex-col gap-6">
          {data.user_profile && (
            <ProfileHeader profile={data.user_profile} summaryStats={data.summary_stats} />
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <LanguagesChart languages={data.most_used_languages} />
            <PullRequestsCard repos={data.repos_with_more_prs} />
            <ContributionsChart contributions={data.monthly_contributions} />
            <HoursActivityChart activity={data.hours_more_activity} />
          </div>
        </main>
      )}
    </div>
  )
}
