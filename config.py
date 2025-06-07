import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token_here")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/telegram_imgbb_bot")
SUBSCRIBE_CHANNEL = os.getenv("SUBSCRIBE_CHANNEL", "codexfusion")

# Multiple imgbb API keys with server config and deletion periods
SERVERS = {
    "Server1": {
        "api_key": os.getenv("IMGBB_API_KEY_1", "your_imgbb_api_key_1"),
        "delete_after_days": 180  # 6 months
    },
    "Server2": {
        "api_key": os.getenv("IMGBB_API_KEY_2", "your_imgbb_api_key_2"),
        "delete_after_days": 30   # 1 month
    },
    "Server3": {
        "api_key": os.getenv("IMGBB_API_KEY_3", "your_imgbb_api_key_3"),
        "delete_after_days": None # No auto delete
    },
}
