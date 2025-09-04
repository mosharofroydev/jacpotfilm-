from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

# 🛠 API ও Bot Token
API_ID = 24776633
API_HASH = "57b1f632044b4e718f5dce004a988d69"
BOT_TOKEN = "8210471056:AAEc76RNEX1w32M7WfyY3R8uKzEBy4aOb8"

# 🛠 চ্যানেল ID
SOURCE_CHANNEL = -1003002438395

# 🛠 MongoDB সংযোগ
MONGO_URL = "mongodb+srv://banglajac13_db_user:ZGTKOUJTJloOFFQS@cluster0.wdbssln.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client["search_bot_db"]  # ডাটাবেস

# 🔹 Pyrogram Client
app = Client("search_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 🔹 Start কমান্ড
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(
        f"👋 হ্যালো **{message.from_user.first_name}**!\n\n"
        "আমি একটি সার্চ বট। 🎬\n"
        "👉 শুধু মুভির নাম লিখুন, আমি ফাইল খুঁজে দেব।\n\n"
        "📌 উদাহরণ: `KGF`"
    )

# 🔹 সার্চ ফাইল
@app.on_message(filters.text & ~filters.command("start"))
async def search_files(client, message):
    query = message.text.lower()
    results = []

    async for msg in app.search_messages(chat_id=SOURCE_CHANNEL, query=query, limit=5):
        # ডকুমেন্ট, ভিডিও বা অডিও হলে
        if msg.document or msg.video or msg.audio:
            file_name = getattr(msg.document or msg.video or msg.audio, "file_name", "ফাইল")
            results.append([InlineKeyboardButton(file_name, callback_data=f"get_{msg.id}")])

    if results:
        sent_msg = await message.reply(
            f"🔎 **'{query}'** এর জন্য পাওয়া গেছে:",
            reply_markup=InlineKeyboardMarkup(results)
        )
        # ৫ মিনিট পরে ডিলিট
        await asyncio.sleep(300)
        try:
            await sent_msg.delete()
        except:
            pass
    else:
        await message.reply("❌ কিছু পাওয়া যায়নি।")

# 🔹 Callback ফাংশন
@app.on_callback_query(filters.regex(r"^get_"))
async def send_file(client, callback_query):
    msg_id = int(callback_query.data.split("_")[1])
    try:
        file_msg = await app.get_messages(SOURCE_CHANNEL, msg_id)
        await file_msg.copy(callback_query.message.chat.id)
        await callback_query.answer("✅ ফাইল পাঠানো হলো।", show_alert=True)
    except:
        await callback_query.answer("⚠️ ফাইল আনতে সমস্যা হয়েছে।", show_alert=True)

# 🔹 Run
app.run()
