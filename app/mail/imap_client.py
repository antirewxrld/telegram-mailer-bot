import asyncio
import imaplib
import email
import logging
import traceback

from aiogram import Bot

from email.utils import parseaddr
from html import escape

from app.config import *
from app.bot.keyboards.mail_keyboard import reply_keyboard

logging.basicConfig(level=logging.INFO)


async def start_listener(bot: Bot):

    logging.info("IMAP listener started")

    while True:

        try:
            mail = imaplib.IMAP4_SSL("imap.yandex.ru")

            mail.login(
                YANDEX_EMAIL,
                YANDEX_PASSWORD
            )

            logging.info("Logged into IMAP")

            mail.select("INBOX")

            status, messages = mail.search(
                None,
                "UNSEEN"
            )

            logging.info(f"Found messages: {messages}")

            if not messages or not messages[0]:
                mail.logout()
                await asyncio.sleep(10)
                continue

            for num in messages[0].split():

                _, data = mail.fetch(num, "(RFC822)")
                raw_email = data[0][1]

                msg = email.message_from_bytes(raw_email)

                # ─────────────────────────────
                # RAW FIELDS
                # ─────────────────────────────
                raw_sender = msg.get("From", "")
                raw_subject = msg.get("Subject", "")

                sender_name, sender_email = parseaddr(raw_sender)
                sender_email = sender_email.strip()

                subject = raw_subject or ""

                # ─────────────────────────────
                # BODY PARSING
                # ─────────────────────────────
                text = ""

                try:
                    if msg.is_multipart():

                        for part in msg.walk():

                            if part.get_content_type() == "text/plain":

                                payload = part.get_payload(decode=True)

                                if payload:
                                    text = payload.decode(errors="ignore")

                                break
                    else:
                        payload = msg.get_payload(decode=True)

                        if payload:
                            text = payload.decode(errors="ignore")

                except Exception:
                    text = ""

                # ─────────────────────────────
                # SAFE TRIM
                # ─────────────────────────────
                text = text[:3000]

                # ─────────────────────────────
                # ESCAPE FOR TELEGRAM HTML
                # ─────────────────────────────
                sender_name = escape(sender_name or "")
                sender_email = escape(sender_email or "")
                subject = escape(subject or "")
                text = escape(text or "")

                # ─────────────────────────────
                # VALIDATION
                # ─────────────────────────────
                if not sender_email:
                    logging.warning(f"Skip email, empty sender: {raw_sender}")
                    continue

                # ─────────────────────────────
                # SEND TO TELEGRAM
                # ─────────────────────────────
                await bot.send_message(
                    ADMIN_ID,
                    f"📩 <b>Новое письмо</b>\n\n"
                    f"<b>От:</b> {sender_name} ({sender_email})\n"
                    f"<b>Тема:</b> {subject}\n\n"
                    f"{text}",
                    reply_markup=reply_keyboard(
                        sender_email,
                        subject
                    )
                )

            mail.logout()

        except Exception:
            traceback.print_exc()

        await asyncio.sleep(10)