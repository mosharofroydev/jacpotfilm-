# add_movies.py
import asyncio
from database import add_movie

# নতুন ভিডিও যোগ করার লিস্ট
movies = [
    ("Spider Man 1", 101),  # আসল Message ID ব্যবহার করুন
    ("Spider Man 2", 102),
    ("Spider Man 3", 103),
    ("Welcome To Waikiki", 104)
]

async def main():
    for title, message_id in movies:
        inserted_id = await add_movie(title, message_id)
        print(f"✅ Added: {title} (ID: {inserted_id})")

if __name__ == "__main__":
    asyncio.run(main())
