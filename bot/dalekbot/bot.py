from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.formatting import Text, TextLink

from dalekbot.settings import settings
from dalekbot.antibot import router as antibot_router
from dalekbot.fun import router as fun_router

# All handlers should be attached to the Router (or Dispatcher)
bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dispatcher = Dispatcher()

@dispatcher.message(CommandStart())
async def start_command_handler(message: Message) -> None:
    text = Text(
        "Привет! Я бот, созданный специально для чата ", TextLink("Чат фанатов «Доктор Кто»", url="https://t.me/chat_fanatov"), ".\n",
        "Исходный код доступен на ", TextLink("GitHub", url="https://github.com/Leaf621/dalek_bot"), ".\n",
    )
    await message.answer(**text.as_kwargs())

dispatcher.include_router(antibot_router)
dispatcher.include_router(fun_router)
