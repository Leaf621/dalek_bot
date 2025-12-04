import { Box, type Theme } from "@mui/material";
import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { authenticateTelegram } from "../../backend/api";

export interface TelegramContextProps {
    userId: number;
    imageUrl: string | null;
    firstName: string;
}

const TelegramContext = createContext<TelegramContextProps | undefined>(undefined);

function Telegram({theme, children, fallback}: {theme: Theme, children?: ReactNode, fallback?: ReactNode}) {
    let [viewportHeight, setViewportHeight] = useState(window.innerHeight);
    let [loading, setLoading] = useState(true);

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

        async function authenticate() {
            // @ts-ignore
            const initData = window.Telegram.WebApp.initData;
            await authenticateTelegram(initData);
            setLoading(false);
        }

        authenticate();

        // @ts-ignore
        window.Telegram.WebApp.onEvent('contentSafeAreaChanged', onResize);
        return () => {
            // @ts-ignore
            window.Telegram.WebApp.offEvent('viewportChanged', onResize);
        };
    }, [theme]);

    const telegramContextValue: TelegramContextProps = {
        // @ts-ignore
        userId: window.Telegram.WebApp.initDataUnsafe.user.id,
        // @ts-ignore
        imageUrl: window.Telegram.WebApp.initDataUnsafe.user.photo_url,
        // @ts-ignore
        firstName: window.Telegram.WebApp.initDataUnsafe.user.first_name,
    };

    return (
        <TelegramContext.Provider value={telegramContextValue}>
            <Box sx={{height: viewportHeight + 'px', boxSizing: 'border-box', overflow: 'auto'}}>
                {loading ? (fallback) : children}
            </Box>    
        </TelegramContext.Provider>
    );
}

export function useTelegramContext() {
    const context = useContext(TelegramContext);
    if (!context) {
        throw new Error("useTelegramContext must be used within a TelegramProvider");
    }
    return context;
}


export function sharePreparedMessage(message_id: string, callback: ((nice: boolean) => void) | null = null) {
    // @ts-ignore
    window.Telegram.WebApp.shareMessage(message_id, callback);
}

export function closeWebApp() {
    // @ts-ignore
    window.Telegram.WebApp.close();
}

export default Telegram;
