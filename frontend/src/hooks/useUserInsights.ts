import { useState, useEffect } from 'react'
import type { GitHubUserInsightsResponse } from '../types/github'

interface UseUserInsightsResult {
  data: GitHubUserInsightsResponse | null
  loading: boolean
  error: string | null
}

export function useUserInsights(username: string | null): UseUserInsightsResult {
  const [data, setData] = useState<GitHubUserInsightsResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!username) {
      setData(null)
      setError(null)
      return
    }

    setLoading(true)
    setError(null)
    setData(null)

    fetch(`http://localhost:8000/user-insights/${username}`)
      .then((res) => {
        if (!res.ok) {
          if (res.status === 404) throw new Error(`Usuario "${username}" no encontrado`)
          throw new Error(`Error ${res.status}: ${res.statusText}`)
        }
        return res.json()
      })
      .then((json: GitHubUserInsightsResponse) => {
        setData(json)
      })
      .catch((err: Error) => {
        setError(err.message)
      })
      .finally(() => {
        setLoading(false)
      })
  }, [username])

  return { data, loading, error }
}
