from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import config

def get_server_selection_keyboard():
    """Create server selection keyboard with expiration info"""
    keyboard = [
        [
            InlineKeyboardButton("🚀 Server 1 (6 Months)", callback_data="server_server_1"),
            InlineKeyboardButton("⚡ Server 2 (1 Month)", callback_data="server_server_2")
        ],
        [
            InlineKeyboardButton("🔥 Server 3 (Permanent)", callback_data="server_server_3")
        ],
        [
            InlineKeyboardButton("ℹ️ Server Info", callback_data="server_info")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_subscription_keyboard():
    """Create subscription check keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{config.CHANNEL_USERNAME[1:]}")
        ],
        [
            InlineKeyboardButton("✅ Check Subscription", callback_data="check_subscription")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_main_menu_keyboard():
    """Create main menu keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("🔄 Change Server", callback_data="change_server"),
            InlineKeyboardButton("📊 My Stats", callback_data="my_stats")
        ],
        [
            InlineKeyboardButton("❓ Help", callback_data="help"),
            InlineKeyboardButton("💡 Tips", callback_data="tips")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
