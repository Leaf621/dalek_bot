import asyncio
import logging
import sys
from os import getenv

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.formatting import Text, TextLink

from antibot import router as antibot_router

# Load .env file and get BOT_TOKEN variable
load_dotenv()
TOKEN = getenv("BOT_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

dp.include_router(antibot_router)

@dp.message(CommandStart())
async def start_command_handler(message: Message) -> None:
    text = Text(
        "Привет! Я бот, созданный специально для чата ", TextLink("Чат фанатов «Доктор Кто»", url="https://t.me/chat_fanatov"), ".\n",
        "Исходный код доступен на ", TextLink("GitHub", url="https://github.com/Leaf621/dalek_bot"), ".\n",
    )
    await message.answer(**text.as_kwargs())

async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())