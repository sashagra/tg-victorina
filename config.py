import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ROOT = int(os.getenv('ROOT'))
ADMIN = int(os.getenv('ADMIN'))
PHONE_MASK = "375"
