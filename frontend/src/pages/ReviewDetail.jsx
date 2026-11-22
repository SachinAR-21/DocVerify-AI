import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { api, formatDate, formatSize, openDocument } from '../api'
import { useAuth } from '../auth'
import StatusBadge from '../components/StatusBadge'

const DECISION_LABELS = {
  accept: 'Accepted',
  reject: 'Rejected',
  request_documents: 'Requested documents',
}

export default function ReviewDetail() {
  const { id } = useParams()
  const { user } = useAuth()
  const [app, setApp] = useState(null)
  const [decision, setDecision] = useState('accept')
  const [comment, setComment] = useState('')
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')

  useEffect(() => {
    api(`/api/applications/${id}`)
      .then(setApp)
      .catch((err) => setError(err.message))
  }, [id])

  async function startReview() {
    setError('')
    try {
      setApp(await api(`/api/review/applications/${id}/start`, { method: 'POST' }))
    } catch (err) {
      setError(err.message)
    }
  }

  async function sendDecision(e) {
    e.preventDefault()
    setError('')
    try {
      const updated = await api(`/api/review/applications/${id}/decision`, {
        method: 'POST',
        body: { decision, comment },
      })
      setApp(updated)
      setComment('')
      setMessage('Decision saved.')
    } catch (err) {
      setError(err.message)
    }
  }

  if (!app) return <p>{error || 'Loading...'}</p>

  const open = ['submitted', 'in_review'].includes(app.status)
  const someoneElse = app.status === 'in_review' && app.reviewer && app.reviewer.id !== user.id

  return (
    <>
      <p>
        <Link to="/review">&larr; Back to the queue</Link>
      </p>
      <h1>
        Application #{app.id} <StatusBadge status={app.status} />
      </h1>
      {message && <p className="success">{message}</p>}
      {error && <p className="error">{error}</p>}

      <div className="grid">
        <section className="card">
          <h2>Applicant</h2>
          <dl>
            <dt>Name</dt>
            <dd>{app.applicant.full_name}</dd>
            <dt>Email</dt>
            <dd>{app.applicant.email}</dd>
            <dt>Programme</dt>
            <dd>{app.programme}</dd>
            <dt>Submitted</dt>
            <dd>{formatDate(app.submitted_at)}</dd>
            <dt>Reviewer</dt>
            <dd>{app.reviewer ? app.reviewer.full_name : 'not assigned'}</dd>
          </dl>
          {app.missing_document_types.length > 0 && (
            <p className="error">Missing: {app.missing_document_types.map((t) => t.name).join(', ')}</p>
          )}
        </section>

        <section className="card">
          <h2>Decision</h2>
          {!open && <p className="muted">This application is closed or waiting for the applicant.</p>}
          {open && app.status === 'submitted' && (
            <p>
              <button onClick={startReview}>Start review</button>{' '}
              <span className="muted small">Shows the others that you are working on it.</span>
            </p>
          )}
          {someoneElse && <p className="warning">{app.reviewer.full_name} is already reviewing this.</p>}
          {open && (
            <form onSubmit={sendDecision}>
              <label className="radio">
                <input
                  type="radio"
                  checked={decision === 'accept'}
                  onChange={() => setDecision('accept')}
                />{' '}
                Accept
              </label>
              <label className="radio">
                <input
                  type="radio"
                  checked={decision === 'request_documents'}
                  onChange={() => setDecision('request_documents')}
                />{' '}
                Request more documents
              </label>
              <label className="radio">
                <input
                  type="radio"
                  checked={decision === 'reject'}
                  onChange={() => setDecision('reject')}
                />{' '}
                Reject
              </label>
              <label>
                Comment for the applicant {decision !== 'accept' && '(required)'}
                <textarea rows="3" value={comment} onChange={(e) => setComment(e.target.value)} />
              </label>
              <button type="submit">Save decision</button>
            </form>
          )}
        </section>
      </div>

      <h2>Documents</h2>
      <p className="muted small">
        The AI verification report will be shown here in Phase 3. For now the documents are checked manually.
      </p>
      <table>
        <thead>
          <tr>
            <th>Type</th>
            <th>File</th>
            <th>Notes from applicant</th>
            <th>Size</th>
            <th>Uploaded</th>
          </tr>
        </thead>
        <tbody>
          {app.documents.map((d) => (
            <tr key={d.id}>
              <td>{d.document_type.name}</td>
              <td>
                <button className="link" onClick={() => openDocument(d.id).catch((e) => setError(e.message))}>
                  {d.original_filename}
                </button>
              </td>
              <td>{d.notes || '-'}</td>
              <td>{formatSize(d.size_bytes)}</td>
              <td>{formatDate(d.uploaded_at)}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {app.decisions.length > 0 && (
        <>
          <h2>History</h2>
          <ul className="history">
            {app.decisions.map((d) => (
              <li key={d.id}>
                <strong>{DECISION_LABELS[d.decision]}</strong> by {d.reviewer.full_name} on{' '}
                {formatDate(d.created_at)}
                {d.comment && <div className="muted">{d.comment}</div>}
              </li>
            ))}
          </ul>
        </>
      )}
    </>
  )
}
