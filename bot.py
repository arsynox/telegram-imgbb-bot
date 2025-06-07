import logging
import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
import config
from handlers.start import start_handler, help_handler
from handlers.image import image_handler
from handlers.callback import callback_handler

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Start the bot"""
    # Create application
    application = Application.builder().token(config.BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(CallbackQueryHandler(callback_handler))
    application.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE, image_handler))
    
    # Start bot
    print("🚀 Lightning Image Host Bot is starting...")
    print(f"📡 Bot will check subscription to: {config.CHANNEL_USERNAME}")
    
    application.run_polling(allowed_updates=["message", "callback_query"])

if __name__ == '__main__':
    main()
