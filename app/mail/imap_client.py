import asyncio
import imaplib
import email

from aiogram import Bot

from app.config import *
from app.bot.keyboards.mail_keyboard import reply_keyboard

async def start_listener(bot: Bot):

    while True:

        try:
            mail = imaplib.IMAP4_SSL("imap.yandex.ru")

            mail.login(
                YANDEX_EMAIL,
                YANDEX_PASSWORD
            )

            mail.select("INBOX")

            status, messages = mail.search(
                None,
                "UNSEEN"
            )

            for num in messages[0].split():

                _, data = mail.fetch(
                    num,
                    "(RFC822)"
                )

                raw_email = data[0][1]

                msg = email.message_from_bytes(
                    raw_email
                )

                sender = msg["From"]
                subject = msg["Subject"]

                text = ""

                if msg.is_multipart():

                    for part in msg.walk():

                        content_type = part.get_content_type()

                        if content_type == "text/plain":

                            text = part.get_payload(
                                decode=True
                            ).decode()

                            break
                else:

                    text = msg.get_payload(
                        decode=True
                    ).decode()

                await bot.send_message(
                    ADMIN_ID,
                    f"📩 <b>Новое письмо</b>\n\n"
                    f"<b>От:</b> {sender}\n"
                    f"<b>Тема:</b> {subject}\n\n"
                    f"{text[:3000]}",
                    reply_markup=reply_keyboard(1)
                )

            mail.logout()

        except Exception as e:
            print(e)

        await asyncio.sleep(10)