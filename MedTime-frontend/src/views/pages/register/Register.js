import React, { useState } from 'react'
import {
  CButton,
  CCard,
  CCardBody,
  CCol,
  CContainer,
  CForm,
  CFormInput,
  CInputGroup,
  CInputGroupText,
  CRow,
  CModal,
  CModalHeader,
  CModalBody,
  CModalFooter,
  CSpinner
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import { useNavigate } from 'react-router-dom'
import { cilLockLocked } from '@coreui/icons'
import { toast, ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import axios from 'axios'
import './Register.scss' // Import the SCSS file

const Register = () => {
  const navigate = useNavigate()

  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    confirm_password: '',
  })

  const [otp, setOtp] = useState('')
  const [showOtpModal, setShowOtpModal] = useState(false)
  const [resendDisabled, setResendDisabled] = useState(true)
  const [resendCountdown, setResendCountdown] = useState(300) // 5 minutes
  const [loading, setLoading] = useState(false) // Loader for form submission
  const [otpLoading, setOtpLoading] = useState(false) // Loader for OTP verification

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true) // Start the loader


    const { first_name, last_name, email, password, confirm_password } = formData

    // Validation: Check if all fields are filled
    if (!first_name || !last_name || !email || !password || !confirm_password) {
      toast.error('All fields are required!')
      setLoading(false)
      return
    }

    // Validation: Check if passwords match
    if (formData.confirm_password !== formData.password) {
      toast.error("Passwords don't match!")
      setLoading(false)
      return
    }

    console.log('Register URL:', import.meta.env.VITE_REGISTER_URL)

    try {
      // Attempt to register the user
      const response = await axios.post(import.meta.env.VITE_REGISTER_URL, formData)
      console.log(response.data)
      toast.success('Registration successful! Please check your email for the OTP.')
      setShowOtpModal(true) // Open OTP modal
      startResendTimer() // Start the OTP resend timer
    } catch (error) {
      console.log(error)

      // Handle specific error messages from the backend
      if (error.response && error.response.status === 400) {
        const errorData = error.response.data

        // If the email already exists, trigger the OTP modal for verification
        if (
          errorData.email &&
          errorData.email[0] === 'user with this Email Address already exists.'
        ) {
          toast.info('Email already exists. Please verify your email with the OTP.')
          setShowOtpModal(true) // Show OTP modal if email exists
          handleResendOtp() // Automatically resend OTP
        } else if (errorData.email) {
          // Handle specific email validation error
          toast.error(errorData.email[0])
        } else {
          // Handle other validation errors
          toast.error('Registration failed. Please check your inputs and try again.')
        }
      } else {
        // Default error handling
        toast.error('Registration failed. Please try again.')
      }
    }finally {
      setLoading(false) // Stop the loader
    }
  }

  // Handle OTP submit
  const handleOtpSubmit = async () => {
    setOtpLoading(true)
    
    try {
    
      // Clean the OTP input by trimming spaces and removing any non-numeric characters
      const cleanedOtp = otp.replace(/\D/g, '').trim();
      
      const response = await axios.post(import.meta.env.VITE_VERIFY_EMAIL_URL, {
        email: formData.email,
        otp: cleanedOtp, // Use cleaned OTP
      }, { headers: { 'Content-Type': 'application/json' } }
      )
      console.log('OTP Verification Response:', response.data) // Log the response
      toast.success('OTP Verified! Redirecting to login...')
      setTimeout(() => {
        navigate('/login')
      }, 2000)
    } catch (error) {
      console.log('OTP Error Response:', error.response) // Log the error response
      console.log('Error Details:', error) // Log the full error
      toast.error('Invalid OTP or OTP has expired!')
    } finally {
      setOtpLoading(false)
    }
}

  // Resend OTP
  const handleResendOtp = async () => {
    try {
      await axios.post(import.meta.env.VITE_RESEND_OTP_URL, { email: formData.email })
      toast.success('OTP Resent! Please check your email.')
      startResendTimer() // Start timer again
    } catch (error) {
      toast.error('Failed to resend OTP. Please try again later.')
    }
  }

  // Start countdown for resend OTP
  const startResendTimer = () => {
    setResendDisabled(true)
    setResendCountdown(300) // 5 minutes

    const interval = setInterval(() => {
      setResendCountdown((prev) => {
        if (prev === 1) {
          clearInterval(interval)
          setResendDisabled(false)
        }
        return prev - 1
      })
    }, 1000)
  }

  return (
    <div className="register-container">
      <CContainer>
        <ToastContainer />
        <CRow className="justify-content-center">
          <CCol md={9} lg={7} xl={6}>
            <CCard className="mx-4">
              <CCardBody className="p-4 register-content">
                <div className="logo">
                </div>
                <CForm onSubmit={handleSubmit}>
                  <h1>Register</h1>
                  <p className="text-body-secondary">Create your account</p>

                  <CInputGroup className="mb-3">
                    <CInputGroupText>First Name</CInputGroupText>
                    <CFormInput
                      name="first_name"
                      placeholder="First Name"
                      value={formData.first_name}
                      onChange={handleChange}
                      autoComplete="given-name"
                    />
                  </CInputGroup>

                  <CInputGroup className="mb-3">
                    <CInputGroupText>Last Name</CInputGroupText>
                    <CFormInput
                      name="last_name"
                      placeholder="Last Name"
                      value={formData.last_name}
                      onChange={handleChange}
                      autoComplete="family-name"
                    />
                  </CInputGroup>

                  <CInputGroup className="mb-3">
                    <CInputGroupText>@</CInputGroupText>
                    <CFormInput
                      name="email"
                      type="email"
                      placeholder="Email"
                      value={formData.email}
                      onChange={handleChange}
                      autoComplete="email"
                    />
                  </CInputGroup>

                  <CInputGroup className="mb-3">
                    <CInputGroupText>
                      <CIcon icon={cilLockLocked} />
                    </CInputGroupText>
                    <CFormInput
                      name="password"
                      type="password"
                      placeholder="Password"
                      value={formData.password}
                      onChange={handleChange}
                      autoComplete="new-password"
                    />
                  </CInputGroup>

                  <CInputGroup className="mb-4">
                    <CInputGroupText>
                      <CIcon icon={cilLockLocked} />
                    </CInputGroupText>
                    <CFormInput
                      name="confirm_password"
                      type="password"
                      placeholder="Repeat password"
                      value={formData.confirm_password}
                      onChange={handleChange}
                      autoComplete="new-password"
                    />
                  </CInputGroup>

                  <div className="d-grid">
                    <CButton className="register-button" type="submit" disabled={loading}>
                      {loading ? <CSpinner size="sm" /> : 'Create Account'}
                    </CButton>
                  </div>
                </CForm>

                {/* OTP Modal */}
                <CModal visible={showOtpModal} backdrop="static" keyboard={false}>
                  <CModalHeader>Enter OTP</CModalHeader>
                  <CModalBody>
                    <CInputGroup className="mb-3">
                      <CInputGroupText>OTP</CInputGroupText>
                      <CFormInput
                        value={otp}
                        onChange={(e) => setOtp(e.target.value)}
                        placeholder="Enter OTP"
                      />
                    </CInputGroup>
                    <CButton color="primary" onClick={handleOtpSubmit} disabled={otpLoading}>
                      {otpLoading ? <CSpinner size="sm" /> : 'Verify OTP'}
                    </CButton>
                  {/* Add Resend OTP button */}
                  <div className="mt-3">
                    <CButton
                      color="link"
                      onClick={handleResendOtp}
                      disabled={resendDisabled}
                    >
                      Resend OTP {resendDisabled && `(${resendCountdown}s)`}
                    </CButton>
                  </div>
                </CModalBody>
                <CModalFooter>
                  <CButton color="secondary" onClick={() => setShowOtpModal(false)}>
                    Close
                  </CButton>
                </CModalFooter>
              </CModal>
              </CCardBody>
            </CCard>
          </CCol>
        </CRow>
      </CContainer>
    </div>
  )
}

export default Register
