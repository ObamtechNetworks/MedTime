import React, { forwardRef } from 'react'
import { makeStyles } from '@mui/styles'
import Paper from '@mui/material/Paper'
import Grid from '@mui/material/Grid'
import FeatureCard from '../FeatureCard'
import { IntegrationIcon, MethodsIcon, SupportIcon } from '../../../assets/images-copy'
import { Link } from 'react-router-dom'

import './index.scss'

// overriding and customizing the @material-ui/core component's style
const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    width: '100%',
  },
  row: {
    width: '100%',
    margin: 0,
  },
  paper: {
    padding: theme.spacing(2),
    textAlign: 'left',
    boxShadow: 'none',
    borderRadius: 22,
    minWidth: 110,
    border: 'none',
    '&:hover': {
      transition: '300ms',
      filter: 'drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.25))',
    },
    '@media screen and (max-width: 478px)': {
      border: '1px solid #EBF2FA',
      textAlign: 'center',
    },
  },
}))

const FeaturesSection = forwardRef((props, ref) => {
  const classes = useStyles();

  return (
    <div ref={ref} className="featuresection-wrapper">
      <div className="featuresection-title">Main Features</div>
      <div className="featuresection-subtitle">
        Discover how MedTime can transform your medication management experience.
        Stay on track with your health goals through our easy-to-use approach.
      </div>
      <div className="features-cols">
        <Grid container spacing={5} className={classes.row}>
          <Grid item xs={12} sm={4}>
            <Paper className={classes.paper}>
              <FeatureCard
                icon={{ icon: <IntegrationIcon />, bgColor: '#EFECF9' }}
                title="Create Drug Schedule"
              >
                Effortlessly set up a personalized drug schedule with daily reminders, so you never miss a dose. Our intuitive interface makes it easy to add or adjust your medications.
              </FeatureCard>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Paper
              style={{
                boxShadow: '0px 70px 106px rgba(60, 52, 81, 0.12)',
                border: 'none',
              }}
              className={classes.paper}
            >
              <FeatureCard
                icon={{ icon: <MethodsIcon />, bgColor: '#FFEDED' }}
                title="Register Drug Prescription"
              >
                Keep your prescriptions organized in one place. Add medication details, dosage instructions, and mark priority drugs for isolation, ensuring you stay on top of your regimen.
              </FeatureCard>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Paper className={classes.paper}>
              <FeatureCard
                icon={{ icon: <SupportIcon />, bgColor: '#FFF7EE' }}
                title="Start the Schedule"
              >
                Choose to start your medication plan immediately or at a later date. Customize your schedule to fit your routine and let MedTime handle the reminders.
              </FeatureCard>
            </Paper>
          </Grid>
        </Grid>
      </div>
      <div className="featuresection-button-wrapper">
        <Link to="/login"><button className="featuresection-button">Try Now</button></Link>
      </div>
    </div>
  );
});


export default FeaturesSection
