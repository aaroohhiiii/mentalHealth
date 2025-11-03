import React, { useState } from 'react'
import './FeedbackCard.css'

interface LLMFeedback {
  risk_level?: string
  reasoning?: string
  supportive_message?: string
  key_concerns?: string[]
  key_observations?: string[]
  suggestions?: string[]
  needs_professional_help?: boolean
  needs_attention?: boolean
  professional_help_reason?: string
  interpretation?: string
  concern_level?: string
}

interface FeedbackCardProps {
  feedback: LLMFeedback
  type?: 'text' | 'audio' | 'image'
}

const FeedbackCard: React.FC<FeedbackCardProps> = ({ feedback, type = 'text' }) => {
  const [isExpanded, setIsExpanded] = useState(true)

  // If no feedback or not enhanced, don't render
  if (!feedback || Object.keys(feedback).length === 0) {
    return null
  }

  const riskLevel = feedback.risk_level || feedback.concern_level || 'Low'
  const concerns = feedback.key_concerns || feedback.key_observations || []
  const suggestions = feedback.suggestions || []

  // Color based on risk level - subtle, professional
  const getRiskColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'high':
        return '#ef5350'
      case 'moderate':
        return '#ffa726'
      case 'low':
        return '#66bb6a'
      default:
        return '#6abce2'
    }
  }

  return (
    <div className="feedback-card">
      <div className="feedback-header" onClick={() => setIsExpanded(!isExpanded)}>
        <div className="feedback-title">
          <span className="feedback-icon">&#9432;</span>
          <h4>AI Insights</h4>
        </div>
        <button className="expand-btn" aria-label={isExpanded ? 'Collapse' : 'Expand'}>
          {isExpanded ? '−' : '+'}
        </button>
      </div>

      {isExpanded && (
        <div className="feedback-content">
          {/* Risk Level */}
          <div className="feedback-section">
            <div className="risk-badge" style={{ borderLeft: `4px solid ${getRiskColor(riskLevel)}` }}>
              <span className="risk-label">Risk Level:</span>
              <span className="risk-value" style={{ color: getRiskColor(riskLevel) }}>
                {riskLevel}
              </span>
            </div>
          </div>

          {/* Supportive Message */}
          {feedback.supportive_message && (
            <div className="feedback-section">
              <p className="supportive-text">{feedback.supportive_message}</p>
            </div>
          )}

          {/* Interpretation (for audio/image) */}
          {feedback.interpretation && (
            <div className="feedback-section">
              <p className="interpretation-text">{feedback.interpretation}</p>
            </div>
          )}

          {/* Reasoning */}
          {feedback.reasoning && (
            <div className="feedback-section">
              <h5 className="section-title">Assessment</h5>
              <p className="reasoning-text">{feedback.reasoning}</p>
            </div>
          )}

          {/* Key Concerns/Observations */}
          {concerns.length > 0 && (
            <div className="feedback-section">
              <h5 className="section-title">Key Points to Monitor</h5>
              <ul className="concerns-list">
                {concerns.map((concern, idx) => (
                  <li key={idx}>{concern}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Suggestions */}
          {suggestions.length > 0 && (
            <div className="feedback-section">
              <h5 className="section-title">Recommendations</h5>
              <ul className="suggestions-list">
                {suggestions.map((suggestion, idx) => (
                  <li key={idx}>{suggestion}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Professional Help Alert */}
          {(feedback.needs_professional_help || feedback.needs_attention) && (
            <div className="feedback-section professional-help-alert">
              <p className="alert-text">
                <strong>Note:</strong> Consider speaking with a mental health professional for personalized support.
                {feedback.professional_help_reason && ` ${feedback.professional_help_reason}`}
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default FeedbackCard
