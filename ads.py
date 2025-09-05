 # ads.py
import random

ad_links = [
    "🔥 আমাদের চ্যানেলে জয়েন করুন: https://t.me/your_channel",
    "💥 Sponsor Link: https://example.com/ad1",
    "👉 এখানে ক্লিক করুন: https://example.com/ad2"
]

def random_ad():
    return random.choice(ad_links)
