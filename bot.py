from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from handlers.start import start_handler
from handlers.callback import callback_handler
from handlers.image import image_handler
import config

def main():
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.PHOTO, image_handler))

    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
