/* eslint-disable react/prop-types */
import React from 'react'
import {
  CTable,
  CTableHead,
  CTableRow,
  CTableHeaderCell,
  CTableBody,
  CTableDataCell,
  CCard,
  CCardBody,
} from '@coreui/react'

const OngoingMedication = ({ medications }) => {
  return (
    <CCard className="ongoing-medication">
      <CCardBody>
        <h5>Ongoing Medications</h5>
        {medications.length > 0 ? (
          <CTable hover striped responsive>
            <CTableHead>
              <CTableRow>
                <CTableHeaderCell>Name</CTableHeaderCell>
                <CTableHeaderCell>Capsules/Doses Taken</CTableHeaderCell>
                <CTableHeaderCell>Total Dose</CTableHeaderCell>
              </CTableRow>
            </CTableHead>
            <CTableBody>
              {medications.map((med, index) => (
                <CTableRow key={index}>
                  <CTableDataCell>{med.name}</CTableDataCell>
                  <CTableDataCell>{med.daysCompleted}</CTableDataCell>
                  <CTableDataCell>{med.totalDays}</CTableDataCell>
                </CTableRow>
              ))}
            </CTableBody>
          </CTable>
        ) : (
          <p>No ongoing medications found.</p>
        )}
      </CCardBody>
    </CCard>
  )
}

export default OngoingMedication
