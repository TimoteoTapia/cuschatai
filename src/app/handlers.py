# app/handlers.py
import datetime
import dateparser
from telegram import Update
from telegram.ext import ContextTypes
from src.google_calendar import create_event, delete_event
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from src.app.config import query_engine
from llama_index.core.query_engine import RetrieverQueryEngine
from telegram.ext import CallbackQueryHandler

# User state tracking
user_context = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_context[user_id] = {}

    keyboard = [
        [InlineKeyboardButton("📅 Schedule Appointment", callback_data="agendar")],
        [InlineKeyboardButton("📍 View Hours", callback_data="horarios")],
        [InlineKeyboardButton("💬 Contact Human", callback_data="humano")],
        [InlineKeyboardButton("❌ Cancel Appointment", callback_data="cancelar")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        "Hello! 👋 I'm *CusChatAI*, your virtual assistant.\n\n"
        "I'm here to help with your questions or to schedule an appointment.\n"
        "Please select an option from the menu below 👇"
    )

    await update.message.reply_text(
        welcome_text, reply_markup=reply_markup, parse_mode="Markdown"
    )


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    if data == "agendar":
        await query.edit_message_text(
            "🗓️ Great! To schedule an appointment, please tell me your availability or ask about available times."
        )
    elif data == "horarios":
        await query.edit_message_text(
            "📍 Our available hours are:\n- Monday to Friday: 10am - 6pm\n- Saturday: 11am - 3pm\n\nWould you like to book one?"
        )
    elif data == "humano":
        await query.edit_message_text(
            "💬 A human agent will contact you shortly. In the meantime, you can ask me anything."
        )
    elif data == "cancelar":
        await query.edit_message_text("❌ Appointment canceled.")
    else:
        await query.edit_message_text("❌ Invalid option. Please try again.")


async def handle_schedule_appointment(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    appointment_date = datetime.datetime(2025, 4, 15, 15, 0)  # Example date

    try:
        event_id = create_event(
            summary="Telegram client appointment",
            description=f"Scheduled by user {user_id} via bot",
            start_time=appointment_date,
            duration_minutes=30,
        )
        user_context[user_id]["event_id"] = event_id
        await query.edit_message_text(
            "✅ Your appointment has been successfully scheduled!"
        )
    except Exception as e:
        print(e)
        await query.edit_message_text(
            "❌ An error occurred while scheduling your appointment. Please try again later."
        )


async def handle_cancel_appointment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    event_id = user_context.get(user_id, {}).get("event_id")

    if event_id:
        try:
            delete_event(event_id)
            await query.edit_message_text(
                "🗑️ Your appointment has been successfully canceled."
            )
        except Exception as e:
            print(e)
            await query.edit_message_text(
                "❌ There was a problem canceling your appointment."
            )
    else:
        await query.edit_message_text(
            "You don't have any scheduled appointments to cancel."
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = update.message.text.strip().lower()

    if user_id not in user_context:
        user_context[user_id] = {}

    context_data = user_context[user_id]

    if "cancel" in message or "delete" in message or "remove" in message:
        event_id = context_data.get("event_id")
        if event_id:
            try:
                delete_event(event_id)
                context_data.clear()
                await update.message.reply_text(
                    "🗑️ Your appointment has been successfully canceled."
                )
            except Exception as e:
                print(e)
                await update.message.reply_text(
                    "❌ There was a problem canceling your appointment."
                )
        else:
            await update.message.reply_text(
                "You don't have any scheduled appointments to cancel."
            )
        return

    if context_data.get("pending_confirmation"):
        if message in ["yes", "i confirm", "confirm", "ok"]:
            start_time = context_data["start_time"]
            name = update.effective_user.first_name or "Cliente"
            event_id = create_event(
                summary=f"Cita con {name}",
                description="Cita agendada por CusChatAI",
                start_time=start_time,
            )
            context_data["event_id"] = event_id
            context_data.clear()
            await update.message.reply_text(
                "✅ Your appointment has been successfully scheduled! 😊"
            )
            return
        else:
            await update.message.reply_text(
                "Please confirm your appointment with 'Yes' or 'Confirm'."
            )
            return

    parsed_date = dateparser.parse(message, settings={"PREFER_DATES_FROM": "future"})
    if parsed_date:
        context_data["start_time"] = parsed_date
        context_data["pending_confirmation"] = True
        await update.message.reply_text(
            f"✅ I found the date: {parsed_date.strftime('%A, %B %d at %I:%M %p')}.\n\nDo you confirm this appointment?"
        )
        return

    response = query_engine.query(message)
    await update.message.reply_text(str(response))
