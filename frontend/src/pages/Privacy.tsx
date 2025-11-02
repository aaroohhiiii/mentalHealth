import { useState } from 'react'
import axios from 'axios'

const API_BASE = 'http://localhost:8000'

function Privacy() {
  const [stats, setStats] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [showConfirm, setShowConfirm] = useState(false)

  const fetchStats = async () => {
    try {
      setLoading(true)
      const response = await axios.get(`${API_BASE}/stats`)
      setStats(response.data)
    } catch (err) {
      console.error('Error fetching stats:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteData = async () => {
    try {
      setLoading(true)
      await axios.delete(`${API_BASE}/purge`)
      alert('All data deleted successfully!')
      setShowConfirm(false)
      await fetchStats()
    } catch (err) {
      console.error('Error deleting data:', err)
      alert('Failed to delete data. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <div className="card">
        <h2>🔒 Privacy & Data Control</h2>
        <p>Your privacy is our priority. All data is processed locally and you have full control.</p>
      </div>

      <div className="card">
        <h3>📊 Your Data</h3>
        <button onClick={fetchStats} disabled={loading} style={styles.button}>
          {loading ? 'Loading...' : 'Check My Data'}
        </button>

        {stats && (
          <div style={styles.statsBox}>
            <h4>Storage Statistics</h4>
            <ul style={styles.statsList}>
              <li><strong>Total Entries:</strong> {stats.total_entries}</li>
              <li><strong>Text Entries:</strong> {stats.by_modality?.text || 0}</li>
              <li><strong>Audio Entries:</strong> {stats.by_modality?.audio || 0}</li>
              <li><strong>Image Entries:</strong> {stats.by_modality?.image || 0}</li>
              <li><strong>Daily Aggregates:</strong> {stats.by_modality?.daily_aggregate || 0}</li>
              <li><strong>Storage Mode:</strong> {stats.storage_mode}</li>
              {stats.oldest_entry && (
                <li><strong>Oldest Entry:</strong> {new Date(stats.oldest_entry).toLocaleString()}</li>
              )}
              {stats.newest_entry && (
                <li><strong>Newest Entry:</strong> {new Date(stats.newest_entry).toLocaleString()}</li>
              )}
            </ul>
          </div>
        )}
      </div>

      <div className="card" style={styles.dangerZone}>
        <h3>⚠️ Delete All Data</h3>
        <p>Permanently delete all your stored analysis data. This action cannot be undone.</p>

        {!showConfirm ? (
          <button onClick={() => setShowConfirm(true)} style={styles.deleteButton}>
            Delete My Data
          </button>
        ) : (
          <div style={styles.confirmBox}>
            <p style={styles.confirmText}>
              Are you sure? This will permanently delete all your entries.
            </p>
            <div style={styles.confirmButtons}>
              <button onClick={handleDeleteData} disabled={loading} style={styles.confirmDelete}>
                {loading ? 'Deleting...' : 'Yes, Delete Everything'}
              </button>
              <button onClick={() => setShowConfirm(false)} style={styles.cancelButton}>
                Cancel
              </button>
            </div>
          </div>
        )}
      </div>

      <div className="card">
        <h3>🛡️ Privacy Policy</h3>
        <div style={styles.policyText}>
          <h4>How We Handle Your Data:</h4>
          <ul style={styles.list}>
            <li><strong>Local Processing:</strong> All analysis happens locally on your device</li>
            <li><strong>In-Memory Storage:</strong> By default, data is stored in memory and cleared on restart</li>
            <li><strong>No Cloud Upload:</strong> Your text, audio, and images never leave your machine</li>
            <li><strong>Anonymized:</strong> No personal identifiers are collected</li>
            <li><strong>Delete Anytime:</strong> You can permanently delete all data with one click</li>
          </ul>

          <h4>What We Do NOT Do:</h4>
          <ul style={styles.list}>
            <li>❌ We do NOT share your data with third parties</li>
            <li>❌ We do NOT use your data for advertising</li>
            <li>❌ We do NOT store raw audio or images permanently</li>
            <li>❌ We do NOT make medical diagnoses</li>
            <li>❌ We do NOT replace professional mental health care</li>
          </ul>

          <h4>Your Rights:</h4>
          <ul style={styles.list}>
            <li>✅ Right to view all stored data</li>
            <li>✅ Right to delete all data anytime</li>
            <li>✅ Right to export your data (future feature)</li>
            <li>✅ Right to use the system completely offline</li>
          </ul>
        </div>
      </div>

      <div className="card" style={styles.disclaimer}>
        <h3>⚖️ Legal Disclaimer</h3>
        <p style={styles.disclaimerText}>
          This Mental Health AI Monitor is an <strong>educational and research tool</strong> developed 
          by Aarohi (B.Tech). It is <strong>NOT a medical device</strong> and does <strong>NOT provide 
          medical diagnoses or treatment</strong>. The risk scores and suggestions are generated by 
          machine learning models and should not be considered as professional medical advice.
        </p>
        <p style={styles.disclaimerText}>
          If you are experiencing mental health concerns, please consult a licensed mental health 
          professional. In case of emergency, contact your local crisis helpline:
        </p>
        <ul style={styles.helplines}>
          <li>🇺🇸 US: 988 (Suicide & Crisis Lifeline)</li>
          <li>🇬🇧 UK: 116 123 (Samaritans)</li>
          <li>🇮🇳 India: +91-9152987821 (Vandrevala Foundation)</li>
          <li>🌍 International: <a href="https://findahelpline.com" target="_blank" rel="noopener noreferrer">findahelpline.com</a></li>
        </ul>
      </div>
    </div>
  )
}

const styles = {
  button: {
    background: '#667eea',
    color: 'white',
    border: 'none',
    padding: '0.75rem 2rem',
    borderRadius: '8px',
    fontSize: '1rem',
    fontWeight: 'bold' as const,
    cursor: 'pointer' as const,
    marginTop: '1rem',
  },
  statsBox: {
    marginTop: '1.5rem',
    padding: '1rem',
    background: '#f9f9f9',
    borderRadius: '8px',
    border: '1px solid #ddd',
  },
  statsList: {
    listStyle: 'none',
    padding: 0,
    lineHeight: '1.8',
  },
  dangerZone: {
    background: 'rgba(239, 68, 68, 0.05)',
    border: '2px solid #ef4444',
  },
  deleteButton: {
    background: '#ef4444',
    color: 'white',
    border: 'none',
    padding: '0.75rem 2rem',
    borderRadius: '8px',
    fontSize: '1rem',
    fontWeight: 'bold' as const,
    cursor: 'pointer' as const,
    marginTop: '1rem',
  },
  confirmBox: {
    marginTop: '1rem',
    padding: '1rem',
    background: '#fee',
    borderRadius: '8px',
    border: '1px solid #f88',
  },
  confirmText: {
    color: '#c00',
    fontWeight: 'bold' as const,
    marginBottom: '1rem',
  },
  confirmButtons: {
    display: 'flex',
    gap: '1rem',
    flexWrap: 'wrap' as const,
  },
  confirmDelete: {
    background: '#dc2626',
    color: 'white',
    border: 'none',
    padding: '0.75rem 1.5rem',
    borderRadius: '8px',
    fontSize: '0.95rem',
    fontWeight: 'bold' as const,
    cursor: 'pointer' as const,
  },
  cancelButton: {
    background: '#999',
    color: 'white',
    border: 'none',
    padding: '0.75rem 1.5rem',
    borderRadius: '8px',
    fontSize: '0.95rem',
    fontWeight: 'bold' as const,
    cursor: 'pointer' as const,
  },
  policyText: {
    lineHeight: '1.6',
  },
  list: {
    paddingLeft: '1.5rem',
    lineHeight: '1.8',
    marginBottom: '1.5rem',
  },
  disclaimer: {
    background: 'rgba(255, 193, 7, 0.1)',
    border: '2px solid #ffc107',
  },
  disclaimerText: {
    lineHeight: '1.6',
    marginBottom: '1rem',
  },
  helplines: {
    listStyle: 'none',
    padding: '1rem',
    background: 'white',
    borderRadius: '8px',
    lineHeight: '1.8',
  },
}

export default Privacy
