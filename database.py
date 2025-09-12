import pymongo
from bson.objectid import ObjectId
from config import Config

client = pymongo.MongoClient(Config.DATABASE_URL)
db = client["autofilter"]

videos = db["videos"]
connections = db["connections"]

def connect_chat(chat_id):
    connections.update_one({"chat_id": chat_id}, {"$set": {"chat_id": chat_id}}, upsert=True)

def disconnect_chat(chat_id):
    connections.delete_one({"chat_id": chat_id})

def search_video(name):
    return videos.find_one({"name": {"$regex": name, "$options": "i"}})

def get_video(video_id):
    return videos.find_one({"_id": ObjectId(video_id)})
