import asyncio
import random
from dataclasses import dataclass
from typing import Union

from aiogram import Router
from aiogram.enums import ChatMemberStatus, ChatAction, ParseMode
from aiogram.filters import Command
from aiogram.types import (
    ChatMemberUpdated,
    Message,
    User,
    InlineQuery,
    InlineQueryResultVoice,
    InputTextMessageContent,
    ChosenInlineResult,
    InlineKeyboardMarkup
)
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
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

@router.inline_query()
async def inline_query_handler(inline_query: InlineQuery) -> None:
    query = inline_query.query.split()
    results = []
    if len(query) == 0:
        results.append(InlineQueryResultVoice(
            id='exterminate',
            title='УНИЧТОЖИТЬ!',
            voice_url='https://media.githubusercontent.com/media/Leaf621/dalek_bot/refs/heads/main/data/exterminate.ogg',
            description='Крик далека',
        ))
    if len(query) == 1 and query[0].lower() == 'uwu':
        results.append(InlineQueryResultVoice(
            id='exterminate_uwu',
            title='УНИЧТОЖИТЬ! (uwu mode)',
            voice_url='https://media.githubusercontent.com/media/Leaf621/dalek_bot/refs/heads/main/data/uwu.ogg',
            description='Крик далека в режиме uwu',
        ))
    await inline_query.answer(results=results, cache_time=1, is_personal=True)
