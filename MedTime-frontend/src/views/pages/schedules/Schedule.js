import React, { useState, useEffect } from 'react'
import axios from 'axios'
import {
  CTable,
  CTableHead,
  CTableRow,
  CTableHeaderCell,
  CTableBody,
  CTableDataCell,
  CButton,
} from '@coreui/react'

const Schedules = () => {
  const [upcomingSchedules, setUpcomingSchedules] = useState([])
  const [previousSchedules, setPreviousSchedules] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Fetch schedules from the API
  useEffect(() => {
    const fetchSchedules = async () => {
      try {
        setLoading(true)
        const response = await axios.get(import.meta.env.VITE_MEDICATIONS_URL)
        const data = response.data

        // Separate upcoming and previous schedules
        const now = new Date()
        const upcoming = data.filter((schedule) => new Date(schedule.date) >= now)
        const previous = data.filter((schedule) => new Date(schedule.date) < now)

        setUpcomingSchedules(upcoming)
        setPreviousSchedules(previous)
      } catch (error) {
        setError('Error fetching schedules')
      } finally {
        setLoading(false)
      }
    }

    fetchSchedules()
  }, [])

  // Function to handle new schedule creation (this would open a form modal or redirect to a creation page)
  const handleCreateSchedule = () => {
    alert('Create a new schedule form here')
  }

  return (
    <div>
      <h1>Schedules</h1>

      {/* Button to create a new schedule */}
      <CButton color="primary" onClick={handleCreateSchedule}>
        Create Schedule
      </CButton>

      {/* Show loading state */}
      {loading && <p>Loading schedules...</p>}

      {/* Show error if there's an issue */}
      {error && <p>{error}</p>}

      {/* Upcoming schedules table */}
      <h2>Upcoming Schedules</h2>
      {upcomingSchedules.length > 0 ? (
        <CTable hover striped responsive>
          <CTableHead>
            <CTableRow>
              <CTableHeaderCell>ID</CTableHeaderCell>
              <CTableHeaderCell>Title</CTableHeaderCell>
              <CTableHeaderCell>Date</CTableHeaderCell>
              <CTableHeaderCell>Description</CTableHeaderCell>
            </CTableRow>
          </CTableHead>
          <CTableBody>
            {upcomingSchedules.map((schedule) => (
              <CTableRow key={schedule.id}>
                <CTableDataCell>{schedule.id}</CTableDataCell>
                <CTableDataCell>{schedule.title}</CTableDataCell>
                <CTableDataCell>{new Date(schedule.date).toLocaleDateString()}</CTableDataCell>
                <CTableDataCell>{schedule.description}</CTableDataCell>
              </CTableRow>
            ))}
          </CTableBody>
        </CTable>
      ) : (
        <p>No upcoming schedules found.</p>
      )}

      {/* Previous schedules table */}
      <h2>Previous Schedules</h2>
      {previousSchedules.length > 0 ? (
        <CTable hover striped responsive>
          <CTableHead>
            <CTableRow>
              <CTableHeaderCell>ID</CTableHeaderCell>
              <CTableHeaderCell>Title</CTableHeaderCell>
              <CTableHeaderCell>Date</CTableHeaderCell>
              <CTableHeaderCell>Description</CTableHeaderCell>
            </CTableRow>
          </CTableHead>
          <CTableBody>
            {previousSchedules.map((schedule) => (
              <CTableRow key={schedule.id}>
                <CTableDataCell>{schedule.id}</CTableDataCell>
                <CTableDataCell>{schedule.title}</CTableDataCell>
                <CTableDataCell>{new Date(schedule.date).toLocaleDateString()}</CTableDataCell>
                <CTableDataCell>{schedule.description}</CTableDataCell>
              </CTableRow>
            ))}
          </CTableBody>
        </CTable>
      ) : (
        <p>No previous schedules found.</p>
      )}
    </div>
  )
}

export default Schedules
