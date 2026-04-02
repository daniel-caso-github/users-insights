import { useState, type FormEvent } from 'react'
import { useApp } from '../context/AppContext'

interface SearchBarProps {
  onSearch: (username: string) => void
  loading: boolean
}

export function SearchBar({ onSearch, loading }: SearchBarProps) {
  const [value, setValue] = useState('')
  const { t } = useApp()

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    const trimmed = value.trim()
    if (trimmed) onSearch(trimmed)
  }

  return (
    <form onSubmit={handleSubmit} className="flex items-center gap-3 w-full max-w-lg">
      <input
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder={t.searchPlaceholder}
        disabled={loading}
        className="flex-1 px-5 py-3 rounded-full bg-surface-variant/60 backdrop-blur-md text-on-surface placeholder-outline border border-outline-variant focus:outline-none focus:border-primary transition-colors text-sm disabled:opacity-50"
      />
      <button
        type="submit"
        disabled={loading || !value.trim()}
        className="px-6 py-3 rounded-full text-on-primary font-medium text-sm transition-opacity disabled:opacity-40 cursor-pointer disabled:cursor-not-allowed"
        style={{ background: 'linear-gradient(135deg, #acc7ff, #0069da)' }}
      >
        {t.searchButton}
      </button>
    </form>
  )
}
