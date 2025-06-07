import sqlite3
import asyncio
from typing import Optional

class Database:
    def __init__(self, db_path: str = "bot_database.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                selected_server TEXT DEFAULT 'server_1',
                subscription_status BOOLEAN DEFAULT 0,
                join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Images table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                image_url TEXT,
                delete_url TEXT,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                server_used TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, user_id: int, username: str = None, first_name: str = None):
        """Add or update user in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO users (user_id, username, first_name, last_activity)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        ''', (user_id, username, first_name))
        
        conn.commit()
        conn.close()
    
    def get_user_server(self, user_id: int) -> str:
        """Get user's selected server"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT selected_server FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else 'server_1'
    
    def update_user_server(self, user_id: int, server: str):
        """Update user's selected server"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users SET selected_server = ?, last_activity = CURRENT_TIMESTAMP 
            WHERE user_id = ?
        ''', (server, user_id))
        
        conn.commit()
        conn.close()
    
    def log_image_upload(self, user_id: int, image_url: str, delete_url: str, server: str):
        """Log image upload to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO images (user_id, image_url, delete_url, server_used)
            VALUES (?, ?, ?, ?)
        ''', (user_id, image_url, delete_url, server))
        
        conn.commit()
        conn.close()
