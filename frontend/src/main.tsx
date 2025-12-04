import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { Box, CircularProgress, createTheme, CssBaseline, ThemeProvider } from '@mui/material'
import Telegram from './components/telegram/Telegram.tsx'

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

function Loading() {
  return (
    <Box sx={{ height: '100vh', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
      <CircularProgress />
    </Box>
  );
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Telegram theme={darkTheme} fallback={<Loading />}>
        <App />
      </Telegram>
    </ThemeProvider>
  </StrictMode>,
);
