from dataclasses import dataclass

from aiogram import Router
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.types import (
    Message,
    InlineKeyboardMarkup
)
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.input_file import FSInputFile


router = Router()

@router.message(Command('exterminate'))
async def exterminate_command_handler(message: Message) -> None:
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_VOICE)
    uwu_mode = message.text.split()
    if len(uwu_mode) > 1 and uwu_mode[1].lower() == 'uwu':
        await message.reply_voice(FSInputFile('data/sounds/uwu.ogg'), caption='(づ｡◕‿‿◕｡)づ')
    else:
        await message.reply_voice(FSInputFile('data/sounds/exterminate.ogg'))

@router.message(Command('sounds'))
async def sounds_command_handler(message: Message) -> None:
    me = await message.bot.get_me()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Открыть', url=f'https://t.me/{me.username}?startapp')],
    ])
    await message.answer("Попробуйте наше новое приложение", reply_markup=keyboard)