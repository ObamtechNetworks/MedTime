import React, { createContext, useContext, useState, useEffect } from 'react'

// Create the AuthContext
const AuthContext = createContext()

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulate an async authentication check
    const checkAuth = async () => {
      const token = localStorage.getItem('accessToken')
      if (token) {
        setIsAuthenticated(true)
      } else {
        setIsAuthenticated(false)
      }
      setLoading(false)
    }

    checkAuth()
  }, [])

  return (
    <AuthContext.Provider value={{ isAuthenticated, setIsAuthenticated, loading }}> {/* Pass setIsAuthenticated */}
      {children}
    </AuthContext.Provider>
  )
}

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext)
  
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  
  return context
}
