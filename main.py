import asyncio, datetime, uuid
from io import BytesIO
from pyrogram import Client, filters
from pyrogram.types import (
    InlineQueryResultArticle, InputTextMessageContent,
    InlineKeyboardButton, InlineKeyboardMarkup
)

from config import (
    BOT_TOKEN, API_ID, API_HASH,
    FILE_STORE_CHANNEL, LOG_CHANNEL,
    BRAND_NAME, BRAND_LINK,
    AUTO_DELETE_SECONDS, USER_VIDEO_LIFETIME_DAYS, OWNER_IDS
)
from db import files_col, channels_col, search_logs_col, users_col
from ads import get_ads_for_query

app = Client("bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

# ----------------------------
# Owner-only connect/disconnect
# ----------------------------
@app.on_message(filters.command("connect") & filters.user(OWNER_IDS))
async def connect_channel(client, message):
    if len(message.command) < 2:
        return await message.reply_text("Use: /connect -1001234567890")
    ch = int(message.command[1])
    try:
        me = await client.get_chat_member(ch, "me")
        if me.status not in ("administrator", "creator"):
            return await message.reply_text("Bot must be admin in that channel.")
    except Exception as e:
        return await message.reply_text(f"Cannot access channel: {e}")

    channels_col.update_one(
        {"channel_id": ch},
        {"$set": {"channel_id": ch, "connected_at": datetime.datetime.utcnow(), "is_bot_admin": True}},
        upsert=True,
    )
    await message.reply_text(f"Connected to {ch}. Fetching files...")
    asyncio.create_task(fetch_store_channel_media(client, ch))


@app.on_message(filters.command("disconnect") & filters.user(OWNER_IDS))
async def disconnect_channel(client, message):
    ch = int(message.command[1])
    channels_col.delete_one({"channel_id": ch})
    await message.reply_text(f"Disconnected {ch}")

# ----------------------------
# Channel Media Fetcher
# ----------------------------
async def fetch_store_channel_media(client, channel_id):
    async for msg in client.get_history(channel_id, limit=200):
        if msg.video or msg.document:
            data = {
                "message_id_in_store": msg.id,
                "store_channel_id": channel_id,
                "file_unique_id": (msg.video or msg.document).file_unique_id,
                "file_name": (msg.video or msg.document).file_name or "",
                "size": (msg.video or msg.document).file_size or 0,
                "metadata": {"caption": msg.caption or ""},
                "created_at": datetime.datetime.utcnow(),
            }
            files_col.update_one(
                {"file_unique_id": data["file_unique_id"]}, {"$set": data}, upsert=True
            )

# ----------------------------
# Inline Search with Ads
# ----------------------------
@app.on_inline_query()
async def inline_search(client, inline_query):
    q = inline_query.query.strip()
    user = inline_query.from_user
    users_col.update_one(
        {"user_id": user.id},
        {"$set": {"last_seen": datetime.datetime.utcnow(), "username": user.username}},
        upsert=True,
    )

    results = (
        list(files_col.find({"$text": {"$search": q}}).limit(25))
        if q
        else list(files_col.find().limit(25))
    )

    ads = get_ads_for_query(q, max_ads=1)
    answers = []

    # Sponsored Ad result at top
    if ads:
        ad = ads[0]
        ad_id = f"ad-{ad['id']}-{uuid.uuid4().hex[:6]}"
        ad_content = ad["text"] + f"\n\nVisit: {ad['button_url']}"
        ad_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(ad["button_text"], url=ad["button_url"])]]
        )
        ad_result = InlineQueryResultArticle(
            id=ad_id,
            title=f"[Ad] {ad['title']}",
            input_message_content=InputTextMessageContent(ad_content),
            description=ad["text"],
            reply_markup=ad_markup,
        )
        answers.append(ad_result)

    # Sponsor button for all results
    sponsor_button = None
    if ads:
        sponsor_button = InlineKeyboardButton(ads[0]["button_text"], url=ads[0]["button_url"])

    for r in results:
        watch_btn = InlineKeyboardButton("Watch ▶", callback_data=f"getfile:{r['file_unique_id']}")
        row = [watch_btn]
        if sponsor_button:
            row.append(sponsor_button)

        buttons = InlineKeyboardMarkup([row])

        res = InlineQueryResultArticle(
            id=r["file_unique_id"],
            title=r.get("file_name", "Result"),
            input_message_content=InputTextMessageContent(f"{r.get('file_name','')}\n\n{BRAND_NAME}"),
            description=r.get("metadata", {}).get("caption", ""),
            reply_markup=buttons
        )
        answers.append(res)

    if not answers:
        if LOG_CHANNEL:
            await client.send_message(LOG_CHANNEL, f"Zero results for `{q}` from {user.id}")
        return await inline_query.answer([], switch_pm_text="No results", switch_pm_parameter="nores")

    await inline_query.answer(answers, cache_time=5)

# ----------------------------
# Inline Button → Send Video
# ----------------------------
@app.on_callback_query(filters.create(lambda _, __, cq: cq.data and cq.data.startswith("getfile:")))
async def on_getfile(client, cq):
    unique_id = cq.data.split(":", 1)[1]
    doc = files_col.find_one({"file_unique_id": unique_id})
    if not doc:
        return await cq.answer("ফাইল পাওয়া যায়নি।", show_alert=True)

    msg = await client.get_messages(doc["store_channel_id"], doc["message_id_in_store"])
    media = msg.video or msg.document
    temp = await client.download_media(media, file=BytesIO())
    temp.seek(0)

    sent = await client.send_video(
        cq.from_user.id,
        video=temp,
        caption=f"{doc.get('file_name','')}\n\n{BRAND_NAME}",
        protect_content=True  # forward/copy disabled
    )

    delete_at = datetime.datetime.utcnow() + datetime.timedelta(days=USER_VIDEO_LIFETIME_DAYS)
    files_col.update_one({"_id": doc["_id"]}, {"$set": {"del_after": delete_at, "sent_msg_id": sent.id}})
    await cq.answer("ভিডিও পাঠানো হয়েছে — ৫ দিন পর মুছে যাবে।", show_alert=True)

# ----------------------------
# Cleanup Loop
# ----------------------------
async def cleanup_loop():
    while True:
        now = datetime.datetime.utcnow()
        expired = list(files_col.find({"del_after": {"$lte": now}}))
        for doc in expired:
            try:
                await app.delete_messages(doc["store_channel_id"], doc["sent_msg_id"])
            except:
                pass
            files_col.update_one({"_id": doc["_id"]}, {"$unset": {"sent_msg_id": "", "del_after": ""}})
        await asyncio.sleep(60)

# ----------------------------
# Start Message
# ----------------------------
@app.on_message(filters.command("start"))
async def start_msg(client, message):
    t = f"👋 Welcome to {BRAND_NAME}!\n\nUse inline search to find videos."
    await message.reply_photo(photo="https://placehold.co/600x400.png", caption=t)

# ----------------------------
# Run Bot
# ----------------------------
if __name__ == "__main__":
    app.start()
    loop = asyncio.get_event_loop()
    loop.create_task(cleanup_loop())
    print("Bot started")
    app.idle()
