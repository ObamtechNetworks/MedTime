import React from 'react'
import { Navigate, Outlet } from 'react-router-dom'

// Higher-Order Component to protect routes
const PrivateRoute = () => {
  const isAuthenticated = !!localStorage.getItem('accessToken') // Change as per your authentication logic

  return isAuthenticated ? <Outlet /> : <Navigate to="/login" />
}

export default PrivateRoute
