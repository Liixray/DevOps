const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000'

export async function getLeaderboard(page = 1, itemsPerPage = 20) {
  const url = `${API_BASE}/participations/leaderboard?page=${page}&limit=${itemsPerPage}`
  const res = await fetch(url)
  if (!res.ok) {
    throw new Error(`Erreur HTTP ${res.status}`)
  }
  return await res.json()
}