import React from 'react'

interface RiskGaugeProps {
  score: number // 0-1
  bucket: string // 'Low', 'Moderate', 'High'
}

const RiskGauge: React.FC<RiskGaugeProps> = ({ score, bucket }) => {
  const percentage = Math.round(score * 100)
  
  // Determine color based on bucket
  let color = '#10b981' // green
  let bgClass = 'risk-low'
  
  if (bucket === 'Moderate') {
    color = '#f59e0b' // amber
    bgClass = 'risk-moderate'
  } else if (bucket === 'High') {
    color = '#ef4444' // red
    bgClass = 'risk-high'
  }
  
  return (
    <div style={styles.container}>
      <div style={styles.gaugeWrapper}>
        <svg width="200" height="120" viewBox="0 0 200 120">
          {/* Background arc */}
          <path
            d="M 20 100 A 80 80 0 0 1 180 100"
            fill="none"
            stroke="#e5e7eb"
            strokeWidth="20"
            strokeLinecap="round"
          />
          {/* Colored arc */}
          <path
            d="M 20 100 A 80 80 0 0 1 180 100"
            fill="none"
            stroke={color}
            strokeWidth="20"
            strokeLinecap="round"
            strokeDasharray={`${percentage * 2.51} 251`}
            style={{ transition: 'stroke-dasharray 0.5s ease' }}
          />
          {/* Center text */}
          <text
            x="100"
            y="85"
            textAnchor="middle"
            fontSize="32"
            fontWeight="bold"
            fill={color}
          >
            {percentage}%
          </text>
        </svg>
      </div>
      
      <div style={styles.labelContainer}>
        <div className={bgClass} style={styles.label}>
          <strong>{bucket} Risk</strong>
        </div>
        <p style={styles.description}>
          {bucket === 'Low' && 'Your indicators suggest good mental wellbeing.'}
          {bucket === 'Moderate' && 'Some signs of stress detected. Monitor closely.'}
          {bucket === 'High' && 'Multiple concerning indicators detected.'}
        </p>
      </div>
    </div>
  )
}

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column' as const,
    alignItems: 'center',
    padding: '1rem',
  },
  gaugeWrapper: {
    marginBottom: '1rem',
  },
  labelContainer: {
    textAlign: 'center' as const,
  },
  label: {
    display: 'inline-block',
    padding: '0.5rem 1.5rem',
    borderRadius: '20px',
    fontSize: '1.2rem',
    marginBottom: '0.5rem',
  },
  description: {
    fontSize: '0.9rem',
    color: '#666',
    margin: '0.5rem 0',
  },
}

export default RiskGauge
