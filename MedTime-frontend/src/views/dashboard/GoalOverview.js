/* eslint-disable react/prop-types */
import React from 'react'
import { CCard, CCardBody, CCol, CRow, CProgress } from '@coreui/react'

const GoalOverview = ({ progressPercentage, totalDays, daysRemaining }) => {
  return (
    <CCard>
      <CCardBody className="text-center">
        <h5>Goal Overview</h5>
        <div className="progress-wrapper">
          <CProgress
            value={progressPercentage}
            color="success"
            className="mb-3"
            style={{ height: '150px', borderRadius: '50%', width: '150px' }}
          >
            <div
              style={{ position: 'relative', top: '-140px', fontSize: '24px', fontWeight: 'bold' }}
            >
              {progressPercentage}%
            </div>
          </CProgress>
        </div>
        <CRow className="justify-content-center">
          <CCol xs="auto">
            <div>
              <strong>Total Days:</strong> {totalDays}
            </div>
          </CCol>
          <CCol xs="auto">
            <div>
              <strong>Days Remaining:</strong> {daysRemaining}
            </div>
          </CCol>
        </CRow>
      </CCardBody>
    </CCard>
  )
}

export default GoalOverview
