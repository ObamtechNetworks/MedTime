import React, {useRef} from 'react'
import { ThemeProvider } from '@mui/material/styles'
import Navbar from '../../UI/Navbar' // Updated import for Navbar
import MainBanner from '../../UI/MainBanner' // Updated import for MainBanner
import FeaturesSection from '../../UI/FeaturesSection'
import { VectorBackground } from '../../../assets/images-copy'
import theme from '../../../theme' // Import the custom theme

import './index.scss'

const LandingPage = () => {
  // Create the ref for the Features section
  const featuresRef = useRef(null);

  return (
    <ThemeProvider theme={theme}>
      <Navbar featuresRef={featuresRef}/>
      <VectorBackground className="vector-bg" />
      <div className="content">
        <MainBanner />
        
        <FeaturesSection ref={featuresRef} /> {/** think implementation needs to be done here for ref */}
      </div>
    </ThemeProvider>
  )
}

export default LandingPage
