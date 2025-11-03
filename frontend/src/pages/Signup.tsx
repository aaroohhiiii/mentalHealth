import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const Signup: React.FC = () => {
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const { signup } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    // Validation
    if (username.length < 3) {
      setError('Username must be at least 3 characters')
      return
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters')
      return
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match')
      return
    }

    if (!email.includes('@')) {
      setError('Please enter a valid email address')
      return
    }

    setIsLoading(true)

    try {
      await signup(username, email, password)
      navigate('/dashboard')
    } catch (err: any) {
      console.error('Signup error:', err)
      setError(err.response?.data?.detail || 'Failed to create account')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={styles.header}>
          <h1 style={styles.logo}>MindEase</h1>
          <p style={styles.tagline}>Find Calm. Feel Better.</p>
        </div>

        <h2 style={styles.title}>Create Account</h2>
        <p style={styles.subtitle}>Start your mental wellness journey today</p>

        {error && (
          <div style={styles.error}>
            <span style={styles.errorIcon}>⚠️</span>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} style={styles.form}>
          <div style={styles.formGroup}>
            <label style={styles.label}>Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Choose a username"
              required
              style={styles.input}
              disabled={isLoading}
            />
          </div>

          <div style={styles.formGroup}>
            <label style={styles.label}>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="your.email@example.com"
              required
              style={styles.input}
              disabled={isLoading}
            />
          </div>

          <div style={styles.formGroup}>
            <label style={styles.label}>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Create a secure password"
              required
              style={styles.input}
              disabled={isLoading}
            />
          </div>

          <div style={styles.formGroup}>
            <label style={styles.label}>Confirm Password</label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Confirm your password"
              required
              style={styles.input}
              disabled={isLoading}
            />
          </div>

          <button
            type="submit"
            style={{
              ...styles.button,
              ...(isLoading ? styles.buttonDisabled : {}),
            }}
            disabled={isLoading}
          >
            {isLoading ? 'Creating Account...' : 'Sign Up'}
          </button>
        </form>

        <div style={styles.footer}>
          <p style={styles.footerText}>
            Already have an account?{' '}
            <Link to="/login" style={styles.link}>
              Sign in
            </Link>
          </p>
        </div>
      </div>

      <div style={styles.decorativeCircle1} />
      <div style={styles.decorativeCircle2} />
    </div>
  )
}

const styles = {
  container: {
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: 'linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%)',
    padding: '2rem',
    position: 'relative' as const,
    overflow: 'hidden',
  },
  card: {
    background: 'white',
    borderRadius: '16px',
    padding: '3rem',
    maxWidth: '450px',
    width: '100%',
    boxShadow: '0 10px 40px rgba(0, 0, 0, 0.1)',
    position: 'relative' as const,
    zIndex: 10,
  },
  header: {
    textAlign: 'center' as const,
    marginBottom: '2rem',
  },
  logo: {
    fontSize: '2.5rem',
    fontWeight: 'bold' as const,
    color: '#1976d2',
    margin: '0',
    fontFamily: "'Poppins', sans-serif",
  },
  tagline: {
    fontSize: '0.95rem',
    color: '#64b5f6',
    margin: '0.5rem 0 0 0',
    fontStyle: 'italic' as const,
  },
  title: {
    fontSize: '1.75rem',
    fontWeight: 'bold' as const,
    color: '#2c3e50',
    marginBottom: '0.5rem',
    textAlign: 'center' as const,
  },
  subtitle: {
    fontSize: '0.95rem',
    color: '#7f8c8d',
    marginBottom: '2rem',
    textAlign: 'center' as const,
  },
  error: {
    background: '#ffebee',
    color: '#c62828',
    padding: '0.75rem 1rem',
    borderRadius: '8px',
    marginBottom: '1.5rem',
    fontSize: '0.9rem',
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    border: '1px solid #ef9a9a',
  },
  errorIcon: {
    fontSize: '1.2rem',
  },
  form: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '1.25rem',
  },
  formGroup: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '0.5rem',
  },
  label: {
    fontSize: '0.9rem',
    fontWeight: '600' as const,
    color: '#34495e',
  },
  input: {
    padding: '0.875rem 1rem',
    fontSize: '1rem',
    border: '2px solid #e0e0e0',
    borderRadius: '8px',
    transition: 'all 0.3s ease',
    fontFamily: 'inherit',
  },
  button: {
    background: 'linear-gradient(135deg, #42a5f5 0%, #1976d2 100%)',
    color: 'white',
    border: 'none',
    padding: '1rem',
    borderRadius: '8px',
    fontSize: '1.05rem',
    fontWeight: 'bold' as const,
    cursor: 'pointer' as const,
    transition: 'transform 0.2s ease, box-shadow 0.2s ease',
    marginTop: '0.5rem',
  },
  buttonDisabled: {
    opacity: 0.6,
    cursor: 'not-allowed' as const,
  },
  footer: {
    marginTop: '2rem',
    textAlign: 'center' as const,
  },
  footerText: {
    fontSize: '0.9rem',
    color: '#7f8c8d',
  },
  link: {
    color: '#1976d2',
    textDecoration: 'none',
    fontWeight: '600' as const,
  },
  decorativeCircle1: {
    position: 'absolute' as const,
    width: '400px',
    height: '400px',
    borderRadius: '50%',
    background: 'linear-gradient(135deg, rgba(66, 165, 245, 0.2), rgba(25, 118, 210, 0.1))',
    top: '-200px',
    left: '-200px',
    zIndex: 1,
  },
  decorativeCircle2: {
    position: 'absolute' as const,
    width: '300px',
    height: '300px',
    borderRadius: '50%',
    background: 'linear-gradient(135deg, rgba(100, 181, 246, 0.15), rgba(66, 165, 245, 0.1))',
    bottom: '-150px',
    right: '-150px',
    zIndex: 1,
  },
}

export default Signup
