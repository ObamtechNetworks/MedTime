/* eslint-disable react/prop-types */
import React from 'react'
import { CCard, CCardBody } from '@coreui/react'

const NextDose = ({ hoursLeft }) => {
  return (
    <CCard>
      <CCardBody className="text-center">
        <h5>Next Dose</h5>
        <div style={{ fontSize: '36px', fontWeight: 'bold', color: '#f39c12' }}>
          {hoursLeft} Hours
        </div>
      </CCardBody>
    </CCard>
  )
}

export default NextDose
