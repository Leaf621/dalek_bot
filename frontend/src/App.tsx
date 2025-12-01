import { useState } from 'react'
import { Box, Button, Container, Typography } from '@mui/material'

function ShareMessage() {
  let [progress, setProgress] = useState(false)

  async function sendMessage() {
    setProgress(true);
    // @ts-ignore
    let userId = window.Telegram.WebApp.initDataUnsafe.user.id;
    let response = await fetch(`/api/share?user_id=${userId}`, {
      method: 'POST',
    });
    let data = await response.json();
    if (!data.status) {
      alert("Failed to send message: " + data.error);
    }
    let messageId = data.prepared_message_id;
    // @ts-ignore
    window.Telegram.WebApp.shareMessage(messageId);
    setProgress(false);
  }

  return (
    <Button onClick={sendMessage} disabled={progress} variant="contained" color="primary">
      Send Something
    </Button>
  )
}

function App() {
  const [count, setCount] = useState(0)

  return (
    <Container maxWidth="sm">
      <Box>
        <Typography variant="h4" component="h1" gutterBottom>
          Test App
        </Typography>
        <ShareMessage />
      </Box>
    </Container>
  )
}

export default App
