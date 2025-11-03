import { Routes, Route, Navigate, useLocation } from 'react-router-dom'
import { useAuth } from './context/AuthContext'
import Dashboard from './pages/Dashboard.tsx'
import NewEntry from './pages/NewEntry.tsx'
import Trends from './pages/Trends.tsx'
import Privacy from './pages/Privacy.tsx'
import Login from './pages/Login.tsx'
import Signup from './pages/Signup.tsx'
import './App.css'

function App() {
  const { user, logout, isLoading } = useAuth()
  const location = useLocation()

  if (isLoading) {
    return (
      <div style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%)',
      }}>
        <div style={{ textAlign: 'center' }}>
          <h2 style={{ color: '#1976d2' }}>Loading...</h2>
        </div>
      </div>
    )
  }

  // Public routes (login, signup)
  if (!user) {
    return (
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    )
  }

  // Authenticated routes
  return (
    <div className="app">
      <nav className="navbar">
        <div className="nav-brand">
          <h1 className="app-name">MindEase</h1>
          <p className="motto">Find Calm. Feel Better.</p>
        </div>
        <div className="nav-links">
          <button
            className={location.pathname === '/' ? 'active' : ''}
            onClick={() => window.location.href = '/'}
          >
            Home
          </button>
          <button
            className={location.pathname === '/new-entry' ? 'active' : ''}
            onClick={() => window.location.href = '/new-entry'}
          >
            New Entry
          </button>
          <button
            className={location.pathname === '/trends' ? 'active' : ''}
            onClick={() => window.location.href = '/trends'}
          >
            Dashboard
          </button>
          <button
            className={location.pathname === '/privacy' ? 'active' : ''}
            onClick={() => window.location.href = '/privacy'}
          >
            Privacy
          </button>
          <button 
            onClick={logout}
            className="logout-btn"
          >
            Logout
          </button>
        </div>
      </nav>

      <main className="main-content">
        {location.pathname === '/' && (
          <div className="welcome-section">
            <div className="welcome-message">
              <h1 className="greeting-text">Hey, {user.username}! 👋</h1>
              <p className="greeting-sub">How are you feeling today?</p>
            </div>
          </div>
        )}

        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/new-entry" element={<NewEntry />} />
          <Route path="/trends" element={<Trends />} />
          <Route path="/privacy" element={<Privacy />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
