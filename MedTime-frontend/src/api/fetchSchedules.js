// Fetch schedules function to be used in CreateMedicationForm and Schedules components
const fetchSchedules = async () => {
  try {
    const response = await axios.get(import.meta.env.VITE_SCHEDULES_URL); // Make sure the URL is correct
    const data = response.data;

    // Process the schedule data, separating upcoming and previous schedules
    const now = new Date();
    const upcoming = data.filter((schedule) => new Date(schedule.next_dose_due_at) >= now);
    const previous = data.filter((schedule) => new Date(schedule.next_dose_due_at) < now);

    // Update state with the fetched schedules
    setUpcomingSchedules(upcoming);
    setPreviousSchedules(previous);
  } catch (error) {
    console.error("Error fetching schedules", error);
    toast.error("Failed to fetch schedules.");
  }
};
