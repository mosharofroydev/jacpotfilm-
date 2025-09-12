from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database import db
import ads
from config import Config

# Welcome / Start
@Client.on_message(filters.command("start"))
async def start_handler(client, message: Message):
    await message.reply_text(
        Config.START_MSG.format(name=message.from_user.first_name),
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("📢 Channel", url="https://t.me/yourchannel")]]
        )
    )

# Connect
@Client.on_message(filters.command("connect") & filters.user(Config.ADMINS))
async def connect_handler(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Channel/Group ID দিন। Example: /connect -1001234567890")
    chat_id = message.command[1]
    db.connect_chat(chat_id)
    await message.reply_text(f"✅ Connected with `{chat_id}`")

# Disconnect
@Client.on_message(filters.command("disconnect") & filters.user(Config.ADMINS))
async def disconnect_handler(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Channel/Group ID দিন।")
    chat_id = message.command[1]
    db.disconnect_chat(chat_id)
    await message.reply_text(f"❌ Disconnected from `{chat_id}`")

# Search in group
@Client.on_message(filters.text & filters.group)
async def search_handler(client, message: Message):
    query = message.text
    result = db.search_video(query)
    if not result:
        return
    buttons = [[InlineKeyboardButton(result["name"], callback_data=f"get-{result['_id']}")]]
    await message.reply_text("🎬 Result Found:", reply_markup=InlineKeyboardMarkup(buttons))

# Callback to send video
@Client.on_callback_query(filters.regex(r"get-(.*)"))
async def send_video(client, callback_query):
    video_id = callback_query.data.split("-")[1]
    video = db.get_video(video_id)
    if not video:
        return await callback_query.message.edit("❌ File not found!")
    await client.send_video(
        chat_id=callback_query.from_user.id,
        file_id=video["file_id"],
        caption=video["name"]
    )
    await ads.send_ad(client, callback_query.from_user.id)
