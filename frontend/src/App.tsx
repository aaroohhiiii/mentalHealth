import { useState } from 'react'
import Dashboard from './pages/Dashboard.tsx'
import NewEntry from './pages/NewEntry.tsx'
import Trends from './pages/Trends.tsx'
import Privacy from './pages/Privacy.tsx'
import './App.css'
import mentalHealthIcon from './public/icons/mental-health.png?url'


type Page = 'dashboard' | 'newEntry' | 'trends' | 'privacy'

function App() {
  const [currentPage, setCurrentPage] = useState<Page>('dashboard')
  const [userName] = useState('User') // You can replace this with actual user data

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
