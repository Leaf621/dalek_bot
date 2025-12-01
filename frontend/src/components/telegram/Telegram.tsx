import { Box, Typography, type Theme } from "@mui/material";
import { useEffect, useState, type ReactNode } from "react";

function Telegram({theme, children}: {theme: Theme, children?: ReactNode}) {
    let [safeAreaInset, setSafeAreaInset] = useState({top:0, bottom:0, left:0, right:0});
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
        
        if (platform === 'ios' || platform === 'android') {
            // @ts-ignore
            window.Telegram.WebApp.requestFullscreen();
        }

        // @ts-ignore
        const onResize = () => {
            // @ts-ignore
            const inset = window.Telegram.WebApp.contentSafeAreaInset;
            setSafeAreaInset(inset);
            // @ts-ignore
            setViewportHeight(window.Telegram.WebApp.viewportHeight);
        };

        onResize();

        // @ts-ignore
        window.Telegram.WebApp.onEvent('contentSafeAreaChanged', onResize);
        // @ts-ignore
        window.Telegram.WebApp.onEvent('viewportChanged', onResize);
        return () => {
            // @ts-ignore
            window.Telegram.WebApp.offEvent('contentSafeAreaChanged', onResize);
            // @ts-ignore
            window.Telegram.WebApp.offEvent('viewportChanged', onResize);
        };
    }, [theme]);
    return (
        <Box sx={{paddingTop: safeAreaInset.top + 'px', paddingBottom: safeAreaInset.bottom + 'px', paddingLeft: safeAreaInset.left + 'px', paddingRight: safeAreaInset.right + 'px', height: viewportHeight - safeAreaInset.bottom - safeAreaInset.top  + 'px', boxSizing: 'border-box', overflow: 'auto'}}>
            {children}
        </Box>
    );
}

export default Telegram;
