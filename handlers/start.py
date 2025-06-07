from telegram import Update
from telegram.ext import ContextTypes
from keyboards.inline import get_subscription_keyboard
from utils.subscription import is_user_subscribed

WELCOME_MESSAGE = """
👋 Welcome to Arsynox Image Hosting Bot!

🚀 Upload your images and get instant links!
🔧 Choose your preferred server with different auto-delete times.

Please subscribe to our channel to use this bot.
"""

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # Check subscription
    subscribed = await is_user_subscribed(context.bot, user.id)

    if not subscribed:
        await update.message.reply_text(
            WELCOME_MESSAGE,
            reply_markup=get_subscription_keyboard(),
            disable_web_page_preview=True
        )
    else:
        await update.message.reply_text(
            "You are subscribed ✅\nUse the menu below:",
            reply_markup=get_main_menu_keyboard()
        )
