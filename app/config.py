from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

YANDEX_EMAIL = os.getenv("YANDEX_EMAIL")
YANDEX_PASSWORD = os.getenv("YANDEX_PASSWORD")

ADMIN_ID = int(os.getenv("ADMIN_ID"))