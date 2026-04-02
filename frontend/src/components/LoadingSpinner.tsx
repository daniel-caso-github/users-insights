import { useApp } from '../context/AppContext'

export function LoadingSpinner() {
  const { t } = useApp()

  return (
    <div className="flex flex-col items-center justify-center gap-4 py-20">
      <div className="w-12 h-12 rounded-full border-4 border-surface-container-high border-t-primary animate-spin" />
      <p className="text-on-surface-variant text-sm">{t.loading}</p>
    </div>
  )
}
