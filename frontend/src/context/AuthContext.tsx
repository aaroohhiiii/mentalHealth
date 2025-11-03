import React, { createContext, useContext, useState, useEffect } from 'react'
import axios from 'axios'

const API_BASE = 'http://127.0.0.1:8000'

interface User {
  username: string
  email: string
}

interface AuthContextType {
  user: User | null
  token: string | null
  login: (username: string, password: string) => Promise<void>
  signup: (username: string, email: string, password: string) => Promise<void>
  logout: () => void
  isLoading: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Check for stored token on mount
    const storedToken = localStorage.getItem('token')
    if (storedToken) {
      setToken(storedToken)
      fetchCurrentUser(storedToken)
    } else {
      setIsLoading(false)
    }
  }, [])

  const fetchCurrentUser = async (authToken: string) => {
    try {
      const response = await axios.get(`${API_BASE}/auth/me`, {
        headers: {
          Authorization: `Bearer ${authToken}`,
        },
      })
      setUser(response.data)
    } catch (error) {
      console.error('Failed to fetch user:', error)
      localStorage.removeItem('token')
      setToken(null)
    } finally {
      setIsLoading(false)
    }
  }

  const login = async (username: string, password: string) => {
    const response = await axios.post(`${API_BASE}/auth/login`, {
      username,
      password,
    })

    const { access_token, user: userData } = response.data
    setToken(access_token)
    setUser(userData)
    localStorage.setItem('token', access_token)
  }

  const signup = async (username: string, email: string, password: string) => {
    const response = await axios.post(`${API_BASE}/auth/signup`, {
      username,
      email,
      password,
    })

    const { access_token, user: userData } = response.data
    setToken(access_token)
    setUser(userData)
    localStorage.setItem('token', access_token)
  }

  const logout = () => {
    setToken(null)
    setUser(null)
    localStorage.removeItem('token')
  }

  return (
    <AuthContext.Provider value={{ user, token, login, signup, logout, isLoading }}>
      {children}
    </AuthContext.Provider>
  )
}
