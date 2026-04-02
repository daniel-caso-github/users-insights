import { createContext, useContext, useEffect, useState, type ReactNode } from 'react'
import { translations, type Translations } from '../i18n/translations'

type Theme = 'dark' | 'light'
type Lang = 'en' | 'es'

interface AppContextValue {
  theme: Theme
  toggleTheme: () => void
  lang: Lang
  setLang: (lang: Lang) => void
  t: Translations
}

const AppContext = createContext<AppContextValue | null>(null)

export function AppProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>(
    () => (localStorage.getItem('theme') as Theme) ?? 'dark',
  )
  const [lang, setLangState] = useState<Lang>(
    () => (localStorage.getItem('lang') as Lang) ?? 'en',
  )

  useEffect(() => {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
    localStorage.setItem('theme', theme)
  }, [theme])

  function toggleTheme() {
    setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'))
  }

  function setLang(newLang: Lang) {
    setLangState(newLang)
    localStorage.setItem('lang', newLang)
  }

  return (
    <AppContext.Provider value={{ theme, toggleTheme, lang, setLang, t: translations[lang] }}>
      {children}
    </AppContext.Provider>
  )
}

export function useApp() {
  const ctx = useContext(AppContext)
  if (!ctx) throw new Error('useApp must be used within AppProvider')
  return ctx
}
