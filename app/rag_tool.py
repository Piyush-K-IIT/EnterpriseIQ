from pathlib import Path

from langchain_core.tools import tool
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CHROMA_DIR = PROJECT_ROOT / "data" / "chroma"


# =========================================================
# LOCAL EMBEDDING MODEL
# =========================================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# =========================================================
# VECTOR STORE
# =========================================================

def get_vector_store():
    """
    Create/open the EnterpriseIQ Chroma vector store.
    """

    return Chroma(
        collection_name="enterpriseiq",
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR),
    )


# =========================================================
# RAG SEARCH TOOL
# =========================================================

@tool
def search_documents(question: str) -> str:
    """
    Search indexed EnterpriseIQ PDF documents.

    Use this tool when the user asks about information
    contained in the indexed documents.
    """

    vector_store = get_vector_store()

    results_with_scores = (
        vector_store.similarity_search_with_score(
            question,
            k=5
        )
    )

    if not results_with_scores:
        return (
            "No relevant information was found "
            "in the company documents."
        )

    context = []

    source_number = 1

    for document, score in results_with_scores:

        source = document.metadata.get(
            "source",
            "Unknown"
        )

        page = document.metadata.get(
            "page"
        )

        if page is not None:

            location = (
                f"{source}, "
                f"Page {page + 1}"
            )

        else:

            location = source

        context.append(
            f"[SOURCE {source_number}]\n"
            f"{location}\n"
            f"Similarity Score: {score:.4f}\n\n"
            f"{document.page_content}"
        )

        source_number += 1

    return "\n\n---\n\n".join(context)