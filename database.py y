from pyrogram import Client
from config import CHANNEL_ID

async def search_files(app: Client, query: str, limit: int = 20):
    """চ্যানেল থেকে keyword দিয়ে ফাইল খোঁজা"""
    results = []
    async for msg in app.search_messages(chat_id=CHANNEL_ID, query=query, limit=limit):
        if msg.document:
            results.append({
                "file_name": msg.document.file_name,
                "file_id": msg.document.file_id
            })
    return results
