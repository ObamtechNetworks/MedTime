import React from 'react';
import { CFooter } from '@coreui/react';

const AppFooter = () => {
  return (
    <CFooter className="px-4">
      <div>
        <span className="fw-bold">MedTime</span> {/* App Title */}
        <span className="ms-1">| Your Health, On Time</span> {/* Tagline */}
      </div>
      <div className="ms-auto">
        <span className="ms-1">&copy; Ipadeola Michael Bamidele (ALX PORTFOLIO PROJECT 2024).</span>
      </div>
    </CFooter>
  );
};

export default React.memo(AppFooter);
