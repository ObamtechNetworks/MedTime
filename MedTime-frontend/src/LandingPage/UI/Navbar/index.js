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

import './index.scss'

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
}))

const Navbar = () => {
  const classes = useStyles()

  const isTabletOrMobile = useMediaQuery({ maxWidth: 980 })

  // array that holds navigation menu items
  const navMenuItems = ['About Us', 'How it Works', 'Integrations', 'Contact']

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
                <Button key={uuidv4()}>{item}</Button>
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
