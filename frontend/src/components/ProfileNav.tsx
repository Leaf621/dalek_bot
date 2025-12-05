import { Avatar, Skeleton, Stack, Typography } from "@mui/material";
import { useEffect, useState } from "react";
import { useTelegramContext } from "./telegram/Telegram";

type AvatarStatus = "idle" | "loading" | "loaded" | "error";

function ProfileNav() {
    const { firstName, imageUrl } = useTelegramContext();
    const [status, setStatus] = useState<AvatarStatus>("idle");

    useEffect(() => {
        if (!imageUrl) {
            setStatus("idle");
            return;
        }

        setStatus("loading");
        const img = new Image();
        // Decode before showing to avoid progressive fade-in while rendering
        img.decoding = "async";
        img.src = imageUrl;
        let cancelled = false;

        img.onload = () => {
            const finish = () => {
                if (!cancelled) {
                    setStatus("loaded");
                }
            };

            // Prefer decode() so the avatar swaps only after the image is fully ready
            if (typeof img.decode === "function") {
                img.decode().then(finish).catch(finish);
            } else {
                finish();
            }
        };
        img.onerror = () => {
            if (!cancelled) {
                setStatus("error");
            }
        };

        return () => {
            cancelled = true;
        };
    }, [imageUrl]);

    const showSkeleton = Boolean(imageUrl) && status === "loading";
    const showAvatar = Boolean(imageUrl) && status === "loaded";
    const showFallback = !imageUrl || status === "idle" || status === "error";
    const initial = firstName?.charAt(0) || "?";

    return (
        <Stack sx={{ p: 2 }} direction="row" alignItems="center" justifyContent="end" spacing={1}>
            <Typography variant="body1">{firstName}</Typography>
            {showSkeleton && <Skeleton variant="circular" width={32} height={32} />}
            {showAvatar && (
                <Avatar src={imageUrl ?? undefined} sx={{ width: 32, height: 32 }} />
            )}
            {showFallback && (
                <Avatar sx={{ width: 32, height: 32 }}>
                    {initial}
                </Avatar>
            )}
        </Stack>
    );
}

export default ProfileNav;