"""
MongoDB Database Handler for Telegram Image Hosting Bot
Handles all database operations including user management and image logging
"""

import asyncio
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure, DuplicateKeyError, PyMongoError
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self, mongodb_uri: str = None, db_name: str = "telegram_bot_db"):
        """
        Initialize MongoDB connection
        
        Args:
            mongodb_uri: MongoDB connection URI (defaults to environment variable MONGODB_URI)
            db_name: Database name to use
        """
        self.mongodb_uri = mongodb_uri or os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        self.db_name = 
        self.client = None
        self.db = None
        
        self._connect()
        self.init_database()
    
    def _connect(self):
        """Establish MongoDB connection"""
        try:
            self.client = MongoClient(
                self.mongodb_uri,
                serverSelectionTimeoutMS=5000,  # 5 second timeout
                connectTimeoutMS=5000,
                maxPoolSize=50,
                retryWrites=True
            )
            
            # Test connection
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            
            logger.info(f"✅ Successfully connected to MongoDB: {self.db_name}")
            
        except ConnectionFailure as e:
            logger.error(f"❌ Failed to connect to MongoDB: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Unexpected error connecting to MongoDB: {e}")
            raise
    
    def init_database(self):
        """Initialize database collections and indexes"""
        try:
            # Create collections
            self.users_collection = self.db.users
            self.images_collection = self.db.images
            self.stats_collection = self.db.stats
            
            # Create indexes for better performance
            
            # Users collection indexes
            self.users_collection.create_index("user_id", unique=True)
            self.users_collection.create_index("username")
            self.users_collection.create_index("last_activity")
            self.users_collection.create_index("subscription_status")
            
            # Images collection indexes
            self.images_collection.create_index("user_id")
            self.images_collection.create_index("upload_date")
            self.images_collection.create_index("server_used")
            self.images_collection.create_index([("user_id", ASCENDING), ("upload_date", DESCENDING)])
            
            # Stats collection indexes
            self.stats_collection.create_index("date", unique=True)
            
            logger.info("✅ Database collections and indexes initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Error initializing database: {e}")
            raise
    
    def add_user(self, user_id: int, username: str = None, first_name: str = None) -> bool:
        """
        Add or update user in database
        
        Args:
            user_id: Telegram user ID
            username: Telegram username
            first_name: User's first name
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            current_time = datetime.utcnow()
            
            # Use upsert to insert or update
            result = self.users_collection.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "username": username,
                        "first_name": first_name,
                        "last_activity": current_time
                    },
                    "$setOnInsert": {
                        "selected_server": "server_1",
                        "subscription_status": False,
                        "join_date": current_time,
                        "total_uploads": 0,
                        "total_storage_used": 0
                    }
                },
                upsert=True
            )
            
            if result.upserted_id:
                logger.info(f"✅ New user added: {user_id}")
            else:
                logger.info(f"✅ User updated: {user_id}")
                
            return True
            
        except Exception as e:
            logger.error(f"❌ Error adding/updating user {user_id}: {e}")
            return False
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get user information
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            Dict containing user information or None
        """
        try:
            user = self.users_collection.find_one({"user_id": user_id})
            return user
            
        except Exception as e:
            logger.error(f"❌ Error getting user {user_id}: {e}")
            return None
    
    def get_user_server(self, user_id: int) -> str:
        """
        Get user's selected server
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            str: Selected server name
        """
        try:
            user = self.users_collection.find_one(
                {"user_id": user_id},
                {"selected_server": 1}
            )
            
            return user.get("selected_server", "server_1") if user else "server_1"
            
        except Exception as e:
            logger.error(f"❌ Error getting user server for {user_id}: {e}")
            return "server_1"
    
    def update_user_server(self, user_id: int, server: str) -> bool:
        """
        Update user's selected server
        
        Args:
            user_id: Telegram user ID
            server: Server name to set
            
        Returns:
            bool: True if successful, False otherwise
        """
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
                # User doesn't exist, create them first
                self.add_user(user_id)
                return self.update_user_server(user_id, server)
            
            logger.info(f"✅ Updated server for user {user_id} to {server}")
            return True
                
        except Exception as e:
            logger.error(f"❌ Error updating user server for {user_id}: {e}")
            return False
    
    def update_subscription_status(self, user_id: int, status: bool) -> bool:
        """
        Update user's subscription status
        
        Args:
            user_id: Telegram user ID
            status: Subscription status
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            result = self.users_collection.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "subscription_status": status,
                        "last_activity": datetime.utcnow()
                    }
                }
            )
            
            return result.matched_count > 0
            
        except Exception as e:
            logger.error(f"❌ Error updating subscription status for {user_id}: {e}")
            return False
    
    def log_image_upload(self, user_id: int, image_url: str, delete_url: str, 
                        server: str, file_size: int = 0, file_name: str = None) -> bool:
        """
        Log image upload to database
        
        Args:
            user_id: Telegram user ID
            image_url: URL of uploaded image
            delete_url: URL to delete the image
            server: Server used for upload
            file_size: Size of uploaded file in bytes
            file_name: Original filename
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            current_time = datetime.utcnow()
            
            image_data = {
                "user_id": user_id,
                "image_url": image_url,
                "delete_url": delete_url,
                "server_used": server,
                "upload_date": current_time,
                "file_size": file_size,
                "file_name": file_name
            }
            
            # Insert image record
            self.images_collection.insert_one(image_data)
            
            # Update user statistics
            self.users_collection.update_one(
                {"user_id": user_id},
                {
                    "$inc": {
                        "total_uploads": 1,
                        "total_storage_used": file_size
                    },
                    "$set": {
                        "last_activity": current_time
                    }
                }
            )
            
            # Update daily statistics
            self._update_daily_stats(current_time.date())
            
            logger.info(f"✅ Image upload logged for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error logging image upload for user {user_id}: {e}")
            return False
    
    def get_user_images(self, user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get user's uploaded images
        
        Args:
            user_id: Telegram user ID
            limit: Maximum number of images to return
            
        Returns:
            List of image documents
        """
        try:
            images = self.images_collection.find(
                {"user_id": user_id}
            ).sort("upload_date", DESCENDING).limit(limit)
            
            return list(images)
            
        except Exception as e:
            logger.error(f"❌ Error getting images for user {user_id}: {e}")
            return []
    
    def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """
        Get comprehensive user statistics
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            Dict containing user statistics
        """
        try:
            user = self.users_collection.find_one({"user_id": user_id})
            if not user:
                return {}
            
            # Get additional stats
            total_images = self.images_collection.count_documents({"user_id": user_id})
            
            # Get images by server
            server_pipeline = [
                {"$match": {"user_id": user_id}},
                {"$group": {"_id": "$server_used", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}
            ]
            server_stats = list(self.images_collection.aggregate(server_pipeline))
            
            # Get recent activity (last 30 days)
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            recent_uploads = self.images_collection.count_documents({
                "user_id": user_id,
                "upload_date": {"$gte": thirty_days_ago}
            })
            
            return {
                "user_id": user["user_id"],
                "username": user.get("username"),
                "first_name": user.get("first_name"),
                "selected_server": user.get("selected_server", "server_1"),
                "subscription_status": user.get("subscription_status", False),
                "join_date": user.get("join_date"),
                "last_activity": user.get("last_activity"),
                "total_uploads": user.get("total_uploads", total_images),
                "total_storage_used": user.get("total_storage_used", 0),
                "recent_uploads": recent_uploads,
                "server_distribution": {item["_id"]: item["count"] for item in server_stats}
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting user stats for {user_id}: {e}")
            return {}
    
    def get_admin_stats(self) -> Dict[str, Any]:
        """
        Get admin statistics for the bot
        
        Returns:
            Dict containing admin statistics
        """
        try:
            current_time = datetime.utcnow()
            
            # Basic counts
            total_users = self.users_collection.count_documents({})
            total_images = self.images_collection.count_documents({})
            subscribed_users = self.users_collection.count_documents({"subscription_status": True})
            
            # Active users (last 7 days)
            week_ago = current_time - timedelta(days=7)
            active_users = self.users_collection.count_documents({
                "last_activity": {"$gte": week_ago}
            })
            
            # Images by server
            server_pipeline = [
                {"$group": {"_id": "$server_used", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}
            ]
            server_stats = list(self.images_collection.aggregate(server_pipeline))
            
            # Daily uploads (last 30 days)
            daily_pipeline = [
                {"$match": {"upload_date": {"$gte": current_time - timedelta(days=30)}}},
                {"$group": {
                    "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$upload_date"}},
                    "count": {"$sum": 1}
                }},
                {"$sort": {"_id": 1}}
            ]
            daily_stats = list(self.images_collection.aggregate(daily_pipeline))
            
            return {
                "total_users": total_users,
                "total_images": total_images,
                "subscribed_users": subscribed_users,
                "active_users_7d": active_users,
                "subscription_rate": round((subscribed_users / total_users * 100), 2) if total_users > 0 else 0,
                "server_distribution": {item["_id"]: item["count"] for item in server_stats},
                "daily_uploads": {item["_id"]: item["count"] for item in daily_stats}
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting admin stats: {e}")
            return {}
    
    def _update_daily_stats(self, date):
        """Update daily statistics"""
        try:
            date_str = date.strftime("%Y-%m-%d")
            
            self.stats_collection.update_one(
                {"date": date_str},
                {
                    "$inc": {"uploads": 1},
                    "$setOnInsert": {"date": date_str}
                },
                upsert=True
            )
            
        except Exception as e:
            logger.error(f"❌ Error updating daily stats: {e}")
    
    def cleanup_old_records(self, days: int = 365) -> int:
        """
        Clean up old image records
        
        Args:
            days: Number of days to keep records
            
        Returns:
            Number of records deleted
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            result = self.images_collection.delete_many({
                "upload_date": {"$lt": cutoff_date}
            })
            
            logger.info(f"✅ Cleaned up {result.deleted_count} old image records")
            return result.deleted_count
            
        except Exception as e:
            logger.error(f"❌ Error cleaning up old records: {e}")
            return 0
    
    def is_connected(self) -> bool:
        """Check if database is connected"""
        try:
            self.client.admin.command('ping')
            return True
        except:
            return False
    
    def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            logger.info("✅ MongoDB connection closed")


# Usage example and testing
if __name__ == "__main__":
    # Initialize database
    db = Database()
    
    try:
        # Test basic operations
        print("Testing database operations...")
        
        # Add a test user
        db.add_user(12345, "testuser", "Test User")
        
        # Get user server
        server = db.get_user_server(12345)
        print(f"User server: {server}")
        
        # Update server
        db.update_user_server(12345, "server_2")
        
        # Log image upload
        db.log_image_upload(
            user_id=12345,
            image_url="https://example.com/image.jpg",
            delete_url="https://example.com/delete/123",
            server="server_2",
            file_size=1024000,
            file_name="test_image.jpg"
        )
        
        # Get user stats
        stats = db.get_user_stats(12345)
        print(f"User stats: {stats}")
        
        # Get admin stats
        admin_stats = db.get_admin_stats()
        print(f"Admin stats: {admin_stats}")
        
        print("✅ All tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        
    finally:
        db.close()
