import React, { useEffect, useState } from 'react';
import { CTable, CTableBody, CTableRow, CTableHeaderCell, CTableDataCell, CTableHead } from '@coreui/react';
import api from '../../../api/axiosInterceptor';
import { format } from 'date-fns'; // For formatting date

const Schedules = () => {
  const [schedules, setSchedules] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch schedules from API
  const fetchSchedules = async () => {
    try {
      const response = await api.get(import.meta.env.VITE_SCHEDULES_URL); // Replace with correct endpoint
      setSchedules(response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch schedules');
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSchedules();
  }, []);

  // Filter schedules based on status
  const upcomingSchedules = schedules.filter(schedule => schedule.status === 'scheduled');
  const missedSchedules = schedules.filter(schedule => schedule.status === 'missed');

  return (
    <div>
      <h3>Medication Schedules</h3>
      {loading ? (
        <p>Loading schedules...</p>
      ) : error ? (
        <p>{error}</p>
      ) : (
        <>
          {/* Upcoming Schedules */}
          <h4>Upcoming Schedules</h4>
          {upcomingSchedules.length > 0 ? (
            <CTable hover striped responsive>
              <CTableHead>
                <CTableRow>
                  <CTableHeaderCell>Medication Name</CTableHeaderCell>
                  <CTableHeaderCell>Created At</CTableHeaderCell>
                  <CTableHeaderCell>Next Dose Due</CTableHeaderCell>
                  <CTableHeaderCell>Status</CTableHeaderCell>
                </CTableRow>
              </CTableHead>
              <CTableBody>
                {upcomingSchedules.map(schedule => (
                  <CTableRow key={schedule.id}>
                    <CTableDataCell>{schedule.medication_name}</CTableDataCell>
                    <CTableDataCell>{format(new Date(schedule.created_at), 'PPpp')}</CTableDataCell>
                    <CTableDataCell>{format(new Date(schedule.next_dose_due_at), 'PPpp')}</CTableDataCell>
                    <CTableDataCell>{schedule.status}</CTableDataCell>
                  </CTableRow>
                ))}
              </CTableBody>
            </CTable>
          ) : (
            <p>No upcoming schedules found.</p>
          )}

          {/* Missed Schedules */}
          <h4>Missed Schedules</h4>
          {missedSchedules.length > 0 ? (
            <CTable hover striped responsive color="danger">
              <CTableHead>
                <CTableRow>
                  <CTableHeaderCell>Medication Name</CTableHeaderCell>
                  <CTableHeaderCell>Created At</CTableHeaderCell>
                  <CTableHeaderCell>Next Dose Due</CTableHeaderCell>
                  <CTableHeaderCell>Status</CTableHeaderCell>
                </CTableRow>
              </CTableHead>
              <CTableBody>
                {missedSchedules.map(schedule => (
                  <CTableRow key={schedule.id}>
                    <CTableDataCell>{schedule.medication_name}</CTableDataCell>
                    <CTableDataCell>{format(new Date(schedule.created_at), 'PPpp')}</CTableDataCell>
                    <CTableDataCell>{format(new Date(schedule.next_dose_due_at), 'PPpp')}</CTableDataCell>
                    <CTableDataCell>{schedule.status}</CTableDataCell>
                  </CTableRow>
                ))}
              </CTableBody>
            </CTable>
          ) : (
            <p>No missed schedules found.</p>
          )}
        </>
      )}
    </div>
  );
};

export default Schedules;
