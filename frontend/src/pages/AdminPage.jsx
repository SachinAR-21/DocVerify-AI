import { useCallback, useEffect, useState } from 'react'
import { api, formatDate } from '../api'
import { useAuth } from '../auth'

const TABS = ['Overview', 'Users', 'Document types', 'Audit log']

export default function AdminPage() {
  const [tab, setTab] = useState('Overview')
  return (
    <>
      <h1>Administration</h1>
      <div className="tabs">
        {TABS.map((t) => (
          <button key={t} className={t === tab ? 'active' : ''} onClick={() => setTab(t)}>
            {t}
          </button>
        ))}
      </div>
      {tab === 'Overview' && <Overview />}
      {tab === 'Users' && <Users />}
      {tab === 'Document types' && <DocumentTypes />}
      {tab === 'Audit log' && <AuditLog />}
    </>
  )
}

function Overview() {
  const [stats, setStats] = useState(null)
  useEffect(() => {
    api('/api/admin/stats').then(setStats)
  }, [])
  if (!stats) return <p>Loading...</p>
  return (
    <div className="grid">
      <section className="card">
        <h2>Users</h2>
        <ul>
          {Object.entries(stats.users_by_role).map(([role, n]) => (
            <li key={role}>
              {role}: <strong>{n}</strong>
            </li>
          ))}
        </ul>
      </section>
      <section className="card">
        <h2>Applications</h2>
        <ul>
          {Object.entries(stats.applications_by_status).map(([status, n]) => (
            <li key={status}>
              {status.replace('_', ' ')}: <strong>{n}</strong>
            </li>
          ))}
        </ul>
        <p>
          Documents uploaded: <strong>{stats.documents_total}</strong>
        </p>
      </section>
    </div>
  )
}

function Users() {
  const { user: me } = useAuth()
  const [users, setUsers] = useState([])
  const [form, setForm] = useState({ full_name: '', email: '', password: '', role: 'reviewer' })
  const [error, setError] = useState('')

  const load = useCallback(() => {
    api('/api/admin/users').then(setUsers)
  }, [])
  useEffect(load, [load])

  async function change(id, data) {
    setError('')
    try {
      await api(`/api/admin/users/${id}`, { method: 'PATCH', body: data })
      load()
    } catch (err) {
      setError(err.message)
    }
  }

  async function createUser(e) {
    e.preventDefault()
    setError('')
    try {
      await api('/api/admin/users', { method: 'POST', body: form })
      setForm({ full_name: '', email: '', password: '', role: 'reviewer' })
      load()
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <>
      {error && <p className="error">{error}</p>}
      <form className="card inline-form" onSubmit={createUser}>
        <strong>New staff account</strong>
        <input
          placeholder="Full name"
          value={form.full_name}
          onChange={(e) => setForm({ ...form, full_name: e.target.value })}
          required
        />
        <input
          type="email"
          placeholder="Email"
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
          required
        />
        <select value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })}>
          <option value="reviewer">Reviewer</option>
          <option value="admin">Admin</option>
        </select>
        <button type="submit">Create</button>
      </form>

      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Role</th>
            <th>Active</th>
            <th>Created</th>
          </tr>
        </thead>
        <tbody>
          {users.map((u) => (
            <tr key={u.id}>
              <td>{u.full_name}</td>
              <td>{u.email}</td>
              <td>
                <select
                  value={u.role}
                  disabled={u.id === me.id}
                  onChange={(e) => change(u.id, { role: e.target.value })}
                >
                  <option value="applicant">Applicant</option>
                  <option value="reviewer">Reviewer</option>
                  <option value="admin">Admin</option>
                </select>
              </td>
              <td>
                <input
                  type="checkbox"
                  checked={u.is_active}
                  disabled={u.id === me.id}
                  onChange={(e) => change(u.id, { is_active: e.target.checked })}
                />
              </td>
              <td>{formatDate(u.created_at)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  )
}

function DocumentTypes() {
  const [types, setTypes] = useState([])
  const [form, setForm] = useState({ name: '', description: '', is_required: false })
  const [error, setError] = useState('')

  const load = useCallback(() => {
    api('/api/admin/document-types').then(setTypes)
  }, [])
  useEffect(load, [load])

  async function save(id, data) {
    setError('')
    try {
      await api(`/api/admin/document-types/${id}`, { method: 'PATCH', body: data })
      load()
    } catch (err) {
      setError(err.message)
    }
  }

  async function create(e) {
    e.preventDefault()
    setError('')
    try {
      await api('/api/admin/document-types', { method: 'POST', body: form })
      setForm({ name: '', description: '', is_required: false })
      load()
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <>
      {error && <p className="error">{error}</p>}
      <form className="card inline-form" onSubmit={create}>
        <strong>New document type</strong>
        <input
          placeholder="Name"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
          required
        />
        <input
          placeholder="Description"
          value={form.description}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
        />
        <label className="checkbox">
          <input
            type="checkbox"
            checked={form.is_required}
            onChange={(e) => setForm({ ...form, is_required: e.target.checked })}
          />{' '}
          Required
        </label>
        <button type="submit">Add</button>
      </form>

      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Required</th>
            <th>Active</th>
          </tr>
        </thead>
        <tbody>
          {types.map((t) => (
            <tr key={t.id} className={t.is_active ? '' : 'inactive'}>
              <td>{t.name}</td>
              <td>{t.description}</td>
              <td>
                <input
                  type="checkbox"
                  checked={t.is_required}
                  onChange={(e) => save(t.id, { is_required: e.target.checked })}
                />
              </td>
              <td>
                <input
                  type="checkbox"
                  checked={t.is_active}
                  onChange={(e) => save(t.id, { is_active: e.target.checked })}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  )
}

function AuditLog() {
  const [entries, setEntries] = useState([])
  const [action, setAction] = useState('')

  useEffect(() => {
    const query = action ? `?action=${encodeURIComponent(action)}` : ''
    api(`/api/admin/audit-log${query}`).then(setEntries)
  }, [action])

  return (
    <>
      <div className="card filters">
        <label>
          Filter by action
          <input placeholder="e.g. login, access_denied" value={action} onChange={(e) => setAction(e.target.value)} />
        </label>
      </div>
      <table>
        <thead>
          <tr>
            <th>Time</th>
            <th>User</th>
            <th>Action</th>
            <th>Object</th>
            <th>Details</th>
          </tr>
        </thead>
        <tbody>
          {entries.map((e) => (
            <tr key={e.id}>
              <td>{formatDate(e.created_at)}</td>
              <td>{e.user ? e.user.email : '-'}</td>
              <td>
                <code>{e.action}</code>
              </td>
              <td>{e.entity_type ? `${e.entity_type} #${e.entity_id}` : '-'}</td>
              <td>{e.details}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  )
}
