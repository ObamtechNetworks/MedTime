import React, { useEffect } from 'react';
import { useSchedules } from '../../../api/ScheduleContext';
import { CTable, CTableHead, CTableBody, CTableRow, CTableHeaderCell, CTableDataCell } from '@coreui/react';

const Schedules = () => {
  const { schedules, loading, error, fetchSchedules } = useSchedules();

  useEffect(() => {
    if (!schedules.length) {
      fetchSchedules(); // Fetch schedules if not available
    }
  }, [schedules, fetchSchedules]); // Add fetchSchedules to dependencies

  return (
    <div>
      <h1>Schedules</h1>
      {loading && <p>Loading...</p>}
      {error && <p>{error}</p>}
      {schedules.length > 0 ? (
        <CTable hover striped responsive>
          <CTableHead>
            <CTableRow>
              <CTableHeaderCell>ID</CTableHeaderCell>
              <CTableHeaderCell>Medication</CTableHeaderCell>
              <CTableHeaderCell>Status</CTableHeaderCell>
              <CTableHeaderCell>Next Dose</CTableHeaderCell>
            </CTableRow>
          </CTableHead>
          <CTableBody>
            {schedules.map(schedule => (
              <CTableRow key={schedule.id}>
                <CTableDataCell>{schedule.id}</CTableDataCell>
                <CTableDataCell>{schedule.medication}</CTableDataCell>
                <CTableDataCell>{schedule.status}</CTableDataCell>
                <CTableDataCell>{new Date(schedule.next_dose_due_at).toLocaleString()}</CTableDataCell>
              </CTableRow>
            ))}
          </CTableBody>
        </CTable>
      ) : (
        <p>No schedules found.</p>
      )}
    </div>
  );
};

export default Schedules;
