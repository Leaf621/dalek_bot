import { Box, Typography, type Theme } from "@mui/material";
import { useEffect, useState, type ReactNode } from "react";

function Telegram({theme, children}: {theme: Theme, children?: ReactNode}) {
    let [viewportHeight, setViewportHeight] = useState(window.innerHeight);

    useEffect(() => {
        // @ts-ignore
        window.Telegram.WebApp.ready();
        // @ts-ignore
        const platform = window.Telegram.WebApp.platform;
        // @ts-ignore
        window.Telegram.WebApp.setBackgroundColor(theme.palette.background.default);
        // @ts-ignore
        window.Telegram.WebApp.setHeaderColor(theme.palette.background.default);
        // @ts-ignore
        window.Telegram.WebApp.setBottomBarColor(theme.palette.background.default);     
        
        // @ts-ignore
        const onResize = () => {
            // @ts-ignore
            setViewportHeight(window.Telegram.WebApp.viewportHeight);
        };

        // @ts-ignore
        window.Telegram.WebApp.onEvent('contentSafeAreaChanged', onResize);
        return () => {
            // @ts-ignore
            window.Telegram.WebApp.offEvent('viewportChanged', onResize);
        };
    }, [theme]);
    return (
        <Box sx={{height: viewportHeight + 'px', boxSizing: 'border-box', overflow: 'auto'}}>
            {children}
        </Box>
    );
}

export default Telegram;
