import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, formatDate } from '../api'
import { useAuth } from '../auth'
import StatusBadge from '../components/StatusBadge'

const STATUS_OPTIONS = [
  ['', 'Open (submitted + in review)'],
  ['submitted', 'Submitted'],
  ['in_review', 'In review'],
  ['needs_documents', 'Waiting for applicant'],
  ['accepted', 'Accepted'],
  ['rejected', 'Rejected'],
]

export default function ReviewQueue() {
  const { user } = useAuth()
  const [filters, setFilters] = useState({ status: '', programme: '', sort: 'oldest', mine: false })
  const [applications, setApplications] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    const params = new URLSearchParams({ sort: filters.sort })
    if (filters.status) params.set('status', filters.status)
    if (filters.programme) params.set('programme', filters.programme)
    if (filters.mine) params.set('mine', 'true')
    api(`/api/review/queue?${params}`)
      .then(setApplications)
      .catch((err) => setError(err.message))
  }, [filters])

  function update(field) {
    return (e) => {
      const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value
      setFilters({ ...filters, [field]: value })
    }
  }

  return (
    <>
      <h1>Review queue</h1>
      {error && <p className="error">{error}</p>}

      <div className="card filters">
        <label>
          Status
          <select value={filters.status} onChange={update('status')}>
            {STATUS_OPTIONS.map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
        </label>
        <label>
          Programme
          <input placeholder="Search..." value={filters.programme} onChange={update('programme')} />
        </label>
        <label>
          Sort
          <select value={filters.sort} onChange={update('sort')}>
            <option value="oldest">Oldest first</option>
            <option value="newest">Newest first</option>
            <option value="programme">Programme</option>
          </select>
        </label>
        <label className="checkbox">
          <input type="checkbox" checked={filters.mine} onChange={update('mine')} /> Only mine
        </label>
      </div>

      {applications.length === 0 ? (
        <p className="muted">Nothing to review right now.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Applicant</th>
              <th>Programme</th>
              <th>Status</th>
              <th>Documents</th>
              <th>Submitted</th>
              <th>Reviewer</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {applications.map((a) => (
              <tr key={a.id}>
                <td>{a.id}</td>
                <td>{a.applicant.full_name}</td>
                <td>{a.programme}</td>
                <td>
                  <StatusBadge status={a.status} />
                </td>
                <td>{a.document_count}</td>
                <td>{formatDate(a.submitted_at)}</td>
                <td>
                  {a.reviewer ? (a.reviewer.id === user.id ? 'You' : a.reviewer.full_name) : '-'}
                </td>
                <td>
                  <Link to={`/review/${a.id}`}>Open</Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </>
  )
}
