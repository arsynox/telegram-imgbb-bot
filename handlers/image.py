from telegram import Update
from telegram.ext import ContextTypes
from database import users_collection, images_collection
from utils.imgbb import upload_image_to_imgbb
from utils.subscription import is_user_subscribed

async def image_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message

    # Check subscription
    subscribed = await is_user_subscribed(context.bot, user.id)
    if not subscribed:
        await message.reply_text("❌ You must subscribe to our channel to use this bot.")
        return

    # Get user server from DB or default to Server1
    user_data = await users_collection.find_one({"user_id": user.id})
    server_name = user_data.get("server") if user_data and "server" in user_data else "Server1"

    # Download photo bytes
    photo = message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    file_bytes = await file.download_as_bytearray()

    # Upload to imgbb
    url, error = await upload_image_to_imgbb(file_bytes, server_name)
    if error:
        await message.reply_text(f"❌ Upload failed: {error}")
        return

    # Save image record with user, url, server, timestamp
    import datetime
    record = {
        "user_id": user.id,
        "url": url,
        "server": server_name,
        "timestamp": datetime.datetime.utcnow()
    }
    await images_collection.insert_one(record)

    await message.reply_text(f"✅ Uploaded successfully!\nYour image URL:\n{url}")
