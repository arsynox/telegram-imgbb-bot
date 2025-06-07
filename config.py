# ===============================================
# TELEGRAM IMAGE HOSTING BOT CONFIGURATION
# ===============================================
# Replace the values below with your actual credentials

# Bot Configuration
BOT_TOKEN = "8059253160:AAH0xNsZVUKgSX6qtbuM40Gz2j51hxxZN04"  # Get from @BotFather

# Database Configuration
# MongoDB URI - Replace with your actual MongoDB connection string
MONGODB_URI = "mongodb://localhost:27017/"  # Default local MongoDB
# For MongoDB Atlas (Cloud): "mongodb+srv://username:password@cluster.mongodb.net/"
# For MongoDB with authentication: "mongodb://username:password@host:port/"

DATABASE_NAME = "telegram_bot_db"  # Database name

# Multiple ImgBB API Keys for Different Servers
IMGBB_API_KEYS = {
    'server_1': "9519474fc492698dbb639aec847a1919",  # Server 1 API Key (6 months auto-delete)
    'server_2': "2d7842bb09c5229c7dcc4acdeb7bc401",  # Server 2 API Key (1 month auto-delete)    
    'server_3': "5c3d4b0dd67e705eec4497a46d2ae421"   # Server 3 API Key (no auto-delete)
}

# Channel Configuration for Forced Subscription
CHANNEL_USERNAME = "@codexfusion"  # Your channel username with @
CHANNEL_ID = -1002638392397                 # Your channel ID (negative number)

# Admin Configuration
ADMIN_ID = 6822491887                        # Your Telegram user ID

# ImgBB Server Configuration
IMGBB_SERVERS = {
    'server_1': {
        'url': 'https://api.imgbb.com/1/upload',
        'api_key': IMGBB_API_KEYS['server_1'],
        'expiration': 15552000,  # 6 months in seconds (6 * 30 * 24 * 60 * 60)
        'name': 'Server 1 (6 Months)',
        'description': 'Files auto-delete after 6 months',
        'icon': '🚀'
    },
    'server_2': {
        'url': 'https://api.imgbb.com/1/upload', 
        'api_key': IMGBB_API_KEYS['server_2'],
        'expiration': 2592000,   # 1 month in seconds (30 * 24 * 60 * 60)
        'name': 'Server 2 (1 Month)',
        'description': 'Files auto-delete after 1 month',
        'icon': '⚡'
    },
    'server_3': {
        'url': 'https://api.imgbb.com/1/upload',
        'api_key': IMGBB_API_KEYS['server_3'], 
        'expiration': 0,         # No expiration (permanent)
        'name': 'Server 3 (Permanent)',
        'description': 'Files stored permanently',
        'icon': '🔥'
    }
}

# Database Configuration Options
DB_CONFIG = {
    'connection_timeout': 5000,  # Connection timeout in milliseconds
    'max_pool_size': 50,         # Maximum number of connections in the pool
    'retry_writes': True,        # Enable retryable writes
    'w': 'majority'              # Write concern
}

# Messages
WELCOME_MESSAGE = """
🚀 **Welcome to Lightning Image Host!** ⚡

Transform your images into instant shareable links!
📸 Upload → 🔗 Get Link → 🌍 Share Anywhere

Ready to get started? Choose your server below! 👇
"""

SUBSCRIPTION_MESSAGE = """
🔒 **Access Required!**

To use this premium service, please join our channel first:
👉 {channel}

After joining, click 'Check Subscription' to continue! ✨
"""

# Error Messages
DATABASE_ERROR_MESSAGE = "🔧 Database temporarily unavailable. Please try again later."
SERVER_ERROR_MESSAGE = "⚠️ Server error occurred. Please contact support if this persists."
UPLOAD_ERROR_MESSAGE = "❌ Failed to upload image. Please try again or select a different server."

# Success Messages
UPLOAD_SUCCESS_MESSAGE = """
✅ **Upload Successful!**

🔗 **Direct Link:** `{image_url}`
🗑️ **Delete Link:** `{delete_url}`
📊 **Server:** {server_name}
📅 **Upload Date:** {upload_date}

Tap to copy the links! 📋
"""

# Environment Variables Support (Optional)
import os

# Override with environment variables if available
BOT_TOKEN = os.getenv('BOT_TOKEN', BOT_TOKEN)
MONGODB_URI = os.getenv('MONGODB_URI', MONGODB_URI)
DATABASE_NAME = os.getenv('DATABASE_NAME', DATABASE_NAME)
CHANNEL_USERNAME = os.getenv('CHANNEL_USERNAME', CHANNEL_USERNAME)
CHANNEL_ID = int(os.getenv('CHANNEL_ID', CHANNEL_ID))
ADMIN_ID = int(os.getenv('ADMIN_ID', ADMIN_ID))

# Override API keys with environment variables if available
for server in IMGBB_API_KEYS:
    env_key = f'IMGBB_API_KEY_{server.upper()}'
    if os.getenv(env_key):
        IMGBB_API_KEYS[server] = os.getenv(env_key)
        IMGBB_SERVERS[server]['api_key'] = os.getenv(env_key)

# Validation function
def validate_config():
    """Validate configuration settings"""
    errors = []
    
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        errors.append("BOT_TOKEN is not set")
    
    if not MONGODB_URI:
        errors.append("MONGODB_URI is not set")
    
    if not all(IMGBB_API_KEYS.values()):
        errors.append("One or more IMGBB_API_KEYS are missing")
    
    if not CHANNEL_USERNAME or CHANNEL_USERNAME == "@your_channel":
        errors.append("CHANNEL_USERNAME is not properly configured")
    
    if ADMIN_ID == 0:
        errors.append("ADMIN_ID is not set")
    
    if errors:
        print("❌ Configuration Errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    print("✅ Configuration validated successfully!")
    return True
