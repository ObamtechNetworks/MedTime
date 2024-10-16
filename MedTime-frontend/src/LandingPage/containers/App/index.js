import React from 'react'
import { ThemeProvider } from '@mui/material/styles'
import Navbar from '../../UI/Navbar' // Updated import for Navbar
import MainBanner from '../../UI/MainBanner' // Updated import for MainBanner
import FeaturesSection from '../../UI/FeaturesSection'
import { VectorBackground } from '../../../assets/images-copy'
import theme from '../../../theme' // Import the custom theme

import './index.scss'

const LandingPage = () => {
  return (
    <ThemeProvider theme={theme}>
      <Navbar />
      <VectorBackground className="vector-bg" />
      <div className="content">
        <MainBanner />
        <FeaturesSection />
      </div>
    </ThemeProvider>
  )
}

export default LandingPage
