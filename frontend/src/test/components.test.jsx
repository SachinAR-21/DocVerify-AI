import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { describe, expect, it } from 'vitest'
import { AuthProvider } from '../auth'
import StatusBadge from '../components/StatusBadge'
import Login from '../pages/Login'

describe('StatusBadge', () => {
  it('shows a readable label', () => {
    render(<StatusBadge status="needs_documents" />)
    expect(screen.getByText('Action needed')).toBeInTheDocument()
  })
})

describe('Login page', () => {
  it('shows the login form and a link to register', () => {
    render(
      <MemoryRouter>
        <AuthProvider>
          <Login />
        </AuthProvider>
      </MemoryRouter>,
    )
    expect(screen.getByRole('button', { name: 'Log in' })).toBeInTheDocument()
    expect(screen.getByText('Register as applicant')).toBeInTheDocument()
  })
})
