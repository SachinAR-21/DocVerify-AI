const LABELS = {
  draft: 'Draft',
  submitted: 'Submitted',
  in_review: 'In review',
  needs_documents: 'Action needed',
  accepted: 'Accepted',
  rejected: 'Rejected',
  uploaded: 'Uploaded',
  verified: 'Verified',
  needs_review: 'Needs review',
}

export default function StatusBadge({ status }) {
  return <span className={`badge badge-${status}`}>{LABELS[status] ?? status}</span>
}
