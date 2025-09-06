from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import search_files
from utils import make_ad_link, batch_link
from config import CHANNEL_ID

async def start_handler(client, message):
    await message.reply_text(
        "🎬 Welcome to Movie Search Bot!\n\n"
        "🔍 Send me a movie/series name to search.\n"
        "📦 If many episodes found → I’ll give you a Batch Download link.\n"
        "💰 Support us by using the links.",
    )

async def search_handler(client, message):
    query = message.text.strip()
    results = await search_files(client, query)

    if not results:
        await message.reply_text("❌ কিছু পাওয়া যায়নি!")
        return

    # যদি অনেক ফাইল পাওয়া যায় → batch link
    if len(results) > 5:
        files = [f"https://t.me/{client.me.username}?start={r['file_id']}" for r in results]
        batch = batch_link(files)
        await message.reply_text(
            f"📦 {len(results)} Episodes Found for: **{query}**\n\n"
            f"👉 Batch Link: {batch}"
        )
    else:
        # একটার পর একটা ফাইল ad-link সহ পাঠানো
        for r in results:
            link = make_ad_link(f"https://t.me/{client.me.username}?start={r['file_id']}")
            await message.reply_text(
                f"🎬 **{r['file_name']}**\n\n👉 {link}",
                disable_web_page_preview=True
            )
