import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma


# --------------------------------------------------
# 1. Load environment variables
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found.")


# --------------------------------------------------
# 2. Load the document
# --------------------------------------------------

document_path = PROJECT_ROOT / "documents" / "company_policy.txt"

with open(document_path, "r", encoding="utf-8") as file:
    text = file.read()


document = Document(
    page_content=text,
    metadata={
        "source": "company_policy.txt"
    }
)


# --------------------------------------------------
# 3. Split the document into chunks
# --------------------------------------------------

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents([document])

print(f"Created {len(chunks)} chunks.")


# --------------------------------------------------
# 4. Create embeddings
# --------------------------------------------------

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=api_key
)


# --------------------------------------------------
# 5. Store embeddings in ChromaDB
# --------------------------------------------------

vector_store = Chroma(
    collection_name="enterpriseiq",
    embedding_function=embeddings,
    persist_directory=str(PROJECT_ROOT / "data" / "chroma")
)


# --------------------------------------------------
# 6. Add documents to the vector database
# --------------------------------------------------

vector_store.add_documents(chunks)

print("Documents successfully added to ChromaDB.")
