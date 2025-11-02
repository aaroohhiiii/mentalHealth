import React from 'react'

interface ModalityCardProps {
  modality: string
  score: number | null
  bucket: string
  explain: any
  icon: string
}

const ModalityCard: React.FC<ModalityCardProps> = ({ modality, score, bucket, explain, icon }) => {
  if (score === null) {
    return (
      <div className="card" style={styles.card}>
        <h3>{icon} {modality}</h3>
        <p style={styles.noData}>No data available</p>
      </div>
    )
  }

  const percentage = Math.round(score * 100)
  let bgClass = 'risk-low'
  if (bucket === 'Moderate') bgClass = 'risk-moderate'
  if (bucket === 'High') bgClass = 'risk-high'

  return (
    <div className="card" style={styles.card}>
      <div style={styles.header}>
        <h3>{icon} {modality}</h3>
        <div className={bgClass} style={styles.badge}>
          {percentage}% - {bucket}
        </div>
      </div>

      <div style={styles.content}>
        {modality === 'Text' && explain && (
          <>
            <p><strong>Sentiment:</strong> {explain.sentiment}</p>
            {explain.tokens && explain.tokens.length > 0 && (
              <div style={styles.tokens}>
                <strong>Key Indicators:</strong>
                <div style={styles.tokenList}>
                  {explain.tokens.map((token: any, idx: number) => (
                    <span
                      key={idx}
                      style={{
                        ...styles.token,
                        backgroundColor: token.type === 'negative' ? '#fee' : '#efe',
                        border: token.type === 'negative' ? '1px solid #f88' : '1px solid #8f8',
                      }}
                    >
                      {token.word}
                    </span>
                  ))}
                </div>
              </div>
            )}
            {explain.dominant_themes && explain.dominant_themes.length > 0 && (
              <p><strong>Themes:</strong> {explain.dominant_themes.join(', ')}</p>
            )}
          </>
        )}

        {modality === 'Audio' && explain && (
          <>
            <p><strong>Dominant Emotion:</strong> {explain.dominant_emotion}</p>
            {explain.emotion_distribution && (
              <div style={styles.emotions}>
                <strong>Emotion Distribution:</strong>
                {Object.entries(explain.emotion_distribution).map(([emotion, prob]: [string, any]) => (
                  <div key={emotion} style={styles.emotionBar}>
                    <span style={styles.emotionLabel}>{emotion}</span>
                    <div style={styles.barContainer}>
                      <div
                        style={{
                          ...styles.bar,
                          width: `${prob * 100}%`,
                        }}
                      />
                    </div>
                    <span style={styles.emotionValue}>{Math.round(prob * 100)}%</span>
                  </div>
                ))}
              </div>
            )}
          </>
        )}

        {modality === 'Image' && explain && (
          <>
            <p><strong>Dominant Emotion:</strong> {explain.dominant_emotion}</p>
            <p><strong>Face Detected:</strong> {explain.face_detected ? 'Yes' : 'No'}</p>
            {explain.all_emotions && (
              <div style={styles.emotions}>
                <strong>Emotion Analysis:</strong>
                {Object.entries(explain.all_emotions)
                  .sort(([, a]: any, [, b]: any) => b - a)
                  .slice(0, 5)
                  .map(([emotion, prob]: [string, any]) => (
                    <div key={emotion} style={styles.emotionBar}>
                      <span style={styles.emotionLabel}>{emotion}</span>
                      <div style={styles.barContainer}>
                        <div
                          style={{
                            ...styles.bar,
                            width: `${prob * 100}%`,
                          }}
                        />
                      </div>
                      <span style={styles.emotionValue}>{Math.round(prob * 100)}%</span>
                    </div>
                  ))}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}

const styles = {
  card: {
    minHeight: '200px',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '1rem',
  },
  badge: {
    padding: '0.5rem 1rem',
    borderRadius: '20px',
    fontSize: '0.9rem',
    fontWeight: 'bold' as const,
  },
  content: {
    fontSize: '0.95rem',
  },
  noData: {
    color: '#999',
    fontStyle: 'italic' as const,
    textAlign: 'center' as const,
    padding: '2rem',
  },
  tokens: {
    marginTop: '0.75rem',
  },
  tokenList: {
    display: 'flex',
    flexWrap: 'wrap' as const,
    gap: '0.5rem',
    marginTop: '0.5rem',
  },
  token: {
    padding: '0.25rem 0.75rem',
    borderRadius: '12px',
    fontSize: '0.85rem',
  },
  emotions: {
    marginTop: '0.75rem',
  },
  emotionBar: {
    display: 'flex',
    alignItems: 'center',
    marginTop: '0.5rem',
    gap: '0.5rem',
  },
  emotionLabel: {
    width: '80px',
    fontSize: '0.85rem',
    textTransform: 'capitalize' as const,
  },
  barContainer: {
    flex: 1,
    height: '20px',
    background: '#e5e7eb',
    borderRadius: '10px',
    overflow: 'hidden' as const,
  },
  bar: {
    height: '100%',
    background: 'linear-gradient(90deg, #667eea, #764ba2)',
    transition: 'width 0.3s ease',
  },
  emotionValue: {
    width: '50px',
    textAlign: 'right' as const,
    fontSize: '0.85rem',
    fontWeight: 'bold' as const,
  },
}

export default ModalityCard
