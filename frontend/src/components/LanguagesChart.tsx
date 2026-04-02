import type { LanguageUsage } from '../types/github'
import { useApp } from '../context/AppContext'

const LANGUAGE_COLORS: Record<string, string> = {
  TypeScript: '#acc7ff',
  JavaScript: '#acc7ff',
  Python: '#acc7ff',
  Go: '#acc7ff',
  Rust: '#acc7ff',
  CSS: '#ffb3ad',
  SCSS: '#ffb3ad',
  HTML: '#ffb3ad',
  Vue: '#ffb3ad',
  Dockerfile: '#bfc7d3',
  Shell: '#bfc7d3',
  Makefile: '#bfc7d3',
}

function getColor(language: string): string {
  return LANGUAGE_COLORS[language] ?? '#acc7ff'
}

interface LanguagesChartProps {
  languages: LanguageUsage[]
}

export function LanguagesChart({ languages }: LanguagesChartProps) {
  const { t } = useApp()

  if (!languages.length) return null

  const max = Math.max(...languages.map((l) => l.count))

  return (
    <div className="p-5 rounded-2xl bg-surface-container">
      <h2 className="text-sm font-semibold text-on-surface-variant uppercase tracking-wider mb-4">
        {t.mostUsedLanguages}
      </h2>
      <div className="flex flex-col gap-3">
        {languages.map((item) => {
          const pct = Math.round((item.count / max) * 100)
          const color = getColor(item.language)
          return (
            <div key={item.language}>
              <div className="flex justify-between items-center mb-1">
                <span className="text-xs font-medium text-on-surface uppercase tracking-wide">
                  {item.language}
                </span>
                <span className="text-xs text-on-surface-variant">{item.count}</span>
              </div>
              <div className="h-2 rounded-full bg-surface-container-high overflow-hidden">
                <div
                  className="h-full rounded-full transition-all duration-500"
                  style={{ width: `${pct}%`, backgroundColor: color }}
                />
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
