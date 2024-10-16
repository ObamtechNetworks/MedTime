import React from 'react'
import { useMediaQuery } from 'react-responsive'
import { MainBannerDescImage, MainBannerDescImageSmall } from '../../../assets/images-copy'
import { Link } from 'react-router-dom'

import './index.scss'

function MainBannerContent() {
  const isMobile = useMediaQuery({ maxWidth: 478 })

  return (
    <div className="mainbanner-content-wrapper">
      <div className="mainbanner-content">
        <div className="desc-img-wrapper">
          {isMobile ? (
            <MainBannerDescImageSmall width="100%" />
          ) : (
            <MainBannerDescImage width="100%" />
          )}
        </div>
        <div className="text-wrapper">
          <p>
            Welcome to <strong>MedTime</strong>—your personal drug reminder and scheduling assistant! MedTime helps you stay consistent with your medication regimen through easy-to-set reminders and customizable schedules. 
          </p>
          <p>
            Never miss a dose again; take control of your health with confidence. Whether you're managing chronic conditions or daily vitamins, MedTime is here to support your journey to better health.
          </p>
        </div>
        <div className="button-wrapper">
          <Link to="/login"><button className="mainbanner-button">Try Now</button></Link> {/* Updated Link */}
        </div>
      </div>
    </div>
  )
}

export default MainBannerContent
