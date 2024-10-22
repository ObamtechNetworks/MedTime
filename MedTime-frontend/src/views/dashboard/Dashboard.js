import React, { useState, useEffect } from 'react';
import { CRow, CCol, CButton } from '@coreui/react';
import CreateMedicationForm from '../../api/createMedicationModal'
import GoalOverview from './GoalOverview';
import NextDose from './NextDose';
import OngoingMedication from './OngoingMedication';
import './Dashboard.scss'; // Importing Sass for styling
import { useSchedules } from '../../api/ScheduleContext';
import api from '../../api/axiosInterceptor'; // axios interceptor for API calls

const Dashboard = () => {
  const { schedules, loading: schedulesLoading, error: schedulesError, fetchSchedules } = useSchedules();
  const [medications, setMedications] = useState([]); // State to store medication data
  const [loading, setLoading] = useState(true); // Loading state for medications
  const [error, setError] = useState(null); // Error state
  const [progress, setProgress] = useState(75); // Example percentage
  const [totalDays, setTotalDays] = useState(30); // Example total days
  const [daysRemaining, setDaysRemaining] = useState(7); // Example days remaining
  const [timeLeft, setTimeLeft] = useState(null); // Time left for next dose (hours, minutes, seconds)
  const [showMedicationForm, setShowMedicationForm] = useState(false); // Track if form is open

  // Fetch ongoing medications
const fetchMedications = async () => {
  try {
    const response = await api.get(import.meta.env.VITE_MEDICATIONS_URL);
    const meds = response.data;

    if (meds.length > 0) {
      let totalProgress = 0;
      let totalDaysSum = 0;  // Sum up total days across all medications
      let totalDaysRemainingSum = 0; // To sum up the remaining days
      let totalMedications = meds.length;

      meds.forEach((medication) => {
        const { total_quantity, total_left, dosage_per_intake, frequency_per_day, time_interval, priority_flag } = medication;
        
        if (total_quantity > 0) {
          const medicationProgress = ((total_quantity - total_left) / total_quantity) * 100;
          totalProgress += medicationProgress;
          
          // Calculate total days for the medication
          let totalDaysForMedication = 0;
          let remainingDaysForMedication = 0;
          
          if (priority_flag) {
            // For priority drugs, calculate days based on time_interval
            const dailyDoses = 24 / time_interval;
            totalDaysForMedication = total_quantity / (dosage_per_intake * dailyDoses);
            remainingDaysForMedication = total_left / (dosage_per_intake * dailyDoses);
          } else {
            // For regular drugs, use frequency_per_day
            totalDaysForMedication = total_quantity / (dosage_per_intake * frequency_per_day);
            remainingDaysForMedication = total_left / (dosage_per_intake * frequency_per_day);
          }

          totalDaysSum += totalDaysForMedication;
          totalDaysRemainingSum += remainingDaysForMedication;
        }
      });

      const averageProgress = totalProgress / totalMedications;
      const daysRemaining = Math.ceil(totalDaysRemainingSum); // Dynamic days remaining calculation

      setTotalDays(Math.ceil(totalDaysSum));  // Use the calculated total days
      setDaysRemaining(daysRemaining); // Set dynamically calculated days remaining
      setProgress(averageProgress); // Set the average progress across all medications
    }

    setMedications(meds);
    setLoading(false);
  } catch (err) {
    setError('Failed to fetch medications');
    setLoading(false);
  }
};


  useEffect(() => {
    fetchMedications(); // Fetch medications when component mounts
  }, []);

  useEffect(() => {
    if (!schedules.length) {
      fetchSchedules();
    } else {
      const calculateNextDoseTime = () => {
        const now = new Date();
        const upcomingSchedules = schedules
          .filter((schedule) => new Date(schedule.next_dose_due_at) > now && schedule.status === 'scheduled')
          .sort((a, b) => new Date(a.next_dose_due_at) - new Date(b.next_dose_due_at));

        if (upcomingSchedules.length > 0) {
          const nextDoseTime = new Date(upcomingSchedules[0].next_dose_due_at);
          const diffInMs = nextDoseTime - now;

          const hours = Math.floor(diffInMs / (1000 * 60 * 60));
          const minutes = Math.floor((diffInMs % (1000 * 60 * 60)) / (1000 * 60));
          const seconds = Math.floor((diffInMs % (1000 * 60)) / 1000);

          setTimeLeft({ hours, minutes, seconds });
        } else {
          setTimeLeft(null); // No upcoming doses
        }
      };

      calculateNextDoseTime();
      const interval = setInterval(calculateNextDoseTime, 1000); // Update countdown every second

      return () => clearInterval(interval); // Clean up the interval on component unmount
    }
  }, [schedules, fetchSchedules]);

  const handleCreateMedicationSchedule = () => {
    setShowMedicationForm(true); // Show the form when button is clicked
  };

  const handleCancelMedicationForm = () => {
    setShowMedicationForm(false); // Hide the form if the user cancels
  };

  const noOngoingMedications = medications.length === 0;

  return (
    <div className="dashboard-container">
      <CRow className="g-4">
        <CCol md={6}>
          <GoalOverview progressPercentage={progress} totalDays={totalDays} daysRemaining={daysRemaining} />
        </CCol>
        <CCol md={6}>
          <NextDose timeLeft={timeLeft} />
        </CCol>

        <CCol xs={12}>
          {!showMedicationForm ? (
            <CButton color="primary" onClick={handleCreateMedicationSchedule} disabled={!noOngoingMedications}>
              Create Medication Schedule
            </CButton>
          ) : (
            <div>
              <CreateMedicationForm onMedicationCreated={fetchMedications} />
              <CButton color="secondary" onClick={handleCancelMedicationForm} style={{ marginTop: '10px' }}>
                Cancel
              </CButton>
            </div>
          )}
        </CCol>

        <CCol xs={12}>
          {loading ? (
            <p>Loading Medications...</p>
          ) : error ? (
            <p>{error}</p>
          ) : (
            <OngoingMedication medications={medications} />
          )}
        </CCol>
      </CRow>
    </div>
  );
};

export default Dashboard;
