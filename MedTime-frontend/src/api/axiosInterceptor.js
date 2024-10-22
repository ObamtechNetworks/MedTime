import axios from 'axios';

// Create axios instance
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});

// Interceptor to attach access token to all requests
api.interceptors.request.use((config) => {
  const accessToken = localStorage.getItem('accessToken');
  if (accessToken) {
    config.headers['Authorization'] = `Bearer ${accessToken}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

// Interceptor to handle expired access tokens
api.interceptors.response.use(
  (response) => response, // Allow response to pass through if no error
  async (error) => {
    const originalRequest = error.config;

    if (error.response) {
      const { status } = error.response;

      // Check if the error is due to an expired token and if the request hasn't been retried yet
      if (status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;

        try {
          const refreshToken = localStorage.getItem('refreshToken');

          // If no refresh token is available, force logout
          if (!refreshToken) {
            localStorage.clear();
            window.location.href = '/login'; // Immediately redirect to login
            return Promise.reject(new Error('No refresh token available'));
          }

          // Use refresh token to get a new access token
          const response = await axios.post(import.meta.env.VITE_TOKEN_REFRESH, {
            refresh: refreshToken, // Replace "refresh" if backend expects a different key
          });

          const { access } = response.data; // .access ? or what?

          // Update the access token in localStorage
          localStorage.setItem('accessToken', access);

          // Retry the original request with new access token
          originalRequest.headers['Authorization'] = `Bearer ${access}`;
          return api(originalRequest); // Retry original request with updated access token

        } catch (tokenRefreshError) {
          console.error('Token refresh failed:', tokenRefreshError);
          localStorage.clear();
          window.location.href = '/login'; // Redirect to login if refresh token fails
          return Promise.reject(tokenRefreshError);
        }
      }
    } else {
      console.error('Network error or no response:', error);
      if (!navigator.onLine) {
        alert('No internet connection. Please check your connection and try again.');
      }
    }

    return Promise.reject(error); // Reject other errors
  }
);

export default api;
