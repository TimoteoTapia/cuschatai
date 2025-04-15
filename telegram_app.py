# telegram_app.py
import logging
import os
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ConversationHandler,
)
from src.app.handlers import (
    start,
    handle_callback,
    handle_message,
    CHOOSING_ACTION,
    ENTERING_DATE,
    CONFIRMING_DATE,
    ENTERING_NAME,
    SELECTING_EVENT,
    ENTERING_NEW_DATE,
)
from src.app.config import TELEGRAM_BOT_TOKEN

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def run_bot():
    global telegram_app
    telegram_app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Define conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING_ACTION: [
                CallbackQueryHandler(handle_callback),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message),
            ],
            ENTERING_DATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message),
            ],
            CONFIRMING_DATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message),
            ],
            ENTERING_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message),
            ],
            SELECTING_EVENT: [
                CallbackQueryHandler(handle_callback),
            ],
            ENTERING_NEW_DATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    # Add the conversation handler
    telegram_app.add_handler(conv_handler)

    # Add a fallback handler for general messages
    telegram_app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    logger.info("Bot is running...")
    telegram_app.run_polling()


if __name__ == "__main__":
    # Run the Telegram bot in the main thread
    run_bot()
