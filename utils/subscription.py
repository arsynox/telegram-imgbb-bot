from telegram import Bot
import config

async def is_user_subscribed(bot: Bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=config.SUBSCRIBE_CHANNEL, user_id=user_id)
        status = member.status
        return status in ["member", "administrator", "creator"]
    except:
        return False
