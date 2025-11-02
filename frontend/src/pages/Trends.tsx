import { useEffect, useState } from 'react'
import axios from 'axios'
import TrendChart from '../components/TrendChart'
import analysisIcon from '../public/icons/analysis.png?url'

const API_BASE = 'http://localhost:8000'

function Trends() {
  const [trendData, setTrendData] = useState<{
    dates: string[]
    scores: (number | null)[]
    buckets: string[]
  }>({ dates: [], scores: [], buckets: [] })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchTrendData()
  }, [])

  const fetchTrendData = async () => {
    try {
      setLoading(true)
      setError(null)

      const response = await axios.get(`${API_BASE}/trend/7d`)
      setTrendData(response.data)
    } catch (err: any) {
      console.error('Error fetching trend data:', err)
      setError(err.message || 'Failed to load trend data')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="loading">Loading trends...</div>
  }

  if (error) {
    return (
      <div className="error">
        <h3>Error Loading Trends</h3>
        <p>{error}</p>
        <button onClick={fetchTrendData}>Retry</button>
      </div>
    )
  }

  const hasData = trendData.scores.some(s => s !== null)

  return (
    <div>
      <div className="card">
        <h2> 7-Day Mental Health Trend</h2>
        <p>Track your mental health indicators over the past week.</p>
      </div>

      <div className="card">
        {hasData ? (
          <>
            <TrendChart
              dates={trendData.dates}
              scores={trendData.scores}
              buckets={trendData.buckets}
            />

            <div style={styles.summary}>
              <h3>Weekly Summary</h3>
              <div style={styles.summaryGrid}>
                {trendData.dates.map((date, index) => {
                  const score = trendData.scores[index]
                  const bucket = trendData.buckets[index]

                  let bgClass = 'risk-low'
                  if (bucket === 'Moderate') bgClass = 'risk-moderate'
                  if (bucket === 'High') bgClass = 'risk-high'

                  return (
                    <div key={date} style={styles.dayCard}>
                      <div style={styles.date}>
                        {new Date(date).toLocaleDateString('en-US', {
                          weekday: 'short',
                          month: 'short',
                          day: 'numeric',
                        })}
                      </div>
                      {score !== null ? (
                        <>
                          <div className={bgClass} style={styles.scoreBadge}>
                            {Math.round(score * 100)}%
                          </div>
                          <div className={bgClass} style={styles.bucketBadge}>
                            {bucket}
                          </div>
                        </>
                      ) : (
                        <div style={styles.noData}>No Data</div>
                      )}
                    </div>
                  )
                })}
              </div>
            </div>
          </>
        ) : (
          <div style={styles.emptyState}>
            <p style={styles.emptyText}>
              <img src={analysisIcon} alt="Analysis" style={styles.emptyIcon} />
              No trend data available yet.
            </p>
            <p>Start adding daily entries to track your mental health over time.</p>
          </div>
        )}
      </div>

      <div className="card" style={styles.insights}>
        <h3>💡 Insights</h3>
        <ul style={styles.list}>
          <li><strong>Consistency:</strong> Add entries daily for accurate trend analysis</li>
          <li><strong>Multi-modal:</strong> Combine text, audio, and images for better insights</li>
          <li><strong>Patterns:</strong> Look for patterns in your risk scores over days/weeks</li>
          <li><strong>Self-care:</strong> Use insights to adjust sleep, exercise, and stress management</li>
          <li><strong>Professional help:</strong> If you see persistent high scores, consider consulting a mental health professional</li>
        </ul>
      </div>
    </div>
  )
}

const styles = {
  summary: {
    marginTop: '2rem',
  },
  summaryGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(120px, 1fr))',
    gap: '1rem',
    marginTop: '1rem',
  },
  dayCard: {
    padding: '1rem',
    border: '2px solid #ddd',
    borderRadius: '8px',
    textAlign: 'center' as const,
    background: '#f9f9f9',
  },
  date: {
    fontSize: '0.85rem',
    fontWeight: 'bold' as const,
    marginBottom: '0.5rem',
    color: '#555',
  },
  scoreBadge: {
    padding: '0.5rem',
    borderRadius: '8px',
    fontSize: '1.2rem',
    fontWeight: 'bold' as const,
    marginBottom: '0.25rem',
  },
  bucketBadge: {
    padding: '0.25rem 0.5rem',
    borderRadius: '12px',
    fontSize: '0.75rem',
    fontWeight: 'bold' as const,
    display: 'inline-block',
    marginTop: '0.25rem',
  },
  noData: {
    color: '#999',
    fontSize: '0.85rem',
    fontStyle: 'italic' as const,
    padding: '0.5rem',
  },
  emptyState: {
    textAlign: 'center' as const,
    padding: '3rem 1rem',
    color: '#999',
  },
  emptyText: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '0.5rem',
  },
  emptyIcon: {
    width: '24px',
    height: '24px',
    objectFit: 'contain' as const,
  },
  insights: {
    background: 'rgba(102, 126, 234, 0.1)',
  },
  list: {
    textAlign: 'left' as const,
    paddingLeft: '1.5rem',
    lineHeight: '1.8',
  },
}

export default Trends
