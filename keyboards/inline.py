from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_server_selection_keyboard():
    buttons = [
        [InlineKeyboardButton("Server1 (6 months)", callback_data="server_Server1")],
        [InlineKeyboardButton("Server2 (1 month)", callback_data="server_Server2")],
        [InlineKeyboardButton("Server3 (No auto delete)", callback_data="server_Server3")],
    ]
    return InlineKeyboardMarkup(buttons)

def get_subscription_keyboard():
    buttons = [
        [InlineKeyboardButton("Check Subscription", callback_data="check_subscription")]
    ]
    return InlineKeyboardMarkup(buttons)

def get_main_menu_keyboard():
    buttons = [
        [InlineKeyboardButton("Choose Server", callback_data="choose_server")],
        [InlineKeyboardButton("Check Subscription", callback_data="check_subscription")]
    ]
    return InlineKeyboardMarkup(buttons)
