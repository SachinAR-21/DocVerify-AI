import { afterEach, describe, expect, it, vi } from 'vitest'
import { api, errorMessage, formatSize, setToken } from '../api'

describe('errorMessage', () => {
  it('uses the detail text from the backend', () => {
    expect(errorMessage({ detail: 'Wrong email or password' }, 401)).toBe('Wrong email or password')
  })

  it('joins FastAPI validation errors', () => {
    const data = { detail: [{ loc: ['body', 'email'], msg: 'not a valid email' }] }
    expect(errorMessage(data, 422)).toBe('email: not a valid email')
  })

  it('has a fallback message', () => {
    expect(errorMessage(null, 500)).toBe('Request failed (500)')
  })
})

describe('formatSize', () => {
  it('formats bytes, KB and MB', () => {
    expect(formatSize(500)).toBe('500 B')
    expect(formatSize(2048)).toBe('2 KB')
    expect(formatSize(3 * 1024 * 1024)).toBe('3.0 MB')
  })
})

describe('api', () => {
  afterEach(() => {
    vi.restoreAllMocks()
    setToken(null)
  })

  it('sends the token and JSON body', async () => {
    setToken('abc')
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockResolvedValue(
      new Response(JSON.stringify({ id: 1 }), { status: 201 }),
    )
    const result = await api('/api/applications', { method: 'POST', body: { programme: 'MSc' } })

    expect(result).toEqual({ id: 1 })
    const [, options] = fetchMock.mock.calls[0]
    expect(options.headers.Authorization).toBe('Bearer abc')
    expect(options.body).toBe('{"programme":"MSc"}')
  })

  it('throws an error with the backend message', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(
      new Response(JSON.stringify({ detail: 'Not logged in' }), { status: 401 }),
    )
    await expect(api('/api/auth/me')).rejects.toThrow('Not logged in')
  })
})
