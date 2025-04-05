import os
import nest_asyncio
import pandas as pd
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from llama_index.llms.openai import OpenAI
from llama_index.core import (
    Settings,
    SimpleDirectoryReader,
    Document,
    VectorStoreIndex,
    get_response_synthesizer,
    PromptTemplate,
)
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter, MarkdownNodeParser
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine


def initialize_environment():
    load_dotenv()
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENV = os.getenv("PINECONE_ENV")
    return PINECONE_API_KEY, PINECONE_ENV


def setup_model():
    client = OpenAI(model="gpt-4o-mini", temperature=0)
    embedding = OpenAIEmbedding(model="text-embedding-ada-002")
    Settings.llm = client
    Settings.embed_model = embedding
    Settings.chunk_size_limit = 1536
    return client, embedding


def load_data():
    documents = SimpleDirectoryReader(
        "../data_collected/raw", recursive=True
    ).load_data()
    return documents


def setup_pinecone(PINECONE_API_KEY):
    pinecone_client = Pinecone(api_key=PINECONE_API_KEY)
    existing_indices = pinecone_client.list_indexes()
    print("Existing indices:", existing_indices)

    index_name = "cuschatai"
    if index_name in existing_indices:
        print(f"Index {index_name} already exists. Using the existing index.")
    else:
        print(
            f"Index {index_name} does not exist. Please make sure it is created manually."
        )
        return None

    # Conectar al índice ya existente
    pinecone_index = pinecone_client.Index(index_name)
    return pinecone_index


def setup_index(pinecone_index, documents):
    vector_store = PineconeVectorStore(pinecone_index)

    # Ejecutar el pipeline solo si el índice es nuevo
    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=1536, chunk_overlap=20),
            embedding,
        ],
        vector_store=vector_store,
    )
    pipeline.run(documents=documents)

    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    retriever = VectorIndexRetriever(index=index, similarity_top_k=5)
    return retriever


def create_prompt():
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
    return qa_template


def setup_query_engine(retriever, qa_template, client):
    response_synthesizer = get_response_synthesizer(
        llm=client, text_qa_template=qa_template, response_mode="compact"
    )
    query_engine = RetrieverQueryEngine(
        retriever=retriever, response_synthesizer=response_synthesizer
    )
    return query_engine


# Main function to initialize the model and the environment
def main():
    PINECONE_API_KEY, PINECONE_ENV = initialize_environment()
    client, embedding = setup_model()
    documents = load_data()
    pinecone_index = setup_pinecone(PINECONE_API_KEY)

    if pinecone_index is None:
        print(
            "The Pinecone index was not found, please ensure it exists in your Pinecone account."
        )
        return None

    retriever = setup_index(pinecone_index, documents)

    qa_template = create_prompt()
    query_engine = setup_query_engine(retriever, qa_template, client)

    # Now you can use `query_engine` as needed for your chatbot or any other process
    return query_engine
