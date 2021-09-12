import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ROOT = int(os.getenv('ROOT'))
