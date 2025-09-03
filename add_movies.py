from database import add_movie

# নতুন ভিডিও যোগ করার লিস্ট
movies = [
    ("Spider Man 1", 101),
    ("Spider Man 2", 102),
    ("Spider Man 3", 103),
]

for title, channel_message_id in movies:
    add_movie(title, channel_message_id)
    print(f"✅ Added: {title}")
