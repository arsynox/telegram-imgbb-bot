from motor.motor_asyncio import AsyncIOMotorClient
import config

client = AsyncIOMotorClient(config.MONGO_URI)
db = client.get_default_database()

# Users collection for storing user info, subscription, chosen server, uploaded images, etc.
users_collection = db.users
images_collection = db.images
