import React from 'react'
import PropTypes from 'prop-types'

import './index.scss'

function FeatureCard({ title, icon, children }) {
  return (
    <div className="feature-card">
      {icon && (
        <div className="feature-card-icon" style={{ backgroundColor: icon.bgColor }}>
          {icon.icon}
        </div>
      )}

      <div className="feature-card-title">{title}</div>
      <div className="feature-card-desc">{children}</div>
    </div>
  )
}

FeatureCard.defaultProps = {
  icon: null,
}

FeatureCard.propTypes = {
  title: PropTypes.string.isRequired,
  icon: PropTypes.object,
  children: PropTypes.any.isRequired,
}

export default FeatureCard
