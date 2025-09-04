# database.py
from pymongo import MongoClient

MONGO_URI = "mongodb+srv://banglajac13_db_user:ZGTKOUJTJloOFFQS@cluster0.wdbssln.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)
db = client["movieDB"]  # DB নাম
movies_collection = db["movies"]  # collection নাম

def init_db():
    print("✅ MongoDB Connected")

def add_movie(title, message_id):
    """
    নতুন মুভি MongoDB তে যোগ করবে
    """
    doc = {
        "name": title,
        "message_id": message_id
    }
    result = movies_collection.insert_one(doc)
    return result.inserted_id

def search_movies():
    """
    সব মুভি রিটার্ন করবে
    """
    return list(movies_collection.find({}, {"_id": 1, "name": 1, "message_id": 1}))
