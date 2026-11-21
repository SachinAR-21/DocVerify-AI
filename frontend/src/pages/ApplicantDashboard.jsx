import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { api, formatDate } from '../api'
import StatusBadge from '../components/StatusBadge'

export default function ApplicantDashboard() {
  const navigate = useNavigate()
  const [applications, setApplications] = useState([])
  const [programme, setProgramme] = useState('')
  const [error, setError] = useState('')

  useEffect(() => {
    api('/api/applications')
      .then(setApplications)
      .catch((err) => setError(err.message))
  }, [])

  async function createApplication(e) {
    e.preventDefault()
    setError('')
    try {
      const app = await api('/api/applications', { method: 'POST', body: { programme } })
      navigate(`/applications/${app.id}`)
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <>
      <h1>My applications</h1>
      {error && <p className="error">{error}</p>}

      <form className="card inline-form" onSubmit={createApplication}>
        <label>
          Start a new application for
          <input
            placeholder="e.g. MSc Data Science"
            value={programme}
            onChange={(e) => setProgramme(e.target.value)}
            required
          />
        </label>
        <button type="submit">Create</button>
      </form>

      {applications.length === 0 ? (
        <p className="muted">You have no applications yet.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Programme</th>
              <th>Status</th>
              <th>Documents</th>
              <th>Last change</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {applications.map((a) => (
              <tr key={a.id}>
                <td>{a.programme}</td>
                <td>
                  <StatusBadge status={a.status} />
                </td>
                <td>{a.document_count}</td>
                <td>{formatDate(a.updated_at)}</td>
                <td>
                  <Link to={`/applications/${a.id}`}>Open</Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </>
  )
}
