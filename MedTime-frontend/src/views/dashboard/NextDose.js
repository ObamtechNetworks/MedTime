/* eslint-disable react/prop-types */
import React from 'react';
import { CCard, CCardBody } from '@coreui/react';

const NextDose = ({ timeLeft }) => {
  if (!timeLeft) {
    return (
      <CCard>
        <CCardBody className="text-center">
          <h5>Next Dose</h5>
          <div style={{ fontSize: '36px', fontWeight: 'bold', color: '#f39c12' }}>
            No upcoming doses
          </div>
        </CCardBody>
      </CCard>
    );
  }

  return (
    <CCard>
      <CCardBody className="text-center">
        <h5>Next Dose</h5>
        <div style={{ fontSize: '36px', fontWeight: 'bold', color: '#f39c12' }}>
          {`${timeLeft.hours}h ${timeLeft.minutes}m ${timeLeft.seconds}s`}
        </div>
      </CCardBody>
    </CCard>
  );
};

export default NextDose;
