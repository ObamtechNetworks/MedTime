import React, { Suspense, useEffect } from 'react'
import { HashRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useSelector } from 'react-redux'
import { CSpinner, useColorModes } from '@coreui/react'
import './scss/style.scss'
import PrivateRoute from './PrivateRoute' // Import the PrivateRoute component

// Containers
const DefaultLayout = React.lazy(() => import('./layout/DefaultLayout'))

// Pages
const Login = React.lazy(() => import('./views/pages/login/Login'))
const Register = React.lazy(() => import('./views/pages/register/Register'))
const Page404 = React.lazy(() => import('./views/pages/page404/Page404'))
const Page500 = React.lazy(() => import('./views/pages/page500/Page500'))
const Dashboard = React.lazy(() => import('./views/dashboard/Dashboard')) // Ensure this is defined
const Profile = React.lazy(() => import('./views/pages/profile/Profile'))
const Settings = React.lazy(() => import('./views/pages/settings/Settings'))
const Schedules = React.lazy(() => import('./views/pages/schedules/Schedule'))

// Landing Page
const LandingPage = React.lazy(() => import('./LandingPage/containers/App'))

const App = () => {
  const { isColorModeSet, setColorMode } = useColorModes('coreui-free-react-admin-template-theme')
  const storedTheme = useSelector((state) => state.theme)

  // Check if user is authenticated
  const isAuthenticated = !!localStorage.getItem('accessToken') // Change as per your auth logic

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.href.split('?')[1])
    const theme = urlParams.get('theme') && urlParams.get('theme').match(/^[A-Za-z0-9\s]+/)[0]
    if (theme) {
      setColorMode(theme)
    }

    if (isColorModeSet()) {
      return
    }

    setColorMode(storedTheme)
  }, [isColorModeSet, setColorMode, storedTheme])

  return (
    <HashRouter>
      <Suspense
        fallback={
          <div className="pt-3 text-center">
            <CSpinner color="primary" variant="grow" />
          </div>
        }
      >
        <Routes>
          {/* Root Route Logic */}
          <Route
            path="/"
            element={
              isAuthenticated ? ( // If authenticated, redirect to dashboard
                <Navigate to="/dashboard" replace />
              ) : (
                <LandingPage /> // If not authenticated, show landing page
              )
            }
          />

          {/* Public Routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/404" element={<Page404 />} />
          <Route path="/500" element={<Page500 />} />

          {/* Protected Routes */}
          <Route element={<PrivateRoute />}> {/** routes are protected */}
            <Route element={<DefaultLayout />}> {/** routes within DefaultLayout */}
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/profile" element={<Profile />} />
              <Route path="/settings" element={<Settings />} />
              <Route path="/schedules" element={<Schedules />} />
            </Route>
          </Route>

          {/* Catch-all for undefined routes */}
          <Route path="*" element={<Navigate to="/404" />} />
        </Routes>
      </Suspense>
    </HashRouter>
  )
}

export default App
