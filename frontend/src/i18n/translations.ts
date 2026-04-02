export interface Translations {
  searchPlaceholder: string
  searchButton: string
  heroTitle: string
  heroSubtitle: string
  loading: string
  followers: string
  following: string
  repos: string
  prsMerged: string
  mergeRate: string
  mostUsedLanguages: string
  reposWithMostPRs: string
  monthlyContributions: string
  month: string
  prs: string
  issues: string
  commits: string
  activityByTime: string
  events: string
}

export const translations: Record<'en' | 'es', Translations> = {
  en: {
    searchPlaceholder: 'Search GitHub user...',
    searchButton: 'Search',
    heroTitle: 'Explore GitHub activity at a glance',
    heroSubtitle:
      'Search for any GitHub user to see their language usage, PR history, contributions, and activity patterns.',
    loading: 'Loading insights...',
    followers: 'Followers',
    following: 'Following',
    repos: 'Repos',
    prsMerged: 'PRs merged',
    mergeRate: 'Merge rate',
    mostUsedLanguages: 'Most Used Languages',
    reposWithMostPRs: 'Repos with Most PRs',
    monthlyContributions: 'Monthly Contributions',
    month: 'Month',
    prs: 'PRs',
    issues: 'Issues',
    commits: 'Commits',
    activityByTime: 'Activity by Time of Day',
    events: 'events',
  },
  es: {
    searchPlaceholder: 'Buscar usuario de GitHub...',
    searchButton: 'Buscar',
    heroTitle: 'Explora la actividad de GitHub de un vistazo',
    heroSubtitle:
      'Busca cualquier usuario de GitHub para ver su uso de lenguajes, historial de PRs, contribuciones y patrones de actividad.',
    loading: 'Cargando insights...',
    followers: 'Seguidores',
    following: 'Siguiendo',
    repos: 'Repos',
    prsMerged: 'PRs fusionados',
    mergeRate: 'Tasa de merge',
    mostUsedLanguages: 'Lenguajes más usados',
    reposWithMostPRs: 'Repos con más PRs',
    monthlyContributions: 'Contribuciones mensuales',
    month: 'Mes',
    prs: 'PRs',
    issues: 'Issues',
    commits: 'Commits',
    activityByTime: 'Actividad por hora del día',
    events: 'eventos',
  },
}
