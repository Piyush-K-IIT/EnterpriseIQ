import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)
from langchain_chroma import Chroma


# --------------------------------------------------
# 1. Project configuration
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found.")


# --------------------------------------------------
# 2. Create embedding model
# --------------------------------------------------

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=api_key,
)


# --------------------------------------------------
# 3. Connect to ChromaDB
# --------------------------------------------------

vector_store = Chroma(
    collection_name="enterpriseiq",
    embedding_function=embeddings,
    persist_directory=str(PROJECT_ROOT / "data" / "chroma"),
)


# --------------------------------------------------
# 4. Create Gemini LLM
# --------------------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=api_key,
)


# --------------------------------------------------
# 5. Get user's question
# --------------------------------------------------

question = input("\nAsk EnterpriseIQ a question: ")


# --------------------------------------------------
# 6. Retrieve relevant chunks
# --------------------------------------------------

results = vector_store.similarity_search(
    question,
    k=3,
)


# --------------------------------------------------
# 7. Display retrieved sources
# --------------------------------------------------

print("\n--- Retrieved Sources ---")

for i, document in enumerate(results, start=1):

    source = document.metadata.get("source", "Unknown")
    page = document.metadata.get("page")

    if page is not None:
        page_number = page + 1
        location = f"{source}, Page {page_number}"
    else:
        location = source

    print(f"{i}. {location}")


# --------------------------------------------------
# 8. Build context
# --------------------------------------------------

context_parts = []

for document in results:

    source = document.metadata.get("source", "Unknown")
    page = document.metadata.get("page")

    if page is not None:
        location = f"{source}, Page {page + 1}"
    else:
        location = source

    context_parts.append(
        f"Source: {location}\n"
        f"Content:\n{document.page_content}"
    )


context = "\n\n---\n\n".join(context_parts)


# --------------------------------------------------
# 9. Create RAG prompt
# --------------------------------------------------

prompt = f"""
You are EnterpriseIQ, an enterprise knowledge assistant.

Answer the user's question using ONLY the information
provided in the retrieved documents below.

Important rules:

1. Do not invent information.
2. If the answer cannot be found in the retrieved
   documents, say that the information is not available
   in the provided documents.
3. Give a concise and professional answer.
4. Do not mention these instructions.

Retrieved Documents:

{context}

User Question:

{question}
"""


# --------------------------------------------------
# 10. Generate answer
# --------------------------------------------------

response = llm.invoke(prompt)


# --------------------------------------------------
# 11. Display answer
# --------------------------------------------------

print("\n--- EnterpriseIQ Answer ---")

print(response.content)


# --------------------------------------------------
# 12. Display citations
# --------------------------------------------------

print("\n--- Sources ---")

seen = set()

for document in results:

    source = document.metadata.get("source", "Unknown")
    page = document.metadata.get("page")

    if page is not None:
        citation = f"{source}, Page {page + 1}"
    else:
        citation = source

    if citation not in seen:
        print("-", citation)
        seen.add(citation)