# handlers/start.py

from aiogram import types
from keyboards.inline import server_selection_keyboard, subscription_check_keyboard
from database import add_or_update_user
from utils.subscription import is_user_subscribed
from config import SUBSCRIPTION_CHANNEL_ID


WELCOME_MESSAGES = [
    "👋 Welcome to Arsynox Image Hosting Bot!",
    "✨ Upload your images and get instant links.",
    "🔒 Please subscribe to our channel to start.",
]


async def cmd_start(message: types.Message, bot):
    user_id = message.from_user.id
    username = message.from_user.username

    # Add or update user in DB with subscribed=False initially
    add_or_update_user(user_id, username=username, subscribed=False)

    # Check subscription
    subscribed = await is_user_subscribed(bot, user_id)
    if not subscribed:
        text = (
            "Hello! To use this bot, you must subscribe to our channel or group first.\n\n"
            f"Please join: {SUBSCRIPTION_CHANNEL_ID}\n\n"
            "After subscribing, press the button below to check your subscription."
        )
        await message.answer(text, reply_markup=subscription_check_keyboard())
        return

    # If subscribed, send welcome and ask for server choice
    welcome_text = "\n".join(WELCOME_MESSAGES)
    await message.answer(welcome_text, reply_markup=server_selection_keyboard())
