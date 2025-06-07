from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
import config
from keyboards.inline import get_server_selection_keyboard, get_subscription_keyboard
from utils.subscription import check_subscription
from database import Database

db = Database()

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    
    # Add user to database
    db.add_user(user.id, user.username, user.first_name)
    
    # Check subscription
    is_subscribed = await check_subscription(context.bot, user.id)
    
    if not is_subscribed:
        await update.message.reply_text(
            config.SUBSCRIPTION_MESSAGE.format(channel=config.CHANNEL_USERNAME),
            reply_markup=get_subscription_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Show welcome message and server selection
    await update.message.reply_text(
        config.WELCOME_MESSAGE,
        reply_markup=get_server_selection_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = """
🔥 **Lightning Image Host - Help Guide**

**How to use:**
1️⃣ Choose your preferred server
2️⃣ Send any image (photo, document, etc.)
3️⃣ Get instant shareable link!

**Features:**
• ⚡ Multiple high-speed servers
• 🔒 Secure image hosting
• 📊 Upload statistics
• 🚀 Instant link generation

**Commands:**
/start - Start the bot
/help - Show this help
/stats - View your statistics

**Support:** Contact @your_support_username
    """
    
    await update.message.reply_text
