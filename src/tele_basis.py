import os
from dotenv import load_dotenv
from openai import OpenAI  # Cambio importante
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

load_dotenv()

# Configuración del cliente OpenAI (nueva forma)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Cambio clave
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Soy tu asistente IA. ¿En qué puedo ayudarte?"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    # Nueva sintaxis para chat completions
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente amable y útil."},
            {"role": "user", "content": user_message},
        ],
    )

    reply = response.choices[0].message.content
    await update.message.reply_text(reply)


def run_bot():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot de Telegram corriendo…")
    app.run_polling()


if __name__ == "__main__":
    run_bot()
