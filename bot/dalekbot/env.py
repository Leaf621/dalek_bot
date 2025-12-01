from os import getenv

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.formatting import Text, TextLink

from fastapi import FastAPI

# Load .env file and get BOT_TOKEN variable
load_dotenv()
TOKEN = getenv("BOT_TOKEN")
BASE_URL = getenv("BASE_URL")

# All handlers should be attached to the Router (or Dispatcher)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dispatcher = Dispatcher()
app = FastAPI()

@dispatcher.message(CommandStart())
async def start_command_handler(message: Message) -> None:
    text = Text(
        "Привет! Я бот, созданный специально для чата ", TextLink("Чат фанатов «Доктор Кто»", url="https://t.me/chat_fanatov"), ".\n",
        "Исходный код доступен на ", TextLink("GitHub", url="https://github.com/Leaf621/dalek_bot"), ".\n",
    )
    await message.answer(**text.as_kwargs())
