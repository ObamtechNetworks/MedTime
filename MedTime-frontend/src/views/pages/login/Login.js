import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import {
  CButton,
  CCard,
  CCardBody,
  CCardGroup,
  CCol,
  CContainer,
  CForm,
  CFormInput,
  CInputGroup,
  CInputGroupText,
  CRow,
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import { cilLockLocked, cilUser } from '@coreui/icons'
import axios from 'axios'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import { toast } from 'react-toastify'
import './login.scss' // Importing the SASS file

// Import your logo image
import Logo from '../../../assets/images/MedTime-logo.jpeg'; // Update the path accordingly

const Login = () => {
  const [formData, setFormData] = useState({ email: '', password: '' })
  const navigate = useNavigate()

  const handleChange = (e) => {

    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!formData.email || !formData.password) {
      toast.error('Both email and password are required!')
      return
    }

    try {
      console.log(import.meta.env.VITE_LOGIN_URL) // Check if the URL is correctly loaded

      const response = await axios.post(import.meta.env.VITE_LOGIN_URL, formData)
      const { access_token, refresh_token } = response.data
      console.log(response.data)

      localStorage.setItem('accessToken', access_token)
      localStorage.setItem('refreshToken', refresh_token)

      toast.success('Login successful! Redirecting...')
      navigate('/dashboard') // Redirect to dashboard after successful login
    } catch (error) {
      console.log(error)

      // Handle specific error scenarios
      if (axios.isAxiosError(error)) {
        if (error.response) {
          // The request was made and the server responded with a status code
          if (error.response.status === 401) {
            // Invalid credentials
            toast.error('Invalid email or password. Please try again.')
          } else if (error.response.status === 403) {
            // Forbidden (e.g., account not activated)
            toast.error('Your account is not active. Please check your email.')
          } else if (error.response.status === 500) {
            // Server error
            toast.error('Server error. Please try again later.')
          } else {
            // Other server error
            toast.error('An error occurred. Please try again.')
          }
        } else if (error.request) {
          // The request was made but no response was received
          toast.error('Network error. Please check your connection and try again.')
        } else {
          // Something happened in setting up the request
          toast.error('An unexpected error occurred. Please try again.')
        }
      } else {
        // General error handling
        toast.error('An unexpected error occurred. Please try again.')
      }
    }
  }

  return (
    <div className="login-page">
      <CContainer>
        <CRow className="justify-content-center">
          <CCol md={8}>
            <CCardGroup>
              <CCard className="p-4">
                <CCardBody className="text-center">
                  {/* Logo */}
                  <Link to="/">
                    <img src={Logo} alt="MedTime Logo" className="logo" />
                  </Link>

                  <CForm onSubmit={handleSubmit} className="mt-4">
                    <h1>Login</h1>
                    <p className="text-body-secondary">Sign In to your account</p>
                    <CInputGroup className="mb-3">
                      <CInputGroupText>
                        <CIcon icon={cilUser} />
                      </CInputGroupText>
                      <CFormInput
                        name="email"
                        placeholder="Email"
                        autoComplete="email"
                        value={formData.email}
                        onChange={handleChange}
                      />
                    </CInputGroup>
                    <CInputGroup className="mb-4">
                      <CInputGroupText>
                        <CIcon icon={cilLockLocked} />
                      </CInputGroupText>
                      <CFormInput
                        type="password"
                        name="password"
                        placeholder="Password"
                        autoComplete="current-password"
                        value={formData.password}
                        onChange={handleChange}
                      />
                    </CInputGroup>
                    <CRow>
                      <CCol xs={6}>
                        <CButton type="submit" color="primary" className="px-4">
                          Login
                        </CButton>
                      </CCol>
                      <CCol xs={6} className="text-right">
                        <CButton color="link" className="px-0">
                          Forgot password?
                        </CButton>
                      </CCol>
                    </CRow>
                  </CForm>
                </CCardBody>
              </CCard>
              <CCard className="text-white bg-primary py-5" style={{ width: '44%' }}>
                <CCardBody className="text-center">
                  <div>
                    <h2>Sign up</h2>
                    <p>Don't have an account? Sign up to get started!</p>
                    <Link to="/register">
                      <CButton color="light" className="mt-3" active tabIndex={-1}>
                        Register Now!
                      </CButton>
                    </Link>
                  </div>
                </CCardBody>
              </CCard>
            </CCardGroup>
          </CCol>
        </CRow>
        <ToastContainer />
      </CContainer>
    </div>
  )
}

export default Login
