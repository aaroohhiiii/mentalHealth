import React from 'react'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts'

interface TrendChartProps {
  dates: string[]
  scores: (number | null)[]
  buckets: string[]
}

const TrendChart: React.FC<TrendChartProps> = ({ dates, scores, buckets }) => {
  // Transform data for recharts
  const data = dates.map((date, index) => ({
    date: new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    score: scores[index] !== null ? Math.round(scores[index]! * 100) : null,
    bucket: buckets[index],
  }))

  return (
    <div style={styles.container}>
      <h3>7-Day Risk Trend</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis domain={[0, 100]} label={{ value: 'Risk Score (%)', angle: -90, position: 'insideLeft' }} />
          <Tooltip
            content={({ active, payload }) => {
              if (active && payload && payload.length) {
                const data = payload[0].payload
                return (
                  <div style={styles.tooltip}>
                    <p><strong>{data.date}</strong></p>
                    {data.score !== null ? (
                      <>
                        <p>Risk Score: {data.score}%</p>
                        <p>Category: <span className={`risk-${data.bucket.toLowerCase()}`}>{data.bucket}</span></p>
                      </>
                    ) : (
                      <p>No data</p>
                    )}
                  </div>
                )
              }
              return null
            }}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="score"
            stroke="#667eea"
            strokeWidth={3}
            dot={{ fill: '#667eea', r: 5 }}
            activeDot={{ r: 8 }}
            name="Risk Score"
            connectNulls
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

const styles = {
  container: {
    width: '100%',
  },
  tooltip: {
    background: 'white',
    border: '1px solid #ccc',
    borderRadius: '8px',
    padding: '10px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
  },
}

export default TrendChart
