import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { api } from '../api'
import { useAuth } from '../auth'

export default function Register() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ full_name: '', email: '', password: '', repeat: '' })
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  function update(field) {
    return (e) => setForm({ ...form, [field]: e.target.value })
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    if (form.password !== form.repeat) {
      setError('The passwords do not match')
      return
    }
    setBusy(true)
    try {
      await api('/api/auth/register', {
        method: 'POST',
        body: { full_name: form.full_name, email: form.email, password: form.password },
      })
      await login(form.email, form.password)
      navigate('/applications')
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="auth-page">
      <form className="card auth-card" onSubmit={handleSubmit}>
        <h1>Create an account</h1>
        <p className="muted">For applicants. Staff accounts are created by the administrator.</p>
        {error && <p className="error">{error}</p>}
        <label>
          Full name
          <input value={form.full_name} onChange={update('full_name')} required />
        </label>
        <label>
          Email
          <input type="email" value={form.email} onChange={update('email')} required />
        </label>
        <label>
          Password
          <input type="password" value={form.password} onChange={update('password')} required />
          <small className="muted">At least 8 characters with letters and numbers.</small>
        </label>
        <label>
          Repeat password
          <input type="password" value={form.repeat} onChange={update('repeat')} required />
        </label>
        <button type="submit" disabled={busy}>
          {busy ? 'Creating account...' : 'Register'}
        </button>
        <p className="muted">
          Already registered? <Link to="/login">Log in</Link>
        </p>
      </form>
    </div>
  )
}
