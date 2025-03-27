import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Define responses
responses = {
    "hello": "Hello! How can I assist you today?",
    "business hours": "Our business hours are from 9 AM to 6 PM, Monday to Friday. We are closed on weekends.",
    "location": 'We are located at 123 Business Avenue, City, Country. Here is a <a href="https://maps.google.com?q=123+Business+Avenue">link to our location</a>',
    "contact": 'You can contact us by phone at (123) 456-7890, by email at contact@ourbusiness.com, or by visiting our <a href="https://www.ourbusiness.com">website</a>'
}

# Function to handle messages
def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text.lower()  # Convert input to lowercase
    response = responses.get(user_message, "Sorry, I don't understand that. Try 'business hours' or 'contact'.")
    update.message.reply_text(response, parse_mode="HTML")

# Function to start the bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome! Ask me about business hours, location, or contact info.")

# Command Handlers
def hours(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(responses["business hours"], parse_mode="HTML")

def location(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(responses["location"], parse_mode="HTML")

def contact(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(responses["contact"], parse_mode="HTML")

def main():
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN is not set in the .env file.")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("hours", hours))
    dp.add_handler(CommandHandler("location", location))
    dp.add_handler(CommandHandler("contact", contact))

    # Message Handler
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
