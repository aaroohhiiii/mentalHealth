import { useState, useRef, useEffect } from 'react'
import axios from 'axios'
import { useAuth } from '../context/AuthContext'
import chatbotIcon from '../public/icons/chatbot.png?url'
import './HistoricalChatBot.css'

const API_BASE = 'http://localhost:8000'

interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: string
}

function HistoricalChatBot() {
  const { token } = useAuth()
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [sessionsAnalyzed, setSessionsAnalyzed] = useState(0)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    // Add welcome message when chat opens
    if (isOpen && messages.length === 0) {
      const welcomeMsg: Message = {
        role: 'assistant',
        content: "Hey! I've been keeping track of your mental health journey. Want to talk about how things have been going?",
        timestamp: new Date().toISOString()
      }
      setMessages([welcomeMsg])
    }
  }, [isOpen])

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return

    const userMessage: Message = {
      role: 'user',
      content: inputValue.trim(),
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    setIsLoading(true)

    try {
      // Build chat history for API
      const chatHistory = messages.map(msg => ({
        role: msg.role,
        content: msg.content
      }))

      const response = await axios.post(
        `${API_BASE}/sessions/chat/history`,
        {
          message: userMessage.content,
          chat_history: chatHistory
        },
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      )

      const assistantMessage: Message = {
        role: 'assistant',
        content: response.data.message,
        timestamp: new Date().toISOString()
      }

      setSessionsAnalyzed(response.data.sessions_analyzed || 0)
      setMessages(prev => [...prev, assistantMessage])
    } catch (error: any) {
      console.error('Historical chat error:', error)
      const errorMessage: Message = {
        role: 'assistant',
        content: "Sorry, I'm having trouble accessing your history right now. Try again?",
        timestamp: new Date().toISOString()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <>
      {/* Floating Chat Button with Shaded Circle */}
      <button
        className="historical-chat-button"
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Open mental health tracker"
      >
        <div className="historical-chat-button-circle">
          <img src={chatbotIcon} alt="Mental Health Tracker" className="historical-chat-button-icon" />
        </div>
        {sessionsAnalyzed > 0 && !isOpen && (
          <span className="historical-chat-badge">{sessionsAnalyzed}</span>
        )}
      </button>

      {/* Chat Panel */}
      {isOpen && (
        <div className="historical-chat-panel">
          {/* Header */}
          <div className="historical-chat-header">
            <div className="historical-chat-header-content">
              <div className="historical-chat-header-icon-wrapper">
                <img src={chatbotIcon} alt="Tracker" className="historical-chat-header-icon" />
              </div>
              <div>
                <h3>Your Mental Health Tracker</h3>
                <p>{sessionsAnalyzed > 0 ? `Tracking ${sessionsAnalyzed} sessions` : 'Let\'s talk'}</p>
              </div>
            </div>
            <button 
              className="historical-chat-close-btn"
              onClick={() => setIsOpen(false)}
              aria-label="Close tracker"
            >
              ×
            </button>
          </div>

          {/* Messages */}
          <div className="historical-chat-messages">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`historical-chat-message ${msg.role === 'user' ? 'user-message' : 'assistant-message'}`}
              >
                <div className="message-content">
                  {msg.content}
                </div>
                <div className="message-timestamp">
                  {new Date(msg.timestamp).toLocaleTimeString([], { 
                    hour: '2-digit', 
                    minute: '2-digit' 
                  })}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="historical-chat-message assistant-message">
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="historical-chat-input-container">
            <textarea
              className="historical-chat-input"
              placeholder="Ask about your mental health trends..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              rows={1}
              disabled={isLoading}
            />
            <button
              className="historical-chat-send-btn"
              onClick={handleSendMessage}
              disabled={!inputValue.trim() || isLoading}
              aria-label="Send message"
            >
              <svg 
                width="20" 
                height="20" 
                viewBox="0 0 24 24" 
                fill="none" 
                stroke="currentColor" 
                strokeWidth="2"
              >
                <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" />
              </svg>
            </button>
          </div>
        </div>
      )}
    </>
  )
}

export default HistoricalChatBot
