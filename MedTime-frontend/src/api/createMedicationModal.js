import React, { useState, useEffect } from 'react'
import {
  CButton,
  CForm,
  CFormLabel,
  CFormInput,
  CFormSelect,
  CFormSwitch,
  CCard,
  CCardBody,
  CModal,
  CModalHeader,
  CModalBody,
  CModalFooter,
} from '@coreui/react'

import { toast, ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'

const CreateMedicationForm = () => {
  // State for form input fields
  const [currentDrug, setCurrentDrug] = useState({
    drug_name: '',
    total_quantity: '',
    dosage_per_intake: '',
    frequency_per_day: '',
    time_interval: '',
    priority_flag: false,
    priority_lead_time: ''
  })

  // State to hold list of added drugs
  const [drugList, setDrugList] = useState([])
  
  // see details of drug being updated
  useEffect(() => {
    console.log('Updated drug list:', drugList)
  }, [drugList])
  // State to track the number of drugs added
  const [drugCount, setDrugCount] = useState(0)

  // State to track whether the user is editing a drug or adding a new one
  const [editingIndex, setEditingIndex] = useState(-1)

  // State to manage preview modal visibility
  const [showPreview, setShowPreview] = useState(false)

  // Handle form changes
 const handleInputChange = (e) => {
  const { name, value, type, checked } = e.target;
  
  // Determine the input value based on the input type
  let inputValue;
  if (type === 'checkbox') {
    inputValue = checked; // For checkboxes, use the checked property
  } else if (type === 'number') {
    inputValue = +value; // Convert string input to number for numeric inputs
  } else {
    inputValue = value; // Default case for other input types (like text)
  }

  // Update state with the correct value
  setCurrentDrug({ ...currentDrug, [name]: inputValue });
}

  // Input validation check
  const isValidDrug = () => {
    return (
      currentDrug.drug_name &&
      currentDrug.total_quantity > 0 &&
      currentDrug.dosage_per_intake > 0 &&
      (!currentDrug.priority_flag || currentDrug.priority_lead_time > 0)
    )
  }

  // Function to add or update a drug in the drugList array and reset the form
  const handleAddOrUpdateDrug = () => {
    // Validate inputs
    if (!isValidDrug()) {
      toast.warning('Please fill in all the required fields with valid data.')
      return
    }

    if (editingIndex > -1) {
      // If editing, update the drug at the specific index
      const updatedDrugList = drugList.map((drug, index) =>
          index === editingIndex ? currentDrug : drug
    )
      setDrugList(updatedDrugList)
      setEditingIndex(-1) // Reset editing state
    } else {
      // If adding a new drug, add the current drug to the list
      setDrugList([...drugList, currentDrug])
      setDrugCount(drugCount + 1) // Increase drug count
    }
      
    // Clear the form fields
    setCurrentDrug({
      drug_name: '',
      total_quantity: '',
      dosage_per_intake: '',
      frequency_per_day: '',
      time_interval: '',
      priority_flag: false,
      priority_lead_time: ''
    })

  }

  // Function to handle editing a drug
  const handleEditDrug = (index) => {
    setCurrentDrug(drugList[index]) // Populate the form with the drug to be edited
    setEditingIndex(index) // Set editing index
  }

  // Function to handle deleting a drug
  const handleDeleteDrug = (index) => {
    const updatedDrugList = drugList.filter((_, i) => i !== index)
    setDrugList(updatedDrugList)
    setDrugCount(drugCount - 1) // Decrease drug count
    setEditingIndex(-1) // Reset editing mode when deleting
      // Clear the form fields
    setCurrentDrug({
      drug_name: '',
      total_quantity: '',
      dosage_per_intake: '',
      frequency_per_day: '',
      time_interval: '',
      priority_flag: false,
      priority_lead_time: ''
    })
  }

  // Function to handle showing the preview modal
  const handlePreview = () => {
    if (drugList.length === 0) {
      alert('Please add at least one drug before previewing.')
      return
    }
    setShowPreview(true)
  }

  // Function to handle form submission
  const handleSubmit = () => {
    console.log('Submitting final drug list:', drugList)
    setShowPreview(false) // Close the preview modal after submission
  }

  return (
    <div className="container">
        <CCard>
        <ToastContainer />
        <CCardBody>
          {/* Form Section */}
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
            {/* Priority as a switch */}
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
                <CFormLabel style={{fontWeight: "bold", color: "red"}}>Enter gap time before other drugs are taken (In Minutes)</CFormLabel>
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
          </CForm>

          {/* Add/Update Button */}
          <CButton color="primary" onClick={handleAddOrUpdateDrug}>
            {editingIndex > -1 ? 'Update Drug' : 'Add Drug'}
          </CButton>

          {/* Drug Count Indicator */}
          <div>
            <span>{`Drugs Added: ${drugCount}`}</span>
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

          {/* Preview Button */}
          <CButton color="secondary" onClick={handlePreview} disabled={drugList.length === 0}>
            Preview & Submit
          </CButton>
        </CCardBody>
      </CCard>

      {/* Preview Modal */}
      <CModal visible={showPreview} onClose={() => setShowPreview(false)}>
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
          <CButton color="primary" onClick={handleSubmit}>
            Submit
          </CButton>
          <CButton color="secondary" onClick={() => setShowPreview(false)}>
            Edit
          </CButton>
        </CModalFooter>
      </CModal>
    </div>
  )
}

export default CreateMedicationForm
