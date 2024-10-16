// src/theme.js
import { createTheme } from '@mui/material/styles'

const theme = createTheme({
  // Customize your theme properties if needed
  palette: {
    primary: {
      main: '#1976d2', // Example color
    },
    secondary: {
      main: '#dc004e',
    },
  },
  spacing: 8, // Default spacing is 8px
})

export default theme
