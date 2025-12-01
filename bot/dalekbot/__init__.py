# __init__.py
from dalekbot.env import bot, dispatcher, app
from dalekbot.routes.v1 import router as v1_router
# Aiogram routers
from dalekbot.antibot import router as antibot_router
from dalekbot.fun import router as fun_router

dispatcher.include_router(antibot_router)
dispatcher.include_router(fun_router)
app.include_router(v1_router)
