import React, { useState, useEffect } from 'react'
import { useSchedules } from './ScheduleContext'
import {
  CButton,
  CForm,
  CFormLabel,
  CFormInput,
  CFormSwitch,
  CCard,
  CCardBody,
  CModal,
  CModalHeader,
  CModalBody,
  CModalFooter,
} from '@coreui/react'

// import datetime picker and its css
import Datetime from 'react-datetime'
import 'react-datetime/css/react-datetime.css'

import { toast, ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import api from './axiosInterceptor'

const CreateMedicationForm = () => {
  const [currentDrug, setCurrentDrug] = useState({
    drug_name: '',
    total_quantity: '',
    dosage_per_intake: '',
    frequency_per_day: '',
    time_interval: '',
    priority_flag: false,
    priority_lead_time: '',
  })

  const { fetchSchedules } = useSchedules(); // Get fetchSchedules from context


  const [drugList, setDrugList] = useState([])
  const [drugCount, setDrugCount] = useState(0)
  const [editingIndex, setEditingIndex] = useState(-1)
  const [showPreview, setShowPreview] = useState(false)

  const [selectedDateTime, setSelectedDateTime] = useState(null)
  const [showDateTimeModal, setShowDateTimeModal] = useState(true)
  const [showForm, setShowForm] = useState(false)

  const [loading, setLoading] = useState(false)  // Add loading state

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target
    let inputValue
    if (type === 'checkbox') {
      inputValue = checked
    } else if (type === 'number') {
      inputValue = +value
    } else {
      inputValue = value
    }

    setCurrentDrug({ ...currentDrug, [name]: inputValue })
  }

 const isValidDrug = () => {
  // Check if the drug name, total quantity, and dosage per intake are provided
  if (!currentDrug.drug_name || currentDrug.total_quantity <= 0 || currentDrug.dosage_per_intake <= 0) {
    return false; // Basic validation fails
  }

  if (currentDrug.priority_flag) {
    // For priority drugs, validate the required fields
    if (currentDrug.priority_lead_time <= 0 || currentDrug.time_interval <= 0) {
      return false; // Invalid priority lead time or time interval
    }
    
    // Set frequency_per_day to null if it's a priority drug
    currentDrug.frequency_per_day = null;
  } else {
    // For regular drugs, validate frequency_per_day
    if (currentDrug.frequency_per_day <= 0) {
      return false; // Invalid frequency per day
    }
    
    // Set priority_lead_time and time_interval to null for regular drugs
    currentDrug.priority_lead_time = null;
    currentDrug.time_interval = null;
  }

  return true; // All validations passed
};


  const handleAddOrUpdateDrug = () => {
    if (!isValidDrug()) {
      toast.warning('Please fill in all the required fields with valid data.')
      return
    }

    if (editingIndex > -1) {
      const updatedDrugList = drugList.map((drug, index) =>
        index === editingIndex ? currentDrug : drug
      )
      setDrugList(updatedDrugList)
      setEditingIndex(-1)
    } else {
      setDrugList([...drugList, currentDrug])
      setDrugCount(drugCount + 1)
    }

    setCurrentDrug({
      drug_name: '',
      total_quantity: '',
      dosage_per_intake: '',
      frequency_per_day: '',
      time_interval: '',
      priority_flag: false,
      priority_lead_time: '',
    })
  }

  const handleEditDrug = (index) => {
    setCurrentDrug(drugList[index])
    setEditingIndex(index)
  }

  const handleDeleteDrug = (index) => {
    const updatedDrugList = drugList.filter((_, i) => i !== index)
    setDrugList(updatedDrugList)
    setDrugCount(drugCount - 1)
    setEditingIndex(-1)
    setCurrentDrug({
      drug_name: '',
      total_quantity: '',
      dosage_per_intake: '',
      frequency_per_day: '',
      time_interval: '',
      priority_flag: false,
      priority_lead_time: '',
    })
  }

  const handlePreview = () => {
    if (drugList.length === 0) {
      alert('Please add at least one drug before previewing.')
      return
    }
    setShowPreview(true)
  }

  const handleSubmit = async () => {
    if (drugList.length === 0) {
      toast.error("Please add at least one medication before submitting.");
      return;
    }
    setLoading(true) // Start loading
  
  try {
    const payload = {
      start_time: selectedDateTime.toISOString(),  // Send the scheduled time along with medications
      medications: drugList
    };
    console.log(payload)

    // Make the API call to create the medications
    const response = await api.post(import.meta.env.VITE_MEDICATIONS_URL, payload);

    // On success, show a success message
    toast.success("Medications and schedules successfully created!");

     // Call fetchSchedules() to update the schedules list after medication creation
    await fetchSchedules();  // <-- Call this function here


    // Reset the form and drug list
    setDrugList([]);
    setCurrentDrug({
      drug_name: '',
      total_quantity: '',
      dosage_per_intake: '',
      frequency_per_day: '',
      time_interval: '',
      priority_flag: false,
      priority_lead_time: '',
    });
    setDrugCount(0);
    setShowPreview(false); // Close the modal
  } catch (error) {
    console.error("Failed to submit medications", error);
    toast.error("An error occurred while submitting medications.");
  } finally {
    setLoading(false); // Stop loading
  }
};
 
  const yesterday = Datetime.moment().subtract(1, 'day')
  const isValidDate = (current) => current.isAfter(yesterday)

  const handleDateTimeConfirm = (dateTime) => {
    if (dateTime && dateTime.isAfter(Datetime.moment())) {
      setSelectedDateTime(dateTime)
      setShowDateTimeModal(false)
      setShowForm(true)
    } else {
      toast.error('Please select a valid future date and time.')
    }
  }

  const formatDateTime = (dateTime) => {
    return dateTime ? dateTime.format('DD MMM YYYY, h:mm A') : ''
  }

  return (
    <div className="container">
      <CCard>
        <ToastContainer />
        <CCardBody>
          {/* Display selected schedule time at the top */}
          {selectedDateTime && (
            <div style={{ marginBottom: '20px' }}>
              <h5>Schedule to begin at: {formatDateTime(selectedDateTime)}</h5>
            </div>
          )}

          {/* Datetime picker modal */}
          <CModal visible={showDateTimeModal} backdrop="static" keyboard={false}>
            <CModalHeader>Select Medication Start Time</CModalHeader>
            <CModalBody>
              <Datetime
                onChange={setSelectedDateTime}
                value={selectedDateTime}
                isValidDate={isValidDate} // Only allow future dates and times
              />
            </CModalBody>
            <CModalFooter>
              <CButton color="secondary" onClick={() => setShowDateTimeModal(false)}>
                Cancel
              </CButton>
              <CButton color="primary" onClick={() => handleDateTimeConfirm(selectedDateTime)}>
                Confirm
              </CButton>
            </CModalFooter>
          </CModal>

          {/* Form section (hidden initially, shown after datetime selection) */}
          {showForm && (
            <CForm>
              <div className="mb-3">
                <CFormLabel>Drug Name</CFormLabel>
                <CFormInput
                  type="text"
                  name="drug_name"
                  value={currentDrug.drug_name}
                  onChange={handleInputChange}
                  placeholder="Enter drug name"
                  required
                />
              </div>

              <div className="mb-3">
                <CFormLabel>Total Quantity</CFormLabel>
                <CFormInput
                  type="number"
                  name="total_quantity"
                  value={currentDrug.total_quantity}
                  onChange={handleInputChange}
                  placeholder="Enter total quantity"
                  min="1"
                  step="1"
                  onKeyDown={(e) => ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()}
                  required
                />
              </div>

              <div className="mb-3">
                <CFormSwitch
                  label="Is this a priority (To be taken in Isolation)?"
                  id="priorityFlagSwitch"
                  name="priority_flag"
                  checked={currentDrug.priority_flag}
                  onChange={handleInputChange}
                />
              </div>

              {/* Conditionally show Priority Lead Time if priority is set */}
              {currentDrug.priority_flag ? (
                <>
                  <div className="mb-3">
                    <CFormLabel style={{ fontWeight: 'bold', color: 'red' }}>
                      Enter gap time before other drugs are taken (In Minutes)
                    </CFormLabel>
                    <CFormInput
                      type="number"
                      name="priority_lead_time"
                      value={currentDrug.priority_lead_time}
                      onChange={handleInputChange}
                      placeholder="Enter lead time in minutes"
                      min="1"
                      step="1"
                      onKeyDown={(e) => ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()}
                      required
                    />
                  </div>

                  <div className="mb-3">
                    <CFormLabel>Time Interval (Hours)</CFormLabel>
                    <CFormInput
                      type="number"
                      name="time_interval"
                      value={currentDrug.time_interval}
                      onChange={handleInputChange}
                      placeholder="Enter time interval in hours"
                      min="1"
                      step="1"
                      onKeyDown={(e) => ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()}
                    />
                  </div>
                </>
              ) : (
                <div className="mb-3">
                  <CFormLabel>Frequency Per Day</CFormLabel>
                  <CFormInput
                    type="number"
                    name="frequency_per_day"
                    value={currentDrug.frequency_per_day}
                    onChange={handleInputChange}
                    placeholder="Enter frequency per day"
                    min="1"
                    step="1"
                    onKeyDown={(e) => ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()}
                    required
                  />
                </div>
              )}

              <div className="mb-3">
                <CFormLabel>Dosage Per Intake</CFormLabel>
                <CFormInput
                  type="number"
                  name="dosage_per_intake"
                  value={currentDrug.dosage_per_intake}
                  onChange={handleInputChange}
                  placeholder="Enter dosage per intake"
                  min="1"
                  step="1"
                  onKeyDown={(e) => ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()}
                  required
                />
              </div>

              {/* Add/Update Drug Button */}
              <CButton color="primary" onClick={handleAddOrUpdateDrug}>
                {editingIndex > -1 ? 'Update Drug' : 'Add Drug'}
              </CButton>

              {/* Drug Count Indicator */}
              <div>
                <span>Drugs Added: {drugCount}</span>
              </div>

              {/* Preview of Added Drugs */}
              <div>
                <h5>Added Drugs:</h5>
                {drugList.length > 0 ? (
                  <ul>
                    {drugList.map((drug, index) => (
                      <li key={index}>
                        {`${drug.drug_name} - ${drug.total_quantity} qty, ${drug.dosage_per_intake} per dose`}
                        <CButton
                          size="sm"
                          color="info"
                          onClick={() => handleEditDrug(index)}
                          style={{ marginLeft: '10px' }}
                        >
                          Edit
                        </CButton>{' '}
                        <CButton
                          size="sm"
                          color="danger"
                          onClick={() => handleDeleteDrug(index)}
                        >
                          Delete
                        </CButton>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p>No drugs added yet.</p>
                )}
              </div>

              {/* Preview and Submit */}
            {drugList.length > 0 && (
            <CButton color="success" className="mt-3" onClick={handlePreview}>
                Preview & Submit
            </CButton>
            )}
            </CForm>
          )}
        </CCardBody>
      </CCard>

      {/* Preview Modal */}
      <CModal visible={showPreview} onClose={() => setShowPreview(false)} keyboard={false} backdrop="static">
        <CModalHeader>Preview Drugs</CModalHeader>
        <CModalBody>
          {drugList.map((drug, index) => (
            <div key={index}>
              <p>{`${drug.drug_name}: ${drug.total_quantity} total, ${drug.dosage_per_intake} per dose, ${drug.frequency_per_day} times/day`}</p>
              {drug.priority_flag && (
                <p>Priority Lead Time: {drug.priority_lead_time} minutes</p>
              )}
            </div>
          ))}
        </CModalBody>
        <CModalFooter>
            <CButton color="primary" onClick={handleSubmit} disabled={loading}>
                {loading ? 'Submitting...' : 'Submit'}
            </CButton>
            <CButton color="secondary" onClick={() => setShowPreview(false)} disabled={loading}>
            Edit
            </CButton>
        </CModalFooter>
      </CModal>
    </div>
  )
}

export default CreateMedicationForm
