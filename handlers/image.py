# handlers/image.py

from aiogram import types
from database import get_user, save_image_upload
from utils.subscription import is_user_subscribed
from utils.imgbb import upload_image_to_imgbb, ImgbbUploadError
from config import AUTO_DELETE_DURATIONS


async def handle_image(message: types.Message, bot):
    user_id = message.from_user.id
    user = get_user(user_id)

    if not user:
        await message.reply("Please start the bot first with /start.")
        return

    # Check subscription
    subscribed = await is_user_subscribed(bot, user_id)
    if not subscribed:
        await message.reply(
            "You must subscribe to the required channel or group to use this bot.\n"
            "Please subscribe and then press the 'Check Subscription' button."
        )
        return

    server = user.get("server")
    if not server:
        await message.reply("Please select a server first using /start command.")
        return

    if not message.photo:
        await message.reply("Please send a valid image.")
        return

    photo = message.photo[-1]
    photo_bytes = await photo.download(destination=bytes)

    try:
        image_url = upload_image_to_imgbb(server, photo_bytes.getvalue())
    except ImgbbUploadError as e:
        await message.reply(f"Failed to upload image: {e}")
        return

    delete_after = AUTO_DELETE_DURATIONS.get(server)
    save_image_upload(user_id, server, image_url, delete_after)

    await message.reply(f"Image uploaded successfully:\n{image_url}")
