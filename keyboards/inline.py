# keyboards/inline.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import AUTO_DELETE_DURATIONS


def server_selection_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(
            text="Server 1 (Delete after 6 months)", callback_data="server_server1"
        ),
        InlineKeyboardButton(
            text="Server 2 (Delete after 1 month)", callback_data="server_server2"
        ),
        InlineKeyboardButton(
            text="Server 3 (No auto-delete)", callback_data="server_server3"
        ),
    )
    return keyboard


def subscription_check_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text="Check Subscription", callback_data="check_subscription")
    )
    return keyboard


def main_menu_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text="Change Server", callback_data="change_server"),
        InlineKeyboardButton(text="Check Subscription", callback_data="check_subscription"),
    )
    return keyboard
