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

from fastapi import FastAPI
from fastapi.params import Query
from uvicorn import Config, Server

from antibot import router as antibot_router
from fun import router as fun_router

# Load .env file and get BOT_TOKEN variable
load_dotenv()
TOKEN = getenv("BOT_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
app = FastAPI()

dp.include_router(antibot_router)
dp.include_router(fun_router)

@dp.message(CommandStart())
async def start_command_handler(message: Message) -> None:
    text = Text(
        "Привет! Я бот, созданный специально для чата ", TextLink("Чат фанатов «Доктор Кто»", url="https://t.me/chat_fanatov"), ".\n",
        "Исходный код доступен на ", TextLink("GitHub", url="https://github.com/Leaf621/dalek_bot"), ".\n",
    )
    await message.answer(**text.as_kwargs())

from aiogram.types import InlineQueryResultArticle, InputTextMessageContent

@app.post("/api/share")
async def prepare_message(user_id: int = Query(...)) -> dict:
    d = await bot.save_prepared_inline_message(
        user_id=user_id, 
        result=InlineQueryResultArticle(
            id="1",
            title="Prepared Message",
            input_message_content=InputTextMessageContent(
                message_text="This is a prepared inline message!"
            ),
        ),
        allow_bot_chats=True,
        allow_group_chats=True,
        allow_user_chats=True,
        allow_channel_chats=True,
    )
    return {"status": "Message prepared", "prepared_message_id": d.id}

async def run_app() -> None:
    config = Config(app=app, host="0.0.0.0", port=8000)
    server = Server(config=config)
    await server.serve()

async def main() -> None:
    app_task = asyncio.create_task(run_app())
    bot_task = asyncio.create_task(dp.start_polling(bot))
    await asyncio.gather(app_task, bot_task)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())