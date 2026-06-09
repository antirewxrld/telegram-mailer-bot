from email.mime.text import MIMEText
from pydoc import text
import aiosmtplib

from app.config import *

async def send_reply(to_email, subject, text):

    msg = MIMEText(text, "html")

    msg["From"] = YANDEX_EMAIL
    msg["To"] = to_email
    msg["Subject"] = f"Re: {subject}"

    print("Sending email...")
    print("TO:", repr(to_email))
    print("SUBJECT:", repr(subject))
    print("TEXT:", repr(text))

    await aiosmtplib.send(
        msg,
        hostname="smtp.yandex.ru",
        port=465,
        username=YANDEX_EMAIL,
        password=YANDEX_PASSWORD,
        use_tls=True
    )