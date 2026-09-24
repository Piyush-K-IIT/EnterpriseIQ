from pathlib import Path
import sys
import subprocess

import streamlit as st

from agent import ask_agent


# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DOCUMENTS_DIR = PROJECT_ROOT / "documents"
CHROMA_DIR = PROJECT_ROOT / "data" / "chroma"
INGEST_SCRIPT = PROJECT_ROOT / "app" / "ingest.py"


DOCUMENTS_DIR.mkdir(exist_ok=True)


# =========================================================
# DOCUMENT INGESTION
# =========================================================

def run_ingestion():
    """
    Run the document ingestion pipeline in a separate
    Python process.

    This prevents Streamlit from holding a Chroma/SQLite
    connection while the database is being rebuilt.
    """

    result = subprocess.run(
        [sys.executable, str(INGEST_SCRIPT)],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            result.stderr.strip()
            or result.stdout.strip()
            or "Document indexing failed."
        )

    return result.stdout


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="EnterpriseIQ",
    page_icon="🤖",
    layout="wide",
)


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# HEADER
# =========================================================

st.title("EnterpriseIQ")

st.markdown(
    """
    **AI-Powered Enterprise Knowledge & Support Agent**

    Ask questions about company documents, perform
    calculations, or create support tickets.
    """
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("EnterpriseIQ")

    st.markdown(
        """
        ### Capabilities

        📚 **Document RAG**  
        Search indexed enterprise documents.

        🧮 **Calculator**  
        Perform mathematical calculations.

        🎫 **Support Tickets**  
        Create support tickets using the AI agent.
        """
    )

    st.divider()

    # =====================================================
    # PDF UPLOAD
    # =====================================================

    st.subheader("Add Documents")

    uploaded_files = st.file_uploader(
        "Upload PDF documents",
        type=["pdf"],
        accept_multiple_files=True,
    )

    if uploaded_files:

        if st.button(
            "Index Uploaded PDFs",
            use_container_width=True,
        ):

            try:

                # -----------------------------------------
                # Save uploaded files
                # -----------------------------------------

                saved_files = []

                for uploaded_file in uploaded_files:

                    destination = (
                        DOCUMENTS_DIR
                        / Path(uploaded_file.name).name
                    )

                    with open(
                        destination,
                        "wb",
                    ) as file:

                        file.write(
                            uploaded_file.getbuffer()
                        )

                    saved_files.append(
                        destination.name
                    )

                # -----------------------------------------
                # Rebuild Chroma database
                # -----------------------------------------

                with st.spinner(
                    "Rebuilding document index..."
                ):

                    output = run_ingestion()

                # -----------------------------------------
                # Success message
                # -----------------------------------------

                st.success(
                    "Documents indexed successfully."
                )

                # -----------------------------------------
                # Show ingestion details
                # -----------------------------------------

                with st.expander(
                    "Ingestion details"
                ):

                    st.code(
                        output
                    )

                # -----------------------------------------
                # Clear chat history
                # -----------------------------------------

                st.session_state.messages = []

                st.rerun()

            except Exception as e:

                st.error(
                    f"Upload failed: {e}"
                )

    # =====================================================
    # EXISTING DOCUMENTS
    # =====================================================

    st.divider()

    st.subheader("Indexed Documents")

    pdf_files = sorted(
        DOCUMENTS_DIR.glob("*.pdf")
    )

    if pdf_files:

        for pdf_file in pdf_files:

            st.write(
                f"📄 {pdf_file.name}"
            )

    else:

        st.info(
            "No PDF documents indexed."
        )

    # =====================================================
    # RE-INDEX BUTTON
    # =====================================================

    st.divider()

    if st.button(
        "Re-index All Documents",
        use_container_width=True,
    ):

        try:

            with st.spinner(
                "Rebuilding document index..."
            ):

                output = run_ingestion()

            st.success(
                "All documents re-indexed successfully."
            )

            with st.expander(
                "Ingestion details"
            ):

                st.code(
                    output
                )

            st.session_state.messages = []

            st.rerun()

        except Exception as e:

            st.error(
                f"Re-index failed: {e}"
            )


# =========================================================
# CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        # ---------------------------------------------
        # Tool information
        # ---------------------------------------------

        if (
            message["role"] == "assistant"
            and message.get("tools_used")
        ):

            st.caption(
                "Tools used: "
                + ", ".join(
                    message["tools_used"]
                )
            )

        # ---------------------------------------------
        # Sources
        # ---------------------------------------------

        if (
            message["role"] == "assistant"
            and message.get("sources")
        ):

            with st.expander(
                "Sources"
            ):

                for source in message[
                    "sources"
                ]:

                    st.write(
                        f"📄 {source}"
                    )


# =========================================================
# CHAT INPUT
# =========================================================

question = st.chat_input(
    "Ask EnterpriseIQ something..."
)


if question:

    # -----------------------------------------------------
    # Display user message
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message(
        "user"
    ):

        st.markdown(
            question
        )

    # -----------------------------------------------------
    # Run agent
    # -----------------------------------------------------

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "EnterpriseIQ is thinking..."
        ):

            try:

                result = ask_agent(
                    question
                )

                answer = result[
                    "answer"
                ]

                tools_used = result[
                    "tools_used"
                ]

                sources = result[
                    "sources"
                ]

                # -----------------------------------------
                # Answer
                # -----------------------------------------

                st.markdown(
                    answer
                )

                # -----------------------------------------
                # Tools
                # -----------------------------------------

                if tools_used:

                    st.caption(
                        "Tools used: "
                        + ", ".join(
                            tools_used
                        )
                    )

                # -----------------------------------------
                # Sources
                # -----------------------------------------

                if sources:

                    with st.expander(
                        "Sources"
                    ):

                        for source in sources:

                            st.write(
                                f"📄 {source}"
                            )

                # -----------------------------------------
                # Save assistant message
                # -----------------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "tools_used": tools_used,
                        "sources": sources,
                    }
                )

            except Exception as e:

                error_message = (
                    f"Error: {e}"
                )

                st.error(
                    error_message
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                        "tools_used": [],
                        "sources": [],
                    }
                )