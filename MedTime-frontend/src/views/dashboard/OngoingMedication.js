import React from 'react';
import { CTable, CTableHead, CTableBody, CTableRow, CTableHeaderCell, CTableDataCell } from '@coreui/react';

const OngoingMedication = ({ medications }) => {
  return (
    <div>
      <h3>Ongoing Medications</h3>
      {medications.length > 0 ? (
        <CTable hover striped responsive>
          <CTableHead>
            <CTableRow>
              <CTableHeaderCell>Medication</CTableHeaderCell>
              <CTableHeaderCell>Total Quantity</CTableHeaderCell>
              <CTableHeaderCell>Quantity Left</CTableHeaderCell>
              <CTableHeaderCell>Dosage Per Intake</CTableHeaderCell>
              <CTableHeaderCell>Frequency / Interval</CTableHeaderCell> {/* Modified header */}
            </CTableRow>
          </CTableHead>
          <CTableBody>
            {medications.map((medication) => (
              <CTableRow key={medication.id}>
                <CTableDataCell>{medication.drug_name}</CTableDataCell>
                <CTableDataCell>{medication.total_quantity}</CTableDataCell>
                <CTableDataCell>{medication.total_left}</CTableDataCell>
                <CTableDataCell>{medication.dosage_per_intake}</CTableDataCell>
                <CTableDataCell>
                  {medication.priority_flag
                    ? `Every ${medication.time_interval} hours (Priority Drug)`
                    : `${medication.frequency_per_day} times per day`}
                </CTableDataCell> {/* Conditional rendering */}
              </CTableRow>
            ))}
          </CTableBody>
        </CTable>
      ) : (
        <p>No ongoing medications found.</p>
      )}
    </div>
  );
};

export default OngoingMedication;
