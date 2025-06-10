# config.py

BOT_TOKEN = "8059253160:AAH0xNsZVUKgSX6qtbuM40Gz2j51hxxZN04"

MONGODB_URI = "YOUR_MONGODB_CONNECTION_URI"

# imgbb API keys mapped to server names
IMGBB_API_KEYS = {
    "server1": "IMGBB_API_KEY_SERVER1",
    "server2": "IMGBB_API_KEY_SERVER2",
    "server3": "IMGBB_API_KEY_SERVER3",
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
