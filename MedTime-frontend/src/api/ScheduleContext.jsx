import React, { createContext, useState, useContext, useEffect } from 'react';
import api from './axiosInterceptor';
import { useAuth } from './authContext';

// Create the context
const SchedulesContext = createContext();

// Create a provider component
export const SchedulesProvider = ({ children }) => {
  const [schedules, setSchedules] = useState([]); // Initial schedules
  const [loading, setLoading] = useState(true); // Loading state
  const [error, setError] = useState(null); // Error state
  const [hasFetched, setHasFetched] = useState(false); // Track if schedules have been fetched
  const { isAuthenticated } = useAuth(); // Get authentication state

  const fetchSchedules = async () => {
    if (!hasFetched) {
      try {
        setLoading(true);
        const response = await api.get(import.meta.env.VITE_SCHEDULES_URL);
        setSchedules(response.data);
        setHasFetched(true);
      } catch (error) {
        console.error('Error fetching schedules:', error);
        setError('Error fetching schedules');
      } finally {
        setLoading(false);
      }
    }
  };

  useEffect(() => {
    if (isAuthenticated) {
      fetchSchedules();
    } else {
      setLoading(false); // Stop loading if not authenticated
    }
  }, [isAuthenticated]); // Re-run when isAuthenticated changes

  return (
    <SchedulesContext.Provider value={{ schedules, loading, error, fetchSchedules }}>
      {children}
    </SchedulesContext.Provider>
  );
};

// Custom hook to use the schedules context
export const useSchedules = () => useContext(SchedulesContext);
