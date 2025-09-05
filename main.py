from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from rapidfuzz import fuzz

# আপনার তথ্য
API_ID = 24776633
API_HASH = "57b1f632044b4e718f5dce004a988d69"
BOT_TOKEN = "8210471056:AAEc76RNEX1w32M7WfyY3R8uKzEBy4aOb8s"
CHANNEL_ID = -1003002438395  

# ক্যাটাগরি লিস্ট
CATEGORIES = ["action", "comedy", "romance", "horror", "hindi dubbed", "bengali dubbed"]

app = Client("movie_search_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ⏺ Start কমান্ডে Welcome Message
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    welcome_text = (
        "👋 **Welcome!**\n\n"
        "🎬 আমি Movie Search Bot.\n"
        "আপনি মুভির নাম লিখুন, আমি আপনার জন্য খুঁজে দেব।\n\n"
        "👉 উদাহরণ:\n"
        "`kgf`\n"
        "`kgf hindi dubbed`\n"
        "`kgf bengali dubbed`\n\n"
        "📌 চাইলে ক্যাটাগরি সিলেক্ট করে সার্চ করতে পারবেন।"
    )
    await message.reply(welcome_text)

# ⏺ ইউজার কিছু লিখলে (সার্চ)
@app.on_message(filters.private & filters.text & ~filters.command("start"))
async def search_handler(client, message):
    query = " ".join(message.text.lower().split())
    buttons = [[InlineKeyboardButton(cat.title(), callback_data=f"cat|{cat}|{query}")]
               for cat in CATEGORIES]
    await message.reply("🎬 কোন ক্যাটাগরি থেকে সার্চ করতে চান?",
                        reply_markup=InlineKeyboardMarkup(buttons))

# ⏺ ক্যাটাগরি সিলেক্ট করলে
@app.on_callback_query(filters.regex(r"^cat\|"))
async def category_search(client, callback_query):
    _, category, query = callback_query.data.split("|")
    results = []
    async for msg in app.search_messages(chat_id=CHANNEL_ID, query="", limit=100):
        text = ""
        if msg.caption:
            text = msg.caption.lower()
        elif msg.document:
            text = msg.document.file_name.lower()
        if category in text:
            score = fuzz.partial_ratio(query, text)
            if score > 60:
                results.append(msg)
    if not results:
        await callback_query.message.reply(f"❌ কিছুই পাওয়া যায়নি ({query}, {category})")
        return
    for msg in results:
        await msg.copy(callback_query.message.chat.id)
    await callback_query.answer("✅ রেজাল্ট পাঠানো হলো!")

app.run()
