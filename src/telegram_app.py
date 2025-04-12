import os
import asyncio
from dotenv import load_dotenv
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
# CONFIGURACIÓN
# ==============

# Cargar variables de entorno
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configuración del modelo y embeddings
client = OpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY, temperature=0)
embedding = OpenAIEmbedding(model="text-embedding-ada-002")
Settings.llm = client
Settings.embed_model = embedding
Settings.chunk_size_limit = 1536

# Conexión a Pinecone
pinecone_client = Pinecone(api_key=PINECONE_API_KEY)
index_name = "cuschatai"
pinecone_index = pinecone_client.Index(index_name)
vector_store = PineconeVectorStore(pinecone_index)

# Configuración de Retriever y Query Engine
index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
retriever = VectorIndexRetriever(index=index, similarity_top_k=5)

# Prompt personalizado
prompt_template = (
    "You are a helpful and friendly chatbot specialized in providing customer support and scheduling appointments. 😊 "
    "You assist customers by answering their inquiries clearly and concisely, and you help them schedule appointments based on their needs. "
    "Please ensure the conversation is engaging and informative! 😄\n\n"
    "Context:\n"
    "#####################################\n"
    "{context_str}\n"
    "Answer the user's question: {query_str}\n\n"
    "If the question is related to our services or products, provide a detailed answer along with a summary. If the customer wants to schedule an appointment, "
    "assist them in finding a suitable time and book it for them.\n\n"
    "For appointment scheduling, please consider the following:\n"
    "- **Available Time Slots**: {available_times}\n"
    "- **Location**: {location}\n"
    "- **Required Information**: {required_info}\n\n"
    "However, if the question is unrelated to the services or scheduling, provide a direct and concise answer without any summary or extra details.\n\n"
    "Don't forget to invite the customer to schedule an appointment by highlighting the value of seeing the products in person and experiencing them firsthand. "
    "Encourage the customer to book an appointment at our office, mentioning that it's a great opportunity to get personalized advice and explore all available options. "
    "For example, you can say: 'Would you like to visit our office and see the products in person? We have some excellent time slots available this week!'"
)
qa_template = PromptTemplate(template=prompt_template)
response_synthesizer = get_response_synthesizer(
    llm=client, text_qa_template=qa_template, response_mode="compact"
)
query_engine = RetrieverQueryEngine(
    retriever=retriever, response_synthesizer=response_synthesizer
)

# Estado por usuario
user_context = {}

# ==============
# HANDLERS
# ==============


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_context[user_id] = {}  # Reiniciar contexto del usuario

    keyboard = [
        [InlineKeyboardButton("📅 Agendar Cita", callback_data="agendar")],
        [InlineKeyboardButton("📍 Ver Horarios", callback_data="horarios")],
        [InlineKeyboardButton("💬 Contactar Humano", callback_data="humano")],
        [InlineKeyboardButton("❌ Cancelar Cita", callback_data="cancelar")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        "¡Hola! 👋 Soy *CusChatAI*, tu asistente virtual.\n\n"
        "Estoy aquí para ayudarte con tus preguntas o para agendar una cita contigo.\n"
        "Selecciona una opción del menú para comenzar 👇"
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
            "🗓️ ¡Genial! Para agendar una cita, por favor indícame tu disponibilidad o pregunta por los horarios."
        )
    elif data == "horarios":
        await query.edit_message_text(
            "📍 Nuestros horarios disponibles son:\n- Lunes a Viernes: 10am - 6pm\n- Sábado: 11am - 3pm\n\n¿Te gustaría reservar alguno?"
        )
    elif data == "humano":
        await query.edit_message_text(
            "💬 Un agente humano se pondrá en contacto contigo pronto. Mientras tanto, puedes preguntarme cualquier cosa."
        )


async def handle_agendar_cita(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # Suponiendo que el bot ya coordinó la fecha con el usuario
    # Por simplicidad, fija una fecha (esto lo puedes cambiar por lógica más avanzada)
    fecha_cita = datetime.datetime(2025, 4, 15, 15, 0)  # Ejemplo: 15 de abril, 3:00 pm

    try:
        event_id = create_event(
            summary="Cita con cliente de Telegram",
            description=f"Agendada por usuario {user_id} desde el bot",
            start_time=fecha_cita,
            duration_minutes=30,
        )
        user_context[user_id]["event_id"] = event_id
        await query.edit_message_text("✅ ¡Tu cita ha sido agendada correctamente!")
    except Exception as e:
        print(e)
        await query.edit_message_text(
            "❌ Ocurrió un error al agendar tu cita. Intenta más tarde."
        )


async def handle_cancelar_cita(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    event_id = user_context.get(user_id, {}).get("event_id")

    if event_id:
        try:
            delete_event(event_id)
            await query.edit_message_text("🗑️ Tu cita ha sido cancelada correctamente.")
        except Exception as e:
            print(e)
            await query.edit_message_text("❌ Hubo un problema al cancelar la cita.")
    else:
        await query.edit_message_text(
            "No tienes ninguna cita programada para cancelar."
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message_text = update.message.text

    # Puedes añadir aquí lógica para manejar estados o contexto

    # Consultar al motor de búsqueda
    response = query_engine.query(message_text)
    await update.message.reply_text(str(response))


# ==============
# MAIN
# ==============

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CallbackQueryHandler(handle_cancelar_cita, pattern="cancelar"))
    app.add_handler(CallbackQueryHandler(handle_agendar_cita, pattern="agendar"))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    asyncio.run(app.run_polling())

    print("Bot stopped.")
