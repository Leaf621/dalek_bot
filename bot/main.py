import asyncio
import logging
import sys
from os import getenv

from dotenv import load_dotenv
from uvicorn import Config, Server

from bot import bot, dispatcher, app

# Register routers
# FastAPI routers
from routes.v1 import router as v1_router
# Aiogram routers
from antibot import router as antibot_router
from fun import router as fun_router

dispatcher.include_router(antibot_router)
dispatcher.include_router(fun_router)

app.include_router(v1_router)

async def run_app() -> None:
    config = Config(app=app, host="0.0.0.0", port=8000)
    server = Server(config=config)
    await server.serve()

async def main() -> None:
    app_task = asyncio.create_task(run_app())
    bot_task = asyncio.create_task(dispatcher.start_polling(bot))
    await asyncio.gather(app_task, bot_task)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())