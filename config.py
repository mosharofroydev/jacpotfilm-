import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
MONGO_URI = os.getenv("MONGO_URI")

FILE_STORE_CHANNEL = int(os.getenv("FILE_STORE_CHANNEL"))
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "0"))

BRAND_NAME = os.getenv("BRAND_NAME")
BRAND_LINK = os.getenv("BRAND_LINK")

AUTO_DELETE_SECONDS = int(os.getenv("AUTO_DELETE_SECONDS"))
USER_VIDEO_LIFETIME_DAYS = int(os.getenv("USER_VIDEO_LIFETIME_DAYS"))

OWNER_IDS = [int(x) for x in os.getenv("OWNER_IDS", "").split(",") if x]
