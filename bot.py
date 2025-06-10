# bot.py

import logging
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN, ADMIN_USER_ID
from handlers import start, callback, image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def on_start(message: types.Message):
    await start.cmd_start(message, bot)


@dp.callback_query_handler()
async def on_callback(callback: types.CallbackQuery):
    await callback_handler(callback)


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def on_photo(message: types.Message):
    await image.handle_image(message, bot)


# Admin commands placeholder (extend as needed)
@dp.message_handler(lambda m: m.from_user.id == ADMIN_USER_ID, commands=["admin"])
async def admin_command(message: types.Message):
    await message.reply("Admin command received.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
