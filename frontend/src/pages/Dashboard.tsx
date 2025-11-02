import { useEffect, useState } from 'react'
import axios from 'axios'
import RiskGauge from '../components/RiskGauge'
import ModalityCard from '../components/ModalityCard'
import TrendChart from '../components/TrendChart'

const API_BASE = 'http://localhost:8000'

interface DashboardData {
  latestScore: number | null
  latestBucket: string
  textData: any
  audioData: any
  imageData: any
  trendData: {
    dates: string[]
    scores: (number | null)[]
    buckets: string[]
  }
}

function Dashboard() {
  const [data, setData] = useState<DashboardData>({
    latestScore: null,
    latestBucket: 'No Data',
    textData: null,
    audioData: null,
    imageData: null,
    trendData: { dates: [], scores: [], buckets: [] },
  })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      setError(null)

      // Fetch trend data
      const trendResponse = await axios.get(`${API_BASE}/trend/7d`)
      
      // Get latest non-null score
      const scores = trendResponse.data.scores
      const buckets = trendResponse.data.buckets
      let latestScore = null
      let latestBucket = 'No Data'
      
      for (let i = scores.length - 1; i >= 0; i--) {
        if (scores[i] !== null) {
          latestScore = scores[i]
          latestBucket = buckets[i]
          break
        }
      }

      setData({
        latestScore,
        latestBucket,
        textData: null,
        audioData: null,
        imageData: null,
        trendData: trendResponse.data,
      })
    } catch (err: any) {
      console.error('Error fetching dashboard data:', err)
      setError(err.message || 'Failed to load dashboard data')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="loading">Loading dashboard...</div>
  }

  if (error) {
    return (
      <div className="error">
        <h3>Error Loading Dashboard</h3>
        <p>{error}</p>
        <button onClick={fetchDashboardData}>Retry</button>
      </div>
    )
  }

  return (
    <div>
      <div className="card">
        <h2> Today's Mental Health Assessment</h2>
        
        {data.latestScore !== null ? (
          <RiskGauge score={data.latestScore} bucket={data.latestBucket} />
        ) : (
          <div style={styles.noData}>
            <p>No assessment data available yet.</p>
            <p>Start by adding a new entry (text, audio, or image).</p>
          </div>
        )}
      </div>

      <div className="card">
        <h2>📈 7-Day Trend</h2>
        {data.trendData.scores.some(s => s !== null) ? (
          <TrendChart
            dates={data.trendData.dates}
            scores={data.trendData.scores}
            buckets={data.trendData.buckets}
          />
        ) : (
          <div style={styles.noData}>
            <p>No trend data available. Add daily entries to see your progress.</p>
          </div>
        )}
      </div>

      <div style={styles.modalityGrid}>
        <ModalityCard
          modality="Text"
          score={data.textData?.score || null}
          bucket={data.textData?.bucket || 'No Data'}
          explain={data.textData?.explain}
          icon="📝"
        />
        <ModalityCard
          modality="Audio"
          score={data.audioData?.score || null}
          bucket={data.audioData?.bucket || 'No Data'}
          explain={data.audioData?.explain}
          icon="🎤"
        />
        <ModalityCard
          modality="Image"
          score={data.imageData?.score || null}
          bucket={data.imageData?.bucket || 'No Data'}
          explain={data.imageData?.explain}
          icon="📸"
        />
      </div>

      <div className="card" style={styles.disclaimer}>
        <h3>ℹ️ How to Use This Dashboard</h3>
        <ul style={styles.list}>
          <li>Add daily entries using the <strong>New Entry</strong> page</li>
          <li>Track your mental health trends over time</li>
          <li>Review explanations for each analysis</li>
          <li>This is <strong>not a medical diagnosis</strong> - consult professionals for concerns</li>
          <li>All data is processed locally and can be deleted anytime</li>
        </ul>
      </div>
    </div>
  )
}

const styles = {
  noData: {
    textAlign: 'center' as const,
    padding: '2rem',
    color: '#999',
  },
  modalityGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: '1.5rem',
    marginBottom: '1.5rem',
  },
  disclaimer: {
    background: 'rgba(102, 126, 234, 0.1)',
  },
  list: {
    textAlign: 'left' as const,
    paddingLeft: '1.5rem',
    lineHeight: '1.8',
  },
}

export default Dashboard
