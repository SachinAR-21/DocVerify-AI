import { Navigate, Route, Routes } from 'react-router-dom'
import { homePathFor, useAuth } from './auth'
import Layout from './components/Layout'
import ApplicantDashboard from './pages/ApplicantDashboard'
import ApplicationDetail from './pages/ApplicationDetail'
import Login from './pages/Login'
import Register from './pages/Register'
import ReviewDetail from './pages/ReviewDetail'
import ReviewQueue from './pages/ReviewQueue'

// placeholder until the page is built in the next pull request
function ComingSoon({ title }) {
  return (
    <>
      <h1>{title}</h1>
      <p className="muted">This page is coming in the next sprint.</p>
    </>
  )
}

function Home() {
  const { user, loading } = useAuth()
  if (loading) return null
  return <Navigate to={homePathFor(user)} replace />
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      <Route element={<Layout roles={['applicant']} />}>
        <Route path="/applications" element={<ApplicantDashboard />} />
        <Route path="/applications/:id" element={<ApplicationDetail />} />
      </Route>

      <Route element={<Layout roles={['reviewer', 'admin']} />}>
        <Route path="/review" element={<ReviewQueue />} />
        <Route path="/review/:id" element={<ReviewDetail />} />
      </Route>

      <Route element={<Layout roles={['admin']} />}>
        <Route path="/admin" element={<ComingSoon title="Administration" />} />
      </Route>

      <Route path="*" element={<Home />} />
    </Routes>
  )
}
