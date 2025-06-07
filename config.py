===============================================
# TELEGRAM IMAGE HOSTING BOT CONFIGURATION
# ===============================================
# Replace the values below with your actual credentials

# Bot Configuration
BOT_TOKEN = "8059253160:AAH0xNsZVUKgSX6qtbuM40Gz2j51hxxZN04"  # Get from @BotFather

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
