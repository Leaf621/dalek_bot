# __init__.py
from bot.config import bot, dispatcher, app
from bot.routes.v1 import router as v1_router
# Aiogram routers
from bot.antibot import router as antibot_router
from bot.fun import router as fun_router

dispatcher.include_router(antibot_router)
dispatcher.include_router(fun_router)
app.include_router(v1_router)
