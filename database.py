import sqlite3

DB_NAME = "movies.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            channel_message_id INTEGER
        )
    """)
    conn.commit()
    conn.close()

def add_movie(title, channel_message_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO movies (title, channel_message_id) VALUES (?, ?)",
              (title, channel_message_id))
    conn.commit()
    conn.close()

def search_movies(query):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, title, channel_message_id FROM movies WHERE title LIKE ?", 
              (f"%{query}%",))
    results = c.fetchall()
    conn.close()
    return results
