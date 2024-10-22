import React, { Suspense } from 'react'
import { Navigate, Route, Routes } from 'react-router-dom'
import { CContainer, CSpinner } from '@coreui/react'
import { useAuth } from '../api/authContext'

// routes config
import routes from '../routes'

const AppContent = () => {
  const { isAuthenticated, loading } = useAuth(); // Use the auth context

  if (loading) {
    // Show a spinner or loading component while loading
    return (
      <CContainer className="px-4" lg>
        <CSpinner color="primary" />
      </CContainer>
    );
  }

  return (
    <CContainer className="px-4" lg>
      <Suspense fallback={<CSpinner color="primary" />}>
        <Routes>
          {routes.map((route, idx) => {
            return (
              route.element && (
                <Route
                  key={idx}
                  path={route.path}
                  exact={route.exact}
                  name={route.name}
                  element={isAuthenticated ? <route.element /> : <Navigate to="/login" replace />} // Check authentication
                />
              )
            )
          })}
          <Route path="/" element={<Navigate to="dashboard" replace />} />
          <Route path="*" element={<Navigate to="/404" />} /> {/* Handle unknown paths */}
        </Routes>
      </Suspense>
    </CContainer>
  );
};

export default React.memo(AppContent);
