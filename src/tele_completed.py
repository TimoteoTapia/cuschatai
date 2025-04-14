# tele_completed.py
import os
import logging
from dotenv import load_dotenv
import dateparser
from google_calendar import create_event, delete_event
import datetime
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from pinecone import Pinecone
from llama_index.llms.openai import OpenAI
from llama_index.core import (
    Settings,
    VectorStoreIndex,
    get_response_synthesizer,
    PromptTemplate,
)
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine

# ==============
# CONFIGURATION
# ==============

# Load environment variables
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Model and embeddings configuration
client = OpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY, temperature=0)
embedding = OpenAIEmbedding(model="text-embedding-ada-002")
Settings.llm = client
Settings.embed_model = embedding
Settings.chunk_size_limit = 1536

# Pinecone connection
pinecone_client = Pinecone(api_key=PINECONE_API_KEY)
index_name = "cuschatai"
pinecone_index = pinecone_client.Index(index_name)
vector_store = PineconeVectorStore(pinecone_index)

# Retriever and Query Engine setup
index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
retriever = VectorIndexRetriever(index=index, similarity_top_k=5)

# Custom prompt template
prompt_template = (
    "You are a friendly and efficient assistant 🤖. Keep answers short and clear, always with a warm emoji.\n\n"
    "Context:\n"
    "#####################################\n"
    "{context_str}\n"
    "Question: {query_str}\n\n"
    "If it's about appointments, suggest a time 🗓️ and ask if the user wants to confirm ✅. "
    "If it's about services, answer briefly. If it’s something unrelated, respond concisely with a helpful emoji 😊."
)
qa_template = PromptTemplate(template=prompt_template)
response_synthesizer = get_response_synthesizer(
    llm=client, text_qa_template=qa_template, response_mode="compact"
)
query_engine = RetrieverQueryEngine(
    retriever=retriever, response_synthesizer=response_synthesizer
)

# Configurar logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# User state tracking
user_context = {}

# ==============
# HANDLERS
# ==============


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_context[user_id] = {}  # Reset user context

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
    elif data == "horarios":
        await query.edit_message_text(
            "⏰ Horarios: Lun-Vie 10am-6pm | Sáb 11am-3pm. ¿Quieres agendar?"
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

    # Assuming the bot already coordinated the date with the user
    # For simplicity, using a fixed date (you can replace with more advanced logic)
    appointment_date = datetime.datetime(
        2025, 4, 15, 15, 0
    )  # Example: April 15, 3:00 pm

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

    # ====================
    # 1. DETECCIÓN DE CANCELACIÓN POR TEXTO
    # ====================
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

    # ====================
    # 2. CONFIRMACIÓN DE CITA
    # ====================
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

    # ====================
    # 3. PROCESAR NUEVA FECHA
    # ====================
    parsed_date = dateparser.parse(message, settings={"PREFER_DATES_FROM": "future"})
    if parsed_date:
        # Aquí podrías agregar validación de horario disponible
        context_data["start_time"] = parsed_date
        context_data["pending_confirmation"] = True
        await update.message.reply_text(
            f"✅ I found the date: {parsed_date.strftime('%A, %B %d at %I:%M %p')}.\n\nDo you confirm this appointment?"
        )
        return

    # ====================
    # 4. CONSULTA GENERAL / DEFAULT
    # ====================
    response = query_engine.query(message)
    await update.message.reply_text(str(response))


# ==============
# MAIN
# ==============

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CallbackQueryHandler(handle_cancel_appointment, pattern="cancelar"))
    app.add_handler(
        CallbackQueryHandler(handle_schedule_appointment, pattern="agendar")
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

    print("Bot stopped.")
