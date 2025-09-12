import json
import random
from pyrogram import Client

with open("ads.json", "r") as f:
    ADS_LIST = json.load(f)

async def send_ad(client: Client, user_id: int):
    if ADS_LIST:
        ad = random.choice(ADS_LIST)
        await client.send_message(
            user_id,
            f"🔗 Sponsored: {ad['link']}"
        )
