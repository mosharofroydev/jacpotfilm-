from pyrogram import Client
from config import Config

bot = Client(
    "AutoFilterBot",
    bot_token=Config.BOT_TOKEN,
)

print("🤖 Auto Filter Bot Started...")
bot.run()
