# utils/subscription.py

from config import SUBSCRIPTION_CHANNEL_ID


async def is_user_subscribed(bot, user_id):
    """
    Check if the user is subscribed to the required channel or group.
    Returns True if subscribed, False otherwise.
    """
    try:
        member = await bot.get_chat_member(SUBSCRIPTION_CHANNEL_ID, user_id)
        # Status can be 'member', 'creator', 'administrator', 'restricted'
        if member.status in ("member", "creator", "administrator"):
            return True
        return False
    except Exception:
        # Could be user not found or bot not admin in channel
        return False
