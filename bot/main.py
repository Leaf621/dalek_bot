import asyncio
import logging
import sys

from uvicorn import Config, Server

from bot import bot, app, dispatcher

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