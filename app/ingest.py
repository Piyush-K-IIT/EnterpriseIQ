import shutil
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DOCUMENTS_DIR = PROJECT_ROOT / "documents"
CHROMA_DIR = PROJECT_ROOT / "data" / "chroma"
STAGING_DIR = PROJECT_ROOT / "data" / "chroma_staging"


DOCUMENTS_DIR.mkdir(
    exist_ok=True
)

CHROMA_DIR.parent.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# EMBEDDING MODEL
# =========================================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# =========================================================
# TEXT SPLITTER
# =========================================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
)


# =========================================================
# INGEST DOCUMENTS
# =========================================================

def ingest_documents():

    pdf_files = sorted(
        DOCUMENTS_DIR.glob("*.pdf")
    )

    if not pdf_files:

        return {
            "success": False,
            "message": "No PDF files found.",
            "files": [],
            "chunks": 0,
        }


    # =====================================================
    # REMOVE OLD STAGING DATABASE
    # =====================================================

    if STAGING_DIR.exists():

        try:
            shutil.rmtree(
                STAGING_DIR
            )

        except Exception as e:

            return {
                "success": False,
                "message": (
                    "Could not clean the temporary "
                    f"Chroma directory: {e}"
                ),
                "files": [],
                "chunks": 0,
            }


    STAGING_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


    # =====================================================
    # CREATE NEW CHROMA DATABASE
    # =====================================================

    vector_store = Chroma(
        collection_name="enterpriseiq",
        embedding_function=embeddings,
        persist_directory=str(
            STAGING_DIR
        ),
    )


    all_chunks = []


    # =====================================================
    # PROCESS PDFs
    # =====================================================

    for pdf_file in pdf_files:

        print(
            f"Processing: {pdf_file.name}"
        )

        loader = PyPDFLoader(
            str(pdf_file)
        )

        pages = loader.load()

        chunks = text_splitter.split_documents(
            pages
        )


        for chunk in chunks:

            chunk.metadata[
                "source"
            ] = pdf_file.name


        all_chunks.extend(
            chunks
        )


        print(
            f"  Pages: {len(pages)}"
        )

        print(
            f"  Chunks: {len(chunks)}"
        )


    # =====================================================
    # ADD DOCUMENTS TO NEW DATABASE
    # =====================================================

    if all_chunks:

        vector_store.add_documents(
            all_chunks
        )


    # =====================================================
    # CLOSE LOCAL VECTOR STORE REFERENCE
    # =====================================================

    del vector_store


    # =====================================================
    # SWAP DATABASES
    # =====================================================

    backup_dir = (
        PROJECT_ROOT
        / "data"
        / "chroma_backup"
    )


    try:

        # Remove previous backup if possible
        if backup_dir.exists():

            try:

                shutil.rmtree(
                    backup_dir
                )

            except Exception:

                # If an old Chroma connection still
                # holds the backup, leave it alone.
                backup_dir = (
                    PROJECT_ROOT
                    / "data"
                    / "chroma_backup_new"
                )

                if backup_dir.exists():

                    shutil.rmtree(
                        backup_dir
                    )


        # -------------------------------------------------
        # Move current database out of the way
        # -------------------------------------------------

        if CHROMA_DIR.exists():

            CHROMA_DIR.rename(
                backup_dir
            )


        # -------------------------------------------------
        # Move new database into place
        # -------------------------------------------------

        STAGING_DIR.rename(
            CHROMA_DIR
        )


    except Exception as e:

        # -------------------------------------------------
        # Attempt recovery
        # -------------------------------------------------

        if (
            not CHROMA_DIR.exists()
            and backup_dir.exists()
        ):

            backup_dir.rename(
                CHROMA_DIR
            )


        if STAGING_DIR.exists():

            shutil.rmtree(
                STAGING_DIR,
                ignore_errors=True
            )


        return {
            "success": False,
            "message": (
                "Could not replace the Chroma "
                f"database: {e}"
            ),
            "files": [],
            "chunks": 0,
        }


    # =====================================================
    # SUCCESS
    # =====================================================

    return {
        "success": True,
        "message": (
            f"Successfully indexed "
            f"{len(pdf_files)} PDF files."
        ),
        "files": [
            pdf.name
            for pdf in pdf_files
        ],
        "chunks": len(
            all_chunks
        ),
    }


# =========================================================
# COMMAND-LINE EXECUTION
# =========================================================

if __name__ == "__main__":

    result = ingest_documents()

    print(
        "\n" + "=" * 50
    )

    print(
        result["message"]
    )

    print(
        f"Chunks indexed: "
        f"{result['chunks']}"
    )

    print(
        "\nDocuments:"
    )

    for file in result["files"]:

        print(
            f" - {file}"
        )

    print(
        "=" * 50
    )