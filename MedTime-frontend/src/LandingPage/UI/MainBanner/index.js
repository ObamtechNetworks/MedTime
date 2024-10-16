import React from 'react'
import { makeStyles } from '@mui/styles'
import Paper from '@mui/material/Paper'
import Grid from '@mui/material/Grid'

import MainBannerImg from '../MainBannerImg'
import MainBannerContent from '../MainBannerContent'
import './index.scss'

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    height: '100%',
  },
  paper: {
    backgroundColor: 'transparent',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    padding: theme.spacing(2),
    textAlign: 'center',
    color: theme.palette.text.secondary,
    boxShadow: 'none',
    height: '100%',
    '@media screen and (max-width:900px)': {
      alignItems: 'start',
    },
  },
  row: {
    height: '100%',
  },
}))

const MainBanner = () => {
  const classes = useStyles()

  return (
    <div className="mainbanner-wrapper">
      <div className={classes.root}>
        <Grid container spacing={3} className={classes.row}>
          <Grid item xs={12} sm={6}>
            <Paper className={classes.paper}>
              <MainBannerContent />
            </Paper>
          </Grid>
          <Grid className="isMobile" item xs={6} sm={6}>
            <Paper className={classes.paper}>
              <MainBannerImg />
            </Paper>
          </Grid>
        </Grid>
      </div>
    </div>
  )
}

export default MainBanner
