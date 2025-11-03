import { useState, useRef, useEffect } from 'react'
import axios from 'axios'
import { useAuth } from '../context/AuthContext'
import gymIcon from '../public/icons/gym.png?url'
import './ChatBot.css'

const API_BASE = 'http://localhost:8000'

interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: string
}

interface ChatBotProps {
  sessionDate: string
  sessionContext?: {
    textResult?: any
    audioResult?: any
    imageResult?: any
  }
}

function ChatBot({ sessionDate, sessionContext }: ChatBotProps) {
  const { token } = useAuth()
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
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
      const hasContext = sessionContext && (
        sessionContext.textResult || 
        sessionContext.audioResult || 
        sessionContext.imageResult
      )

      const welcomeMsg: Message = {
        role: 'assistant',
        content: hasContext 
          ? "Hey! I saw your check-in results. Want to talk about anything?"
          : "Hi there! Complete a check-in above and I'll be here to chat about it with you.",
        timestamp: new Date().toISOString()
      }

      setMessages([welcomeMsg])
    }
  }, [isOpen, sessionContext])

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
        `${API_BASE}/sessions/chat`,
        {
          session_date: sessionDate,
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

      setMessages(prev => [...prev, assistantMessage])
    } catch (error: any) {
      console.error('Chat error:', error)
      const errorMessage: Message = {
        role: 'assistant',
        content: "Oops, something went wrong on my end. Mind trying that again?",
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
      {/* Floating Chat Button */}
      <button
        className="chat-button"
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Open chat assistant"
      >
        <img src={gymIcon} alt="Chat Assistant" className="chat-button-icon" />
        {!isOpen && <span className="chat-button-badge">AI</span>}
      </button>

      {/* Chat Panel */}
      {isOpen && (
        <div className="chat-panel">
          {/* Header */}
          <div className="chat-header">
            <div className="chat-header-content">
              <img src={gymIcon} alt="Assistant" className="chat-header-icon" />
              <div>
                <h3>Chat with me</h3>
                <p>I'm here for you</p>
              </div>
            </div>
            <button 
              className="chat-close-btn"
              onClick={() => setIsOpen(false)}
              aria-label="Close chat"
            >
              ×
            </button>
          </div>

          {/* Messages */}
          <div className="chat-messages">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`chat-message ${msg.role === 'user' ? 'user-message' : 'assistant-message'}`}
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
              <div className="chat-message assistant-message">
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
          <div className="chat-input-container">
            <textarea
              className="chat-input"
              placeholder="Type your message..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              rows={1}
              disabled={isLoading}
            />
            <button
              className="chat-send-btn"
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

export default ChatBot
