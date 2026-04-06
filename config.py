"""
config.py — Shared model, embeddings, and vectorstore setup.
All other modules import from here to avoid re-initialisation.
"""

from langchain_mistralai import ChatMistralAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from dotenv import load_dotenv
load_dotenv()


# LLM
model = ChatMistralAI(model_name="mistral-large-2512")

# Embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

# Semantic cache vectorstore
VECTORSTORE = PineconeVectorStore(
    index_name="research-agent-semantic-cache",
    embedding=embeddings,
)

# Minimum cosine similarity to cache hit
CACHE_DISTANCE = 0.7
