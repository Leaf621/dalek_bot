from random import choice
import hmac
import hashlib
from urllib.parse import parse_qsl

from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse

from aiogram.types.input_file import FSInputFile
from aiogram.types import InlineQueryResultAudio
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from dalekbot.sounds import SOUNDS
from dalekbot.bot import bot
from dalekbot.settings import settings

from pydantic import BaseModel


class PublicSound(BaseModel):
    identifier: str
    description: str

class SoundShareRequest(BaseModel):
    identifier: str
    user_id: int

class SoundShareResponse(BaseModel):
    success: bool
    message_id: str

router = APIRouter(prefix="/api/v1")

@router.get("/status")
def get_status():
    return {"status": "ok", "version": "1.0"}

@router.get("/sounds")
def list_sounds():
    public_sounds = [
        PublicSound(identifier=sound.identifier, description=sound.description)
        for sound in SOUNDS
    ]
    return public_sounds

@router.get("/sounds/{identifier}/sound.ogg")
def get_sound(identifier: str):
    sound = next((s for s in SOUNDS if s.identifier == identifier), None)
    if sound is None:
        return JSONResponse(status_code=404, content={"detail": "Sound not found"})
    return FileResponse(sound.file_path, media_type="audio/ogg")

def _create_sound_inline_query_result(sound: PublicSound, username: str) -> InlineQueryResultAudio:
    keyboard = None
    if choice([True, True, False]): # 2/3 chance to add
        keyboard = InlineKeyboardBuilder([[
            InlineKeyboardButton(
                text="Попробуйте в приложении",
                url=f'https://t.me/{username}?startapp'
            )
        ]])
    return InlineQueryResultAudio(
        id=sound.identifier,
        audio_url=f"{settings.BASE_URL}api/v1/sounds/{sound.identifier}/sound.ogg",
        title=sound.description,
        reply_markup=keyboard.as_markup() if keyboard else None,
    )

@router.post("/sounds/share")
async def share_sound(request: SoundShareRequest) -> SoundShareResponse:
    sound = next((s for s in SOUNDS if s.identifier == request.identifier), None)
    if sound is None:
        return JSONResponse(status_code=404, content={"detail": "Sound not found"})
    me = await bot.get_me()
    prepared_message = await bot.save_prepared_inline_message(
        request.user_id,
        result=_create_sound_inline_query_result(
            PublicSound(identifier=sound.identifier, description=sound.description),
            me.username
        ),
        allow_bot_chats=True,
        allow_group_chats=True,
        allow_channel_chats=True,
        allow_user_chats=True,
    )
    return SoundShareResponse(success=True, message_id=prepared_message.id)

class TelegramAuthRequest(BaseModel):
    init_data: str

@router.post("/auth/telegram")
async def telegram_auth(request: TelegramAuthRequest):
    params = dict(parse_qsl(request.init_data))
    check_string = '\n'.join(f"{k}={v}" for k, v in sorted(params.items()) if k != 'hash')
    secret_key = hmac.new(b'WebAppData', bot.token.encode(), hashlib.sha256).digest()
    computed_hash = hmac.new(secret_key, check_string.encode(), hashlib.sha256).hexdigest()
    if computed_hash != params.get('hash'):
        return JSONResponse(status_code=403, content={"detail": "Invalid data"})
    return {"status": "ok"}
