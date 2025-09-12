from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["botdb"]

channels_col = db.channels
files_col = db.files
users_col = db.users
search_logs_col = db.search_logs

# search index
try:
    files_col.create_index([("file_name", "text"), ("metadata.caption", "text")])
except:
    pass
