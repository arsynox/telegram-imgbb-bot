# config.py

BOT_TOKEN = "8059253160:AAH0xNsZVUKgSX6qtbuM40Gz2j51hxxZN04"

MONGODB_URI = "mongodb+srv://arsynox:arsynox#90@cluster0.rllegme.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# imgbb API keys mapped to server names
IMGBB_API_KEYS = {
    "server1": "2d7842bb09c5229c7dcc4acdeb7bc401",
    "server2": "9519474fc492698dbb639aec847a1919",
    "server3": "5c3d4b0dd67e705eec4497a46d2ae421",
}

# Subscription channel or group ID (use negative for groups)
SUBSCRIPTION_CHANNEL_ID = "@codexfusion"

# Auto-delete durations in seconds (None means no auto-delete)
AUTO_DELETE_DURATIONS = {
    "server1": 6 * 30 * 24 * 3600,  # 6 months approx
    "server2": 1 * 30 * 24 * 3600,  # 1 month approx
    "server3": None,                 # no auto-delete
}

# Admin Telegram user ID (integer)
ADMIN_USER_ID = 6822491887
