import os
from dotenv import load_dotenv

load_dotenv()

# Bot API & Token
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")

# Database
MONGO_URI = os.getenv("MONGO_URI", "")

# Channels
FILE_STORE_CHANNEL = int(os.getenv("FILE_STORE_CHANNEL", "0"))
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "0"))

# Branding
BRAND_NAME = os.getenv("BRAND_NAME", "Jacpotfilm")
BRAND_LINK = os.getenv("BRAND_LINK", None)  # Cosmetic only, no URL needed

# Auto-delete & video lifetime
AUTO_DELETE_SECONDS = int(os.getenv("AUTO_DELETE_SECONDS", "300"))  # default 5 min
USER_VIDEO_LIFETIME_DAYS = int(os.getenv("USER_VIDEO_LIFETIME_DAYS", "5"))  # default 5 days

# Owner IDs
OWNER_IDS = [int(x) for x in os.getenv("OWNER_IDS", "").split(",") if x]
