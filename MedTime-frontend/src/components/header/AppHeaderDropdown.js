import React, { useState } from 'react';
import {
  CAvatar,
  CDropdown,
  CDropdownDivider,
  CDropdownHeader,
  CDropdownItem,
  CDropdownMenu,
  CDropdownToggle,
} from '@coreui/react';
import { cilSettings, cilUser, cilLockLocked } from '@coreui/icons';
import CIcon from '@coreui/icons-react';
import { Link } from 'react-router-dom';
import avatar8 from './../../assets/images/avatars/8.jpg';
import Logout from '../../views/pages/logout/Logout';
import { useAuth } from '../../api/authContext';

const AppHeaderDropdown = () => {
  const [showModal, setShowModal] = useState(false);
  const { setIsAuthenticated } = useAuth(); // Get setIsAuthenticated from context

  const handleLogoutClick = (event) => {
    event.preventDefault(); // Prevent the default Link behavior
    setShowModal(true); // Show the logout confirmation modal
  };

  return (
    <>
      <CDropdown variant="nav-item">
        <CDropdownToggle placement="bottom-end" className="py-0 pe-0" caret={false}>
          <CAvatar src={avatar8} size="md" />
        </CDropdownToggle>
        <CDropdownMenu className="pt-0" placement="bottom-end">
          <CDropdownHeader className="bg-body-secondary fw-semibold mb-2">Account</CDropdownHeader>

          {/* Profile */}
          <CDropdownItem>
            <Link to="/profile" className="dropdown-item">
              <CIcon icon={cilUser} className="me-2" />
              Profile
            </Link>
          </CDropdownItem>

          {/* Settings */}
          <CDropdownItem>
            <Link to="/settings" className="dropdown-item">
              <CIcon icon={cilSettings} className="me-2" />
              Settings
            </Link>
          </CDropdownItem>

          <CDropdownDivider />

          {/* Logout */}
          <CDropdownItem onClick={handleLogoutClick} style={{ cursor: 'pointer' }}>
            <CIcon icon={cilLockLocked} className="me-2" />
            Logout
          </CDropdownItem>
        </CDropdownMenu>
      </CDropdown>

      {/* Logout Confirmation Modal */}
      <Logout showModal={showModal} setShowModal={setShowModal} setIsAuthenticated={setIsAuthenticated} /> {/* Pass setIsAuthenticated */}
    </>
  );
};

export default AppHeaderDropdown;



// import React from 'react'
// import {
//   CAvatar,
//   CBadge,
//   CDropdown,
//   CDropdownDivider,
//   CDropdownHeader,
//   CDropdownItem,
//   CDropdownMenu,
//   CDropdownToggle,
// } from '@coreui/react'
// import {
//   cilBell,
//   cilCreditCard,
//   cilCommentSquare,
//   cilEnvelopeOpen,
//   cilFile,
//   cilLockLocked,
//   cilSettings,
//   cilTask,
//   cilUser,
// } from '@coreui/icons'
// import CIcon from '@coreui/icons-react'

// import avatar8 from './../../assets/images/avatars/8.jpg'

// const AppHeaderDropdown = () => {
//   return (
//     <CDropdown variant="nav-item">
//       <CDropdownToggle placement="bottom-end" className="py-0 pe-0" caret={false}>
//         <CAvatar src={avatar8} size="md" />
//       </CDropdownToggle>
//       <CDropdownMenu className="pt-0" placement="bottom-end">
//         <CDropdownHeader className="bg-body-secondary fw-semibold mb-2">Account</CDropdownHeader>
//         <CDropdownItem href="#">
//           <CIcon icon={cilBell} className="me-2" />
//           Updates
//           <CBadge color="info" className="ms-2">
//             42
//           </CBadge>
//         </CDropdownItem>
//         <CDropdownItem href="#">
//           <CIcon icon={cilEnvelopeOpen} className="me-2" />
//           Messages
//           <CBadge color="success" className="ms-2">
//             42
//           </CBadge>
//         </CDropdownItem>
//         <CDropdownItem href="#">
//           <CIcon icon={cilTask} className="me-2" />
//           Tasks
//           <CBadge color="danger" className="ms-2">
//             42
//           </CBadge>
//         </CDropdownItem>
//         <CDropdownItem href="#">
//           <CIcon icon={cilCommentSquare} className="me-2" />
//           Comments
//           <CBadge color="warning" className="ms-2">
//             42
//           </CBadge>
//         </CDropdownItem>
//         <CDropdownHeader className="bg-body-secondary fw-semibold my-2">Settings</CDropdownHeader>
//         <CDropdownItem href="#">
//           <CIcon icon={cilUser} className="me-2" />
//           Profile
//         </CDropdownItem>
//         <CDropdownItem href="#">
//           <CIcon icon={cilSettings} className="me-2" />
//           Settings
//         </CDropdownItem>
//         <CDropdownItem href="#">
//           <CIcon icon={cilCreditCard} className="me-2" />
//           Payments
//           <CBadge color="secondary" className="ms-2">
//             42
//           </CBadge>
//         </CDropdownItem>
//         <CDropdownItem href="#">
//           <CIcon icon={cilFile} className="me-2" />
//           Projects
//           <CBadge color="primary" className="ms-2">
//             42
//           </CBadge>
//         </CDropdownItem>
//         <CDropdownDivider />
//         <CDropdownItem href="#">
//           <CIcon icon={cilLockLocked} className="me-2" />
//           Lock Account
//         </CDropdownItem>
//       </CDropdownMenu>
//     </CDropdown>
//   )
// }

// export default AppHeaderDropdown
