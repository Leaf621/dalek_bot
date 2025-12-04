import { Avatar, Stack, Typography } from "@mui/material";
import { useTelegramContext } from "./telegram/Telegram";

function ProfileNav() {
    const telegramContext = useTelegramContext();
    return (
        <Stack sx={{ p: 2 }} direction="row" alignItems="center" justifyContent="end" spacing={1}>
            <Typography variant="body1">{telegramContext.firstName}</Typography>
            { telegramContext.imageUrl && 
                <Avatar src={telegramContext.imageUrl} sx={{ width: 32, height: 32 }} />
            }
        </Stack>
    );
}

export default ProfileNav;