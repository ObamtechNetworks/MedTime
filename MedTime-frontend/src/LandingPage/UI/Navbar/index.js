import React from 'react'
import { makeStyles } from '@mui/styles'
import AppBar from '@mui/material/AppBar'
import Toolbar from '@mui/material/Toolbar'
import Button from '@mui/material/Button'
import { Link } from 'react-router-dom'
import MoreButton from '../MoreButton'
import { Logo } from '../../../assets/images-copy'
import { useMediaQuery } from 'react-responsive'
import { v4 as uuidv4 } from 'uuid' //to generate key values

import FeaturesSection from '../FeaturesSection'; // Import the FeaturesSection

import './index.scss'

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
}))

const Navbar = ({ featuresRef }) => {
  const classes = useStyles()

  const isTabletOrMobile = useMediaQuery({ maxWidth: 980 })

  // Scroll to features when "Features" is clicked
  const handleFeaturesClick = () => {
    if (featuresRef.current) {
      featuresRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };

  // array that holds navigation menu items
  const navMenuItems = ['About Us', 'Features', 'Contact']

  return (
    <div className={classes.root}>
      <AppBar position="static" className="appbar-wrapper">
        <Toolbar>
          <div className="logo-wrapper">
            <Logo />
          </div>
          {!isTabletOrMobile && (
            <>
              {navMenuItems.map((item) => (
                <Button key={uuidv4()} onClick={item === 'Features' ? handleFeaturesClick : null}>{item}</Button>
              ))}
            </>
          )}

          {/* Add Login and Register buttons here */}
          <Link to="/login">
            <Button className="login-btn">Login</Button>
          </Link>
          <Link to="/register">
            <Button className="register-btn">Register</Button>
          </Link>

          <Button className="isMobile selected">Try now</Button>

          {isTabletOrMobile && <MoreButton menuItems={navMenuItems} btnCls="isMobile" />}
        </Toolbar>
      </AppBar>
    </div>
  )
}

export default Navbar
