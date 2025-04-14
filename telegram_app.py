# telegram_app.py
import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from src.app.handlers import (
    start,
    handle_callback,
    handle_schedule_appointment,
    handle_cancel_appointment,
    handle_message,
)
from src.app.config import TELEGRAM_BOT_TOKEN

# Configuración de logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Registra los handlers importados
    app.add_handler(CallbackQueryHandler(handle_cancel_appointment, pattern="cancelar"))
    app.add_handler(
        CallbackQueryHandler(handle_schedule_appointment, pattern="agendar")
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
