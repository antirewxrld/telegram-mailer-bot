import asyncio

from aiogram import Bot
from aiogram import Dispatcher

from app.config import *

from app.bot.handlers.reply import router
from app.mail.imap_client import start_listener

bot = Bot(
    BOT_TOKEN,
    parse_mode="HTML"
)

dp = Dispatcher()

dp.include_router(router)

async def main():

    asyncio.create_task(
        start_listener(bot)
    )

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())