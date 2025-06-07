import asyncio
from typing import Optional
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError
import os

class Database:
    def __init__(self, mongodb_uri: str = None, db_name: str = "Cluster0"):
        """
        Initialize MongoDB connection
        
        Args:
            mongodb_uri: MongoDB connection URI (defaults to environment variable MONGODB_URI)
            db_name: Database name to use
        """
        self.mongodb_uri = mongodb_uri or os.getenv('MONGODB_URI', 'mongodb+srv://arsynox:arsynox#90@cluster0.rllegme.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
        self.db_name = db_name
        
        try:
            self.client = MongoClient(self.mongodb_uri)
            self.db = self.client[self.db_name]
            
            # Test connection
            self.client.admin.command('ping')
            print(f"Successfully connected to MongoDB: {self.db_name}")
            
            self.init_database()
            
        except ConnectionFailure as e:
            print(f"Failed to connect to MongoDB: {e}")
            raise
    
    def init_database(self):
        """Initialize database collections and indexes"""
        try:
            # Create collections
            self.users_collection = self.db.users
            self.images_collection = self.db.images
            
            # Create indexes for better performance
            self.users_collection.create_index("user_id", unique=True)
            self.images_collection.create_index("user_id")
            self.images_collection.create_index("upload_date")
            
            print("Database collections and indexes initialized successfully")
            
        except Exception as e:
            print(f"Error initializing database: {e}")
            raise
    
    def add_user(self, user_id: int, username: str = None, first_name: str = None):
        """Add or update user in database"""
        try:
            user_data = {
                "user_id": user_id,
                "username": username,
                "first_name": first_name,
                "selected_server": "server_1",
                "subscription_status": False,
                "join_date": datetime.utcnow(),
                "last_activity": datetime.utcnow()
            }
            
            # Use upsert to insert or update
            self.users_collection.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "username": username,
                        "first_name": first_name,
                        "last_activity": datetime.utcnow()
                    },
                    "$setOnInsert": {
                        "selected_server": "server_1",
                        "subscription_status": False,
                        "join_date": datetime.utcnow()
                    }
                },
                upsert=True
            )
            
        except Exception as e:
            print(f"Error adding/updating user {user_id}: {e}")
            raise
    
    def get_user_server(self, user_id: int) -> str:
        """Get user's selected server"""
        try:
            user = self.users_collection.find_one(
                {"user_id": user_id},
                {"selected_server": 1}
            )
            
            return user.get("selected_server", "server_1") if user else "server_1"
            
        except Exception as e:
            print(f"Error getting user server for {user_id}: {e}")
            return "server_1"
    
    def update_user_server(self, user_id: int, server: str):
        """Update user's selected server"""
        try:
            result = self.users_collection.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "selected_server": server,
                        "last_activity": datetime.utcnow()
                    }
                }
            )
            
            if result.matched_count == 0:
                # User doesn't exist, create them
                self.add_user(user_id)
                self.update_user_server(user_id, server)
                
        except Exception as e:
            print(f"Error updating user server for {user_id}: {e}")
            raise
    
    def log_image_upload(self, user_id: int, image_url: str, delete_url: str, server: str):
        """Log image upload to database"""
        try:
            image_data = {
                "user_id": user_id,
                "image_url": image_url,
                "delete_url": delete_url,
                "server_used": server,
                "upload_date": datetime.utcnow()
            }
            
            self.images_collection.insert_one(image_data)
            
        except Exception as e:
            print(f"Error logging image upload for user {user_id}: {e}")
            raise
    
    def get_user_images(self, user_id: int, limit: int = 50):
        """Get user's uploaded images"""
        try:
            images = self.images_collection.find(
                {"user_id": user_id}
            ).sort("upload_date", -1).limit(limit)
            
            return list(images)
            
        except Exception as e:
            print(f"Error getting images for user {user_id}: {e}")
            return []
    
    def get_user_stats(self, user_id: int) -> dict:
        """Get user statistics"""
        try:
            user = self.users_collection.find_one({"user_id": user_id})
            if not user:
                return {}
            
            image_count = self.images_collection.count_documents({"user_id": user_id})
            
            return {
                "user_id": user["user_id"],
                "username": user.get("username"),
                "first_name": user.get("first_name"),
                "selected_server": user.get("selected_server", "server_1"),
                "subscription_status": user.get("subscription_status", False),
                "join_date": user.get("join_date"),
                "last_activity": user.get("last_activity"),
                "total_images": image_count
            }
            
        except Exception as e:
            print(f"Error getting user stats for {user_id}: {e}")
            return {}
    
    def close(self):
        """Close database connection"""
        if hasattr(self, 'client'):
            self.client.close()
            print("MongoDB connection closed")


# Usage example:
if __name__ == "__main__":
    # Initialize with MongoDB URI
    db = Database(
        mongodb_uri="mongodb+srv://arsynox:arsynox#90@cluster0.rllegme.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
        db_name="Cluster0"
    )
    
    # Or use environment variable
    # export MONGODB_URI="mongodb://username:password@host:port/database_name"
    # db = Database()
    
    try:
        # Test the database
        db.add_user(12345, "testuser", "Test User")
        server = db.get_user_server(12345)
        print(f"User server: {server}")
        
        db.update_user_server(12345, "server_2")
        db.log_image_upload(12345, "http://example.com/image.jpg", "http://example.com/delete/123", "server_2")
        
        stats = db.get_user_stats(12345)
        print(f"User stats: {stats}")
        
    finally:
        db.close()
