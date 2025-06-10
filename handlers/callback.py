# handlers/callback.py

from aiogram import types
from keyboards.inline import server_selection_keyboard, subscription_check_keyboard, main_menu_keyboard
from database import add_or_update_user, update_subscription_status
from utils.subscription import is_user_subscribed


async def callback_handler(callback: types.CallbackQuery, bot):
    data = callback.data
    user_id = callback.from_user.id
    username = callback.from_user.username

    if data.startswith("server_"):
        # User selected a server
        server = data.split("_", 1)[1]
        add_or_update_user(user_id, username=username, server=server)
        await callback.answer(f"Server set to {server.capitalize()}. You can now upload images.")
        await callback.message.edit_text(
            f"Server selected: {server.capitalize()}\n\n"
            "Send me an image to upload.",
            reply_markup=main_menu_keyboard(),
        )

    elif data == "check_subscription":
        subscribed = await is_user_subscribed(bot, user_id)
        update_subscription_status(user_id, subscribed)
        if subscribed:
            await callback.answer("Subscription verified! You can now use the bot.", show_alert=True)
            # If user has no server selected, ask to select
            user = await bot.get_chat(user_id)
            # We do not have direct DB access here, so just prompt server selection
            await callback.message.edit_text(
                "Subscription confirmed! Please select a server to start uploading images.",
                reply_markup=server_selection_keyboard(),
            )
        else:
            await callback.answer("You are not subscribed yet. Please subscribe and try again.", show_alert=True)

    elif data == "change_server":
        await callback.answer()
        await callback.message.edit_text(
            "Please select a server:",
            reply_markup=server_selection_keyboard(),
        )
