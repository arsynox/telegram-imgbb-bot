from telegram import Bot
from telegram.error import TelegramError
import config

async def check_subscription(bot: Bot, user_id: int) -> bool:
    """Check if user is subscribed to the required channel"""
    try:
        member = await bot.get_chat_member(chat_id=config.CHANNEL_ID, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except TelegramError:
        return False

async def is_user_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id == config.ADMIN_ID
