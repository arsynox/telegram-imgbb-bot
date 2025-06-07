import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token_here")
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://arsynox:arsynox#90@cluster0.rllegme.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
SUBSCRIBE_CHANNEL = os.getenv("SUBSCRIBE_CHANNEL", "codexfusion")

# Multiple imgbb API keys with server config and deletion periods
SERVERS = {
    "Server1": {
        "api_key": os.getenv("IMGBB_API_KEY_1", "9519474fc492698dbb639aec847a1919"),
        "delete_after_days": 180  # 6 months
    },
    "Server2": {
        "api_key": os.getenv("IMGBB_API_KEY_2", "2d7842bb09c5229c7dcc4acdeb7bc401"),
        "delete_after_days": 30   # 1 month
    },
    "Server3": {
        "api_key": os.getenv("IMGBB_API_KEY_3", "5c3d4b0dd67e705eec4497a46d2ae421"),
        "delete_after_days": None # No auto delete
    },
}
