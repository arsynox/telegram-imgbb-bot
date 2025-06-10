# database.py

from pymongo import MongoClient
from config import MONGODB_URI
from datetime import datetime

client = MongoClient(MONGODB_URI)
db = client["arsynox_imgbb_bot"]

users_collection = db["users"]
images_collection = db["images"]


def get_user(user_id):
    return users_collection.find_one({"user_id": user_id})


def add_or_update_user(user_id, username=None, server=None, subscribed=False):
    update_fields = {"subscribed": subscribed}
    if username:
        update_fields["username"] = username
    if server:
        update_fields["server"] = server
    update_fields["last_seen"] = datetime.utcnow()
    users_collection.update_one(
        {"user_id": user_id},
        {"$set": update_fields},
        upsert=True,
    )


def update_subscription_status(user_id, subscribed):
    users_collection.update_one(
        {"user_id": user_id},
        {"$set": {"subscribed": subscribed, "last_seen": datetime.utcnow()}},
        upsert=True,
    )


def save_image_upload(user_id, server, image_url, delete_after=None):
    doc = {
        "user_id": user_id,
        "server": server,
        "image_url": image_url,
        "uploaded_at": datetime.utcnow(),
        "delete_after": delete_after,
    }
    images_collection.insert_one(doc)
