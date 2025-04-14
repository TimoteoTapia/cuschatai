# app/config.py
import os
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import (
    Settings,
    VectorStoreIndex,
    get_response_synthesizer,
    PromptTemplate,
)
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from pinecone import Pinecone


# ============== CONFIGURATION ==============
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
    "If it's about services, answer briefly. If it is something unrelated, respond concisely with a helpful emoji 😊."
)
qa_template = PromptTemplate(template=prompt_template)
response_synthesizer = get_response_synthesizer(
    llm=client, text_qa_template=qa_template, response_mode="compact"
)
query_engine = RetrieverQueryEngine(
    retriever=retriever, response_synthesizer=response_synthesizer
)
