import { useEffect, useState } from 'react'
import axios from 'axios'
import RiskGauge from '../components/RiskGauge'
import FeedbackCard from '../components/FeedbackCard'
import TrendChart from '../components/TrendChart'
import HistoricalChatBot from '../components/HistoricalChatBot'
import analysisIcon from '../public/icons/analysis.png?url'
import audioIcon from '../public/icons/audio-waves.png?url'
import cameraIcon from '../public/icons/camera.png?url'
import { useAuth } from '../context/AuthContext'

const API_BASE = 'http://localhost:8000'

interface Session {
  _id: string
  date: string
  text_analysis?: any
  audio_analysis?: any
  image_analysis?: any
  fusion_result?: any
  created_at: string
  updated_at: string
}

interface DashboardData {
  latestScore: number | null
  latestBucket: string
  latestSession: Session | null
  sessions: Session[]
  trendData: {
    dates: string[]
    scores: (number | null)[]
    buckets: string[]
  }
}

function Dashboard() {
  const { token } = useAuth()
  const [data, setData] = useState<DashboardData>({
    latestScore: null,
    latestBucket: 'No Data',
    latestSession: null,
    sessions: [],
    trendData: { dates: [], scores: [], buckets: [] },
  })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    console.log('🎯 Dashboard useEffect triggered, token:', token ? 'exists' : 'missing')
    if (token) {
      fetchDashboardData()
    } else {
      console.warn('⚠️ No token available, skipping data fetch')
      setLoading(false)
    }
  }, [token])

  const fetchDashboardData = async () => {
    console.log('🔄 Dashboard: Starting to fetch data...')
    console.log('Token exists:', !!token)
    
    if (!token) {
      console.error('❌ No token available!')
      setError('Authentication required. Please log in again.')
      setLoading(false)
      return
    }

    try {
      setLoading(true)
      setError(null)

      // Fetch user sessions from MongoDB (last 30 days)
      console.log('📡 Calling API:', `${API_BASE}/sessions/my-sessions`)
      const sessionsResponse = await axios.get(`${API_BASE}/sessions/my-sessions`, {
        headers: {
          'Authorization': `Bearer ${token}`
        },
        params: {
          limit: 30
        }
      })

      const sessions: Session[] = sessionsResponse.data.sessions || []
      console.log('✅ Fetched sessions from MongoDB:', sessions)
      console.log('Total sessions:', sessions.length)

      // Get today's session (latest)
      const today = new Date().toISOString().split('T')[0]
      const latestSession = sessions.find(s => s.date === today) || sessions[0] || null
      console.log('Latest session:', latestSession)

      // Calculate latest score from fusion or individual modalities
      let latestScore = null
      let latestBucket = 'No Data'

      if (latestSession) {
        if (latestSession.fusion_result?.final_score !== undefined) {
          latestScore = latestSession.fusion_result.final_score
          latestBucket = latestSession.fusion_result.final_bucket || 'No Data'
        } else if (latestSession.text_analysis?.score !== undefined) {
          latestScore = latestSession.text_analysis.score
          latestBucket = latestSession.text_analysis.bucket || 'No Data'
        } else if (latestSession.audio_analysis?.score !== undefined) {
          latestScore = latestSession.audio_analysis.score
          latestBucket = latestSession.audio_analysis.bucket || 'No Data'
        } else if (latestSession.image_analysis?.score !== undefined) {
          latestScore = latestSession.image_analysis.score
          latestBucket = latestSession.image_analysis.bucket || 'No Data'
        }
      }

      // Build trend data from sessions (last 7 days)
      const last7Days = Array.from({ length: 7 }, (_, i) => {
        const d = new Date()
        d.setDate(d.getDate() - (6 - i))
        return d.toISOString().split('T')[0]
      })

      const trendScores = last7Days.map(date => {
        const session = sessions.find(s => s.date === date)
        if (!session) return null
        return session.fusion_result?.final_score 
          || session.text_analysis?.score 
          || session.audio_analysis?.score 
          || session.image_analysis?.score 
          || null
      })

      const trendBuckets = last7Days.map(date => {
        const session = sessions.find(s => s.date === date)
        if (!session) return 'No Data'
        return session.fusion_result?.final_bucket 
          || session.text_analysis?.bucket 
          || session.audio_analysis?.bucket 
          || session.image_analysis?.bucket 
          || 'No Data'
      })

      console.log('📊 Trend data:', {
        dates: last7Days,
        scores: trendScores,
        buckets: trendBuckets
      })

      setData({
        latestScore,
        latestBucket,
        latestSession,
        sessions,
        trendData: {
          dates: last7Days,
          scores: trendScores,
          buckets: trendBuckets
        },
      })
      
      console.log('✅ Dashboard data loaded successfully!')
    } catch (err: any) {
      console.error('❌ Error fetching dashboard data:', err)
      console.error('Error details:', {
        status: err.response?.status,
        statusText: err.response?.statusText,
        data: err.response?.data,
        message: err.message
      })
      setError(err.response?.data?.detail || err.message || 'Failed to load dashboard data')
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
        <h2 style={styles.headerWithIcon}>
          <img src={analysisIcon} alt="Analysis" style={styles.icon} />
          Today's Mental Health Assessment
        </h2>
        
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
        <h2>📊 7-Day Mental Health Trend</h2>
        <p style={{fontSize: '0.9rem', color: '#666', marginTop: '0.5rem'}}>Track your mental health indicators over the past week.</p>
        {data.trendData.scores.some(s => s !== null) ? (
          <TrendChart
            dates={data.trendData.dates}
            scores={data.trendData.scores}
            buckets={data.trendData.buckets}
          />
        ) : (
          <div style={styles.noData}>
            <p>📊 No trend data available yet.</p>
            <p>Start adding daily entries to track your mental health over time.</p>
          </div>
        )}
      </div>

      {/* Display latest session analysis with LLM feedback */}
      {data.sessions.length > 0 && (
        <div className="card">
          <h2 style={styles.headerWithIcon}>
            <img src={analysisIcon} alt="Analysis" style={styles.icon} />
            Recent Assessments
          </h2>
          <p style={{fontSize: '0.9rem', color: '#666', marginBottom: '1rem'}}>
            Your latest mental health check-ins with AI insights
          </p>
        </div>
      )}

      {data.latestSession && (
        <>
          {data.latestSession.text_analysis && data.latestSession.text_analysis.llm_feedback && (
            <div className="card">
              <h3 style={styles.modalityTitle}>
                <img src={analysisIcon} alt="Text" style={styles.modalityIcon} />
                Text Analysis - {data.latestSession.date}
              </h3>
              <FeedbackCard 
                feedback={data.latestSession.text_analysis.llm_feedback} 
                type="text" 
              />
            </div>
          )}

          {data.latestSession.audio_analysis && data.latestSession.audio_analysis.llm_feedback && (
            <div className="card">
              <h3 style={styles.modalityTitle}>
                <img src={audioIcon} alt="Audio" style={styles.modalityIcon} />
                Voice Analysis - {data.latestSession.date}
              </h3>
              <FeedbackCard 
                feedback={data.latestSession.audio_analysis.llm_feedback} 
                type="audio" 
              />
            </div>
          )}

          {data.latestSession.image_analysis && data.latestSession.image_analysis.llm_feedback && (
            <div className="card">
              <h3 style={styles.modalityTitle}>
                <img src={cameraIcon} alt="Image" style={styles.modalityIcon} />
                Image Analysis - {data.latestSession.date}
              </h3>
              <FeedbackCard 
                feedback={data.latestSession.image_analysis.llm_feedback} 
                type="image" 
              />
            </div>
          )}
        </>
      )}

      {/* Historical ChatBot for tracking trends over time */}
      <HistoricalChatBot />

      <div className="card" style={styles.disclaimer}>
        {/* <h3>ℹ️ How to Use This Dashboard</h3>
        <ul style={styles.list}>
          <li>Add daily entries using the <strong>New Entry</strong> page</li>
          <li>Track your mental health trends over time</li>
          <li>Review explanations for each analysis</li>
          <li>This is <strong>not a medical diagnosis</strong> - consult professionals for concerns</li>
          <li>All data is processed locally and can be deleted anytime</li>
        </ul> */}
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
  headerWithIcon: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
  },
  icon: {
    width: '50px',
    height: '50px',
    objectFit: 'contain' as const,
  },
  modalityTitle: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    color: '#235284',
    fontSize: '1.2rem',
    fontWeight: 'bold' as const,
    marginBottom: '1rem',
  },
  modalityIcon: {
    width: '24px',
    height: '24px',
    objectFit: 'contain' as const,
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
