import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from app.config import *

from app.bot.handlers.reply import router
from app.bot.handlers.start import router as start_router
from app.bot.handlers.reply import router as reply_router
from app.mail.imap_client import start_listener

logging.basicConfig(
    level=logging.INFO
)

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode="HTML"
    )
)

dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(reply_router)

async def main():

    logging.info("Bot starting...")

    asyncio.create_task(
        start_listener(bot)
    )

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())