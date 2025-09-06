from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN
from handlers import start_handler, search_handler

app = Client("movie-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(_, message):
    await start_handler(_, message)

@app.on_message(filters.text & ~filters.command("start"))
async def search(_, message):
    await search_handler(_, message)

print("🤖 Bot Started...")
app.run()
