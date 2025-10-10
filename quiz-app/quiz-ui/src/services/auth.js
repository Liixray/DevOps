const API_BASE = import.meta.env.VITE_API_URL || '/api'

export async function loginAdmin(password) {
  const url = `${API_BASE}/auth/login`
  console.log('POST ->', url)
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ password }),
  })
  if (!res.ok) {
    const txt = await res.text().catch(() => '')
    throw new Error(txt || `HTTP ${res.status}`)
  }
  return (await res.json()).token
}

export async function registerUser({ name, mail, password }) {
  const url = `${API_BASE}/auth/user/register`
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, mail, password }),
  })
  if (res.status !== 201) {
    const txt = await res.text().catch(() => '')
    throw new Error(txt || `HTTP ${res.status}`)
  }
  return await res.json()
}

export async function loginUser(mail, password) {
  const url = `${API_BASE}/auth/user/login`
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ mail, password }),
  })
  if (!res.ok) {
    const txt = await res.text().catch(() => '')
    throw new Error(txt || `HTTP ${res.status}`)
  }
  return (await res.json()).token
}