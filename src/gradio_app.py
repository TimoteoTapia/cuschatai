# app.py
import os
import gradio as gr
from dotenv import load_dotenv
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

# Cargar variables de entorno
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")

# Configuración del cliente OpenAI y modelos
client = OpenAI(model="gpt-4o-mini", temperature=0)
embedding = OpenAIEmbedding(model="text-embedding-ada-002")
Settings.llm = client
Settings.embed_model = embedding
Settings.chunk_size_limit = 1536

# Conectarse al índice existente en Pinecone
pinecone_client = Pinecone(api_key=PINECONE_API_KEY)
index_name = "cuschatai"
pinecone_index = pinecone_client.Index(index_name)
vector_store = PineconeVectorStore(pinecone_index)

# Crear índice desde vector store
index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
retriever = VectorIndexRetriever(index=index, similarity_top_k=5)

# Template personalizado
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


# Función para consultar el modelo
def get_model_response(query):
    response = query_engine.query(query)
    return str(response)


# Interfaz con Gradio
iface = gr.Interface(
    fn=get_model_response,
    inputs=gr.Textbox(lines=3, placeholder="Escribe tu pregunta aquí..."),
    outputs="text",
    title="CusChatAI 🤖",
    description="Asistente especializado en atención al cliente y agendado de citas.",
)

if __name__ == "__main__":
    iface.launch()
