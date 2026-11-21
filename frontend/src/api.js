// Small helper around fetch() that adds the login token and turns errors into messages.

const TOKEN_KEY = 'docverify_token'

export function getToken() {
  try {
    return localStorage.getItem(TOKEN_KEY)
  } catch {
    return null
  }
}

export function setToken(token) {
  try {
    if (token) localStorage.setItem(TOKEN_KEY, token)
    else localStorage.removeItem(TOKEN_KEY)
  } catch {
    // ignore (private mode etc.)
  }
}

export function errorMessage(data, status) {
  if (!data || !data.detail) return `Request failed (${status})`
  if (typeof data.detail === 'string') return data.detail
  // FastAPI validation errors come as a list
  if (Array.isArray(data.detail)) {
    return data.detail.map((d) => `${d.loc?.slice(-1)[0] ?? 'field'}: ${d.msg}`).join(', ')
  }
  return `Request failed (${status})`
}

export async function api(path, { method = 'GET', body, form } = {}) {
  const headers = {}
  const token = getToken()
  if (token) headers.Authorization = `Bearer ${token}`

  let payload
  if (form) {
    payload = form // FormData, the browser sets the content type
  } else if (body !== undefined) {
    headers['Content-Type'] = 'application/json'
    payload = JSON.stringify(body)
  }

  const response = await fetch(path, { method, headers, body: payload })
  if (response.status === 204) return null

  const data = await response.json().catch(() => null)
  if (!response.ok) {
    const error = new Error(errorMessage(data, response.status))
    error.status = response.status
    throw error
  }
  return data
}

// Opens an uploaded document in a new tab (needs the token, so we fetch it as a blob)
export async function openDocument(docId) {
  const response = await fetch(`/api/documents/${docId}/file`, {
    headers: { Authorization: `Bearer ${getToken()}` },
  })
  if (!response.ok) throw new Error('Could not open the document')
  const blob = await response.blob()
  const url = URL.createObjectURL(blob)
  window.open(url, '_blank')
  setTimeout(() => URL.revokeObjectURL(url), 60000)
}

export function formatDate(value) {
  if (!value) return '-'
  return new Date(value + 'Z').toLocaleString()
}

export function formatSize(bytes) {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`
}
