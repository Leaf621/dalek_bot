import asyncio
import random
from dataclasses import dataclass
from typing import Union

from aiogram import Router
from aiogram.enums import ChatMemberStatus, ChatAction
from aiogram.filters import Command
from aiogram.types import ChatMemberUpdated, Message, User
from aiogram.types.input_file import FSInputFile
from aiogram.utils.formatting import Bold, Text, TextMention

from captcha.image import ImageCaptcha


router = Router()

@router.message(Command('exterminate'))
async def exterminate_command_handler(message: Message) -> None:
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_VOICE)
    uwu_mode = message.text.split()
    if len(uwu_mode) > 1 and uwu_mode[1].lower() == 'uwu':
        await message.reply_voice(FSInputFile('data/uwu.ogg'), caption='(づ｡◕‿‿◕｡)づ')
    else:
        await message.reply_voice(FSInputFile('data/exterminate.ogg'))