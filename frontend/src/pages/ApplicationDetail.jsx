import { useCallback, useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { api, formatDate, formatSize, openDocument } from '../api'
import StatusBadge from '../components/StatusBadge'

const MAX_MB = 10
const EDITABLE = ['draft', 'needs_documents']

export default function ApplicationDetail() {
  const { id } = useParams()
  const [app, setApp] = useState(null)
  const [types, setTypes] = useState([])
  const [typeId, setTypeId] = useState('')
  const [file, setFile] = useState(null)
  const [notes, setNotes] = useState('')
  const [fileKey, setFileKey] = useState(0) // to reset the file input
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  const load = useCallback(() => {
    api(`/api/applications/${id}`)
      .then(setApp)
      .catch((err) => setError(err.message))
  }, [id])

  useEffect(() => {
    load()
    api('/api/document-types').then((list) => {
      setTypes(list)
      if (list.length) setTypeId(String(list[0].id))
    })
  }, [load])

  function chooseFile(e) {
    const selected = e.target.files[0]
    setError('')
    // quick checks in the browser, the server checks again
    if (selected && !/\.(pdf|jpe?g|png)$/i.test(selected.name)) {
      setError('Only PDF, JPG and PNG files are allowed')
      setFile(null)
      return
    }
    if (selected && selected.size > MAX_MB * 1024 * 1024) {
      setError(`The file is bigger than ${MAX_MB} MB`)
      setFile(null)
      return
    }
    setFile(selected)
  }

  async function uploadFile(e) {
    e.preventDefault()
    if (!file) return
    const form = new FormData()
    form.append('document_type_id', typeId)
    form.append('notes', notes)
    form.append('file', file)
    setBusy(true)
    setError('')
    setMessage('')
    try {
      await api(`/api/applications/${id}/documents`, { method: 'POST', form })
      setMessage(`${file.name} was uploaded`)
      setFile(null)
      setNotes('')
      setFileKey((k) => k + 1)
      load()
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  async function deleteDocument(docId) {
    if (!window.confirm('Remove this document?')) return
    try {
      await api(`/api/documents/${docId}`, { method: 'DELETE' })
      load()
    } catch (err) {
      setError(err.message)
    }
  }

  async function submit() {
    setError('')
    try {
      setApp(await api(`/api/applications/${id}/submit`, { method: 'POST' }))
      setMessage('Your application was submitted. You will see the result here.')
    } catch (err) {
      setError(err.message)
    }
  }

  if (!app) return <p>{error || 'Loading...'}</p>

  const editable = EDITABLE.includes(app.status)
  const lastDecision = app.decisions[app.decisions.length - 1]

  return (
    <>
      <p>
        <Link to="/applications">&larr; Back to my applications</Link>
      </p>
      <h1>
        {app.programme} <StatusBadge status={app.status} />
      </h1>
      {message && <p className="success">{message}</p>}
      {error && <p className="error">{error}</p>}

      {lastDecision && lastDecision.comment && (
        <div className={`card note note-${lastDecision.decision}`}>
          <strong>Message from the reviewer ({formatDate(lastDecision.created_at)}):</strong>
          <p>{lastDecision.comment}</p>
        </div>
      )}

      <div className="grid">
        <section className="card">
          <h2>Checklist</h2>
          {app.missing_document_types.length === 0 ? (
            <p className="success">All required documents are uploaded.</p>
          ) : (
            <>
              <p>Still missing:</p>
              <ul>
                {app.missing_document_types.map((t) => (
                  <li key={t.id}>{t.name}</li>
                ))}
              </ul>
            </>
          )}
          {editable && (
            <button onClick={submit} disabled={app.missing_document_types.length > 0}>
              {app.status === 'needs_documents' ? 'Submit again' : 'Submit application'}
            </button>
          )}
        </section>

        {editable && (
          <section className="card">
            <h2>Upload a document</h2>
            <form onSubmit={uploadFile}>
              <label>
                Document type
                <select value={typeId} onChange={(e) => setTypeId(e.target.value)}>
                  {types.map((t) => (
                    <option key={t.id} value={t.id}>
                      {t.name} {t.is_required ? '(required)' : ''}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                File (PDF, JPG or PNG, max {MAX_MB} MB)
                <input key={fileKey} type="file" accept=".pdf,.jpg,.jpeg,.png" onChange={chooseFile} />
              </label>
              <label>
                Notes (optional)
                <textarea
                  rows="2"
                  placeholder="e.g. my name is spelled differently on this certificate"
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                />
              </label>
              <button type="submit" disabled={!file || busy}>
                {busy ? 'Uploading...' : 'Upload'}
              </button>
            </form>
          </section>
        )}
      </div>

      <h2>Documents</h2>
      {app.documents.length === 0 ? (
        <p className="muted">No documents uploaded yet.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Type</th>
              <th>File</th>
              <th>Size</th>
              <th>Status</th>
              <th>Uploaded</th>
              <th></th>
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
                  {d.notes && <div className="muted small">{d.notes}</div>}
                </td>
                <td>{formatSize(d.size_bytes)}</td>
                <td>
                  <StatusBadge status={d.status} />
                </td>
                <td>{formatDate(d.uploaded_at)}</td>
                <td>
                  {editable && (
                    <button className="link danger" onClick={() => deleteDocument(d.id)}>
                      Remove
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </>
  )
}
