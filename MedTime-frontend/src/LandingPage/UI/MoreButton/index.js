import React, { useState } from 'react'
import PropTypes from 'prop-types'
import Button from '@mui/material/Button'
import Menu from '@mui/material/Menu'
import MenuItem from '@mui/material/MenuItem'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faBars } from '@fortawesome/free-solid-svg-icons'
import { v4 as uuidv4 } from 'uuid' //to generate keys

import './index.scss'

const MoreButton = ({ btnCls, menuItems }) => {
  const [anchorEl, setAnchorEl] = useState(null)

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget)
  }

  const handleClose = () => {
    setAnchorEl(null)
  }

  return (
    <div>
      <Button
        className={`${btnCls} more-btn`}
        aria-controls="simple-menu"
        aria-haspopup="true"
        onClick={handleClick}
        style={{ padding: 5, width: 15 }}
      >
        <FontAwesomeIcon icon={faBars} size="lg" />
      </Button>
      <Menu
        className="more-btn-menu"
        anchorEl={anchorEl}
        keepMounted
        open={Boolean(anchorEl)}
        onClose={handleClose}
      >
        {menuItems.map((item) => (
          <MenuItem key={uuidv4()} onClick={handleClose}>
            {item}
          </MenuItem>
        ))}
      </Menu>
    </div>
  )
}

MoreButton.defaultProps = {
  btnCls: '',
}

MoreButton.propTypes = {
  btnCls: PropTypes.string,
  menuItems: PropTypes.arrayOf(PropTypes.string).isRequired,
}

export default MoreButton
