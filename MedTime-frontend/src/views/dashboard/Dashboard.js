import React, { useState, useEffect } from 'react'
import { CRow, CCol, CButton } from '@coreui/react'
import GoalOverview from './GoalOverview'
import NextDose from './NextDose'
import OngoingMedication from './OngoingMedication'
import './Dashboard.scss' // Importing Sass for styling

//  import axios intercpetor
import api from '../../api/axiosInterceptor'

// import medication component
import CreateMedicationForm from '../../api/createMedicationModal'

const Dashboard = () => {
  const [progress, setProgress] = useState(75) // Example percentage
  const [totalDays, setTotalDays] = useState(30) // Example total days
  const [daysRemaining, setDaysRemaining] = useState(7) // Example days remaining
  const [hoursLeft, setHoursLeft] = useState(5) // Example hours till next dose
  const [medications, setMedications] = useState([]) // Medication data

  const [showMedicationForm, setShowMedicationForm] = useState(false) // Track if form is open

  // Check if there are ongoing medications
  const noOngoingMedications = medications.length === 0

  // Function to handle schedule creation click
  const handleCreateMedicationSchedule = () => {
    setShowMedicationForm(true) // Show the form when button is clicked
  }

  // Function to handle canceling the form creation
  const handleCancelMedicationForm = () => {
    setShowMedicationForm(false) // Hide the form if the user cancels
  }

  useEffect(() => {
    // API call to fetch progress, medications, etc.
  }, [])

  return (
    <div className="dashboard-container">
      <CRow className="g-4">
        <CCol md={6}>
          <GoalOverview
            progressPercentage={progress}
            totalDays={totalDays}
            daysRemaining={daysRemaining}
          />
        </CCol>
        <CCol md={6}>
          <NextDose hoursLeft={hoursLeft} />
        </CCol>

        <CCol xs={12}>
          {/* Render Button or Form Based on State */}
          {!showMedicationForm ? (
            <CButton
              color="primary"
              onClick={handleCreateMedicationSchedule}
              disabled={!noOngoingMedications} // Disable if there are ongoing medications
            >
              Create Medication Schedule
            </CButton>
          ) : (
            <div>
              {/* Render the Create Medication Form */}
              <CreateMedicationForm />

              {/* Cancel Button to close the form */}
              <CButton
                color="secondary"
                onClick={handleCancelMedicationForm}
                style={{ marginTop: '10px' }}
              >
                Cancel
              </CButton>
            </div>
          )}
        </CCol>

        <CCol xs={12}>
          <OngoingMedication medications={medications} />
        </CCol>
      </CRow>
    </div>
  )
}

export default Dashboard
