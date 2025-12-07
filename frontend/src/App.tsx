import { useEffect, useRef, useState } from 'react'
import { Box, Button, Container, Typography, Paper, Slider, Stack, Skeleton, CircularProgress } from '@mui/material'
import { ENDPOINT, getSounds, requestShareSound, type Sound } from './backend/api'
import { closeWebApp, sharePreparedMessage, useTelegramContext } from './components/telegram/Telegram';
import { PlayArrow, Share, VolumeDown, VolumeUp } from '@mui/icons-material';
import ProfileNav from './components/ProfileNav';

function Sound(props: {sound: Sound, volume: number}) {
  const telegramContext = useTelegramContext();
  const [loading, setLoading] = useState(false);
  const [playing, setPlaying] = useState(false);

  const audio = useRef<HTMLAudioElement>(new Audio());

  useEffect(() => {
    audio.current.volume = props.volume / 100;
  }, [props.volume]);

  audio.current.onloadstart = () => {
    setLoading(true);
  };

  audio.current.oncanplaythrough = () => {
    setLoading(false);
    setPlaying(true);
  };

  audio.current.onended = () => {
    setPlaying(false);
  };

  async function play() {
    audio.current.src = `${ENDPOINT}/sounds/${props.sound.identifier}/sound.ogg`;
    await audio.current.play();
  }

  async function shareSound() {
    let result = await requestShareSound({user_id: telegramContext.userId, identifier: props.sound.identifier});
    sharePreparedMessage(result.message_id, (nice) => {
      if (nice) {
        closeWebApp();
      }
    });
  }

  return (
    <Paper sx={{ p: 2, mb: 2 }}>
      <Stack direction="row" spacing={2} alignItems="center">
        <Box sx={{ flexGrow: 1 }}>
          <Typography variant="body1">{props.sound.description}</Typography>
          <Typography variant="caption">ID: {props.sound.identifier}</Typography>
        </Box>
        <Button variant="outlined" onClick={play} disabled={loading || playing}>
          {!loading ? <PlayArrow /> : <CircularProgress size={24} />}
        </Button>
        <Button variant="outlined" onClick={shareSound}>
          <Share />
        </Button>
      </Stack>
    </Paper>
  );
}

function SoundSkeleton() {
  return (
    <Paper sx={{ p: 2, mb: 2 }}>
      <Stack direction="row" spacing={2} alignItems="center">
        <Skeleton variant="rectangular" height={40} sx={{ flexGrow: 1 }} />
        <Skeleton variant="rectangular" width={60} height={40} />
        <Skeleton variant="rectangular" width={60} height={40} />
      </Stack>
    </Paper>
  )
}

function Sounds() {
  let [sounds, setSounds] = useState<Sound[]>([]);
  let [volume, setVolume] = useState(30);
  let [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchSounds() {
      let data = await getSounds();
      setSounds(data);
      setLoading(false);
    }
    fetchSounds();
  }, []);

  return (
    <Box>
    <Stack spacing={2} direction="row" sx={{ alignItems: 'center', mb: 1 }}>
      <VolumeDown />
      <Slider aria-label="Volume" value={volume} onChange={(_, v) => setVolume(v)} />
      <VolumeUp />
    </Stack>
    <Stack spacing={2}>
      {sounds.map((sound) => (<Sound key={sound.identifier} sound={sound} volume={volume} />))}
      {loading && Array.from({length: 5}).map((_, idx) => (<SoundSkeleton key={idx} />))}
    </Stack>
    </Box>
  );
}

function App() {
  return (
    <Stack>
      <ProfileNav />
      <Container maxWidth="sm">
        <Sounds />
      </Container>
    </Stack>
  )
}

export default App
