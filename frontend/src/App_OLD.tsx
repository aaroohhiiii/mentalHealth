import { Routes, Route, Navigate, Link, useNavigate, useLocation } from 'react-router-dom'
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
  const navigate = useNavigate()
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
  if (!user && (location.pathname === '/login' || location.pathname === '/signup')) {
    return (
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    )
  }

  // Redirect to login if not authenticated
  if (!user) {
    return <Navigate to="/login" replace />
  }

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard />
      case 'newEntry':
        return <NewEntry />
      case 'trends':
        return <Trends />
      case 'privacy':
        return <Privacy />
      default:
        return <Dashboard />
    }
  }

  return (
    <div className="app">
      <nav className="navbar">
        <div className="nav-brand">
          <h1 className="app-name">MindEase</h1>
          <p className="motto">Find Calm. Feel Better.</p>
          {/* <img src='../public/icons/healthIcon.png' /> */}
        </div>
        <div className="nav-links">
          <button
            className={currentPage === 'dashboard' ? 'active' : ''}
            onClick={() => setCurrentPage('dashboard')}
          >
            Home
          </button>
          <button
            className={currentPage === 'newEntry' ? 'active' : ''}
            onClick={() => setCurrentPage('newEntry')}
          >
            New Entry
          </button>
          <button
            className={currentPage === 'trends' ? 'active' : ''}
            onClick={() => setCurrentPage('trends')}
          >
            Dashboard
          </button>
          <button
            className={currentPage === 'privacy' ? 'active' : ''}
            onClick={() => setCurrentPage('privacy')}
          >
            Privacy
          </button>
        </div>
      </nav>

      <main className="main-content">
        {currentPage === 'dashboard' && (
          <div className="greeting-section">
            <div className="greeting-container">
              <img 
                src={mentalHealthIcon} 
                alt="Mental Health" 
                className="greeting-image"
              />
              <h1 className="greeting-text">Hey, {userName} </h1>
            </div>
          </div>
        )}
        {renderPage()}
      </main>

      <footer className="footer">
        <div className="disclaimer">
           <strong>Disclaimer:</strong> This is not a medical device. Results are for educational/research purposes only. 
          If you're experiencing mental health concerns, please consult a qualified healthcare professional.
        </div>
        <div className="footer-info">
          {/* <p>Developed by Aarohi (B.Tech) | Mental Health AI Research Project</p> */}
          <p>Privacy-First • Local Processing • Non-Diagnostic</p>
        </div>
      </footer>
    </div>
  )
}

export default App
