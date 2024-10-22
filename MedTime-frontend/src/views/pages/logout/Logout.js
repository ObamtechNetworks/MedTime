import React from 'react';
import { useNavigate } from 'react-router-dom';
import { CModal, CModalHeader, CModalTitle, CModalBody, CModalFooter, CButton } from '@coreui/react';

const Logout = ({ showModal, setShowModal, setIsAuthenticated }) => { // Accept setIsAuthenticated as prop
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.clear(); // Clears all items in localStorage
    setIsAuthenticated(false); // Update authentication state
    setShowModal(false); // Close the modal
    navigate('/'); // Redirect to the home/landing page
  };

  return (
    <CModal visible={showModal} onClose={() => setShowModal(false)}>
      <CModalHeader>
        <CModalTitle>Confirm Logout</CModalTitle>
      </CModalHeader>
      <CModalBody>Are you sure you want to logout?</CModalBody>
      <CModalFooter>
        <CButton color="secondary" onClick={() => setShowModal(false)}>Cancel</CButton>
        <CButton color="danger" onClick={handleLogout}>Logout</CButton>
      </CModalFooter>
    </CModal>
  );
};

export default Logout;
