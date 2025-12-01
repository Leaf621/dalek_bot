import { useEffect, useState } from 'react'
import { Box, Button, Container, Typography, Paper } from '@mui/material'
import { ENDPOINT, getSounds, requestShareSound, type Sound } from './backend/api'
import SendIcon from '@mui/icons-material/Send';
import { sharePreparedMessage, useUserId } from './components/telegram/Telegram';

function Sound(props: {sound: Sound}) {
  const userId = useUserId();

  async function shareSound() {
    let result = await requestShareSound({user_id: userId, identifier: props.sound.identifier});
    sharePreparedMessage(result.message_id);
  }

  return (
    <Paper sx={{ p: 2, mb: 2 }}>
      <audio controls src={`${ENDPOINT}/sounds/${props.sound.identifier}/sound.ogg`} />
      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Typography variant="caption">{props.sound.description}</Typography>
        <Button variant="outlined" endIcon={<SendIcon />} onClick={shareSound}>
          Поделится
        </Button>
      </Box>
    </Paper>
  );
}

function Sounds() {
  let [sounds, setSounds] = useState<Sound[]>([]);

  useEffect(() => {
    async function fetchSounds() {
      let data = await getSounds();
      setSounds(data);
    }
    fetchSounds();
  }, []);

  return (<Box>
    {sounds.map((sound) => (<Sound key={sound.identifier} sound={sound} />))}
  </Box>
  );
}

function App() {
  return (
    <Container maxWidth="sm">
      <Box>
        <Sounds />
      </Box>
    </Container>
  )
}

export default App
