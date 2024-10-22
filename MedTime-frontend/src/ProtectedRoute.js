import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from './api/authContext'

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <div>Loading...</div>; // Add a loading indicator if necessary
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />; // render children components
};

export default ProtectedRoute;
