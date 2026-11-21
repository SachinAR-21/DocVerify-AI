import { Link, NavLink, Navigate, Outlet } from 'react-router-dom'
import { homePathFor, useAuth } from '../auth'

const MENU = {
  applicant: [{ to: '/applications', label: 'My applications' }],
  reviewer: [{ to: '/review', label: 'Review queue' }],
  admin: [
    { to: '/review', label: 'Review queue' },
    { to: '/admin', label: 'Administration' },
  ],
}

// Page frame with the top bar. Also redirects to /login if nobody is logged in.
export default function Layout({ roles }) {
  const { user, loading, logout } = useAuth()

  if (loading) return <p className="container">Loading...</p>
  if (!user) return <Navigate to="/login" replace />
  if (roles && !roles.includes(user.role)) return <Navigate to={homePathFor(user)} replace />

  return (
    <>
      <header className="topbar">
        <Link to={homePathFor(user)} className="logo">
          DocVerify <span>AI</span>
        </Link>
        <nav>
          {MENU[user.role].map((item) => (
            <NavLink key={item.to} to={item.to}>
              {item.label}
            </NavLink>
          ))}
        </nav>
        <div className="user">
          {user.full_name} <small>({user.role})</small>
          <button className="link" onClick={logout}>
            Log out
          </button>
        </div>
      </header>
      <main className="container">
        <Outlet />
      </main>
    </>
  )
}
