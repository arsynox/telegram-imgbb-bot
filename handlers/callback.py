from telegram import Update
from telegram.ext import ContextTypes
from keyboards.inline import get_server_selection_keyboard, get_main_menu_keyboard, get_subscription_keyboard
from database import users_collection
from utils.subscription import is_user_subscribed

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = update.effective_user
    data = query.data

    await query.answer()

    if data == "choose_server":
        await query.edit_message_text("Please choose a server:", reply_markup=get_server_selection_keyboard())

    elif data.startswith("server_"):
        server_name = data.split("_")[1]
        # Save user's chosen server in DB
        await users_collection.update_one({"user_id": user.id}, {"$set": {"server": server_name}}, upsert=True)
        await query.edit_message_text(f"Server chosen: {server_name}", reply_markup=get_main_menu_keyboard())

    elif data == "check_subscription":
        subscribed = await is_user_subscribed(context.bot, user.id)
        if subscribed:
            await query.edit_message_text("Subscription verified ✅ You can now upload images.", reply_markup=get_main_menu_keyboard())
        else:
            await query.edit_message_text("You are not subscribed ❌ Please subscribe to use the bot.", reply_markup=get_subscription_keyboard())
