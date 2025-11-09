const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000'

export async function loginAdmin(password) {
  const url = `${API_BASE}/login/`
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

export async function validateAdminToken() {
  const url = `${API_BASE}/validate-token/`
  const adminToken = localStorage.getItem('admin_token')
  if (!adminToken) return false

  const res = await fetch(url, {
    method: 'GET',
    headers: { 'Authorization': `Bearer ${adminToken}` },
  })
  return res.ok
}