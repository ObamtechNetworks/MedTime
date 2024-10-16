import React, { useState, useEffect } from 'react'
import { CRow, CCol, CButton } from '@coreui/react'
import GoalOverview from './GoalOverview'
import NextDose from './NextDose'
import OngoingMedication from './OngoingMedication'
import './Dashboard.scss' // Importing Sass for styling

const Dashboard = () => {
  const [progress, setProgress] = useState(75) // Example percentage
  const [totalDays, setTotalDays] = useState(30) // Example total days
  const [daysRemaining, setDaysRemaining] = useState(7) // Example days remaining
  const [hoursLeft, setHoursLeft] = useState(5) // Example hours till next dose
  const [medications, setMedications] = useState([
    // { name: 'Med 1', daysCompleted: 2, totalDays: 30 },
    // { name: 'Med 2', daysCompleted: 3, totalDays: 20 },
    // { name: 'Med 3', daysCompleted: 3, totalDays: 10 },
  ])

  // Check if there are ongoing medications
  const noOngoingMedications = medications.length === 0

  // Function to handle schedule creation click
  const handleCreateMedicationSchedule = () => {
    if (noOngoingMedications) {
      // Logic to open medication creation form or redirect
      alert('Create a new medication schedule here.')
    }
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

        {/* Button to Create Medication Schedule */}
        <CCol xs={12}>
          <CButton
            color="primary"
            onClick={handleCreateMedicationSchedule}
            disabled={!noOngoingMedications}
          >
            Create Medication Schedule
          </CButton>
        </CCol>

        <CCol xs={12}>
          <OngoingMedication medications={medications} />
        </CCol>
      </CRow>
    </div>
  )
}

export default Dashboard
