# EnterpriseIQ

### AI-Powered Enterprise Knowledge & Support Agent

EnterpriseIQ is an AI-powered enterprise assistant that combines **LLM-based reasoning, Retrieval-Augmented Generation (RAG), vector search, and tool calling** to answer questions from enterprise documents, perform calculations, and create support tickets.

---

## 🚀 Features

- 📚 **Document RAG** — Ask questions about uploaded enterprise documents.
- 🤖 **AI Agent** — Uses LangGraph to orchestrate reasoning and tool execution.
- 🔎 **Semantic Search** — Retrieves relevant document chunks using ChromaDB.
- 🧠 **Local Embeddings** — Uses Sentence Transformers for document embeddings.
- 🧮 **Calculator Tool** — Performs mathematical calculations safely.
- 🎫 **Support Ticket Tool** — Creates support tickets with unique ticket IDs.
- 📄 **PDF Ingestion** — Upload and index new PDF documents through the UI.
- 🔄 **Dynamic Re-indexing** — Rebuild the knowledge base when documents change.
- 📑 **Source Attribution** — Displays the document and page used for retrieved information.
- 💬 **Interactive Chat UI** — Built with Streamlit.

---

## 🏗️ System Architecture


                         ┌─────────────────────┐
                         │     Streamlit UI    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    LangGraph Agent  │
                         │      + Gemini       │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
             ┌────────────┐  ┌────────────┐  ┌──────────────┐
             │ Document   │  │ Calculator │  │   Support    │
             │ Search     │  │   Tool     │  │ Ticket Tool  │
             └─────┬──────┘  └────────────┘  └──────────────┘
                   │
                   ▼
             ┌────────────┐
             │ ChromaDB   │
             │ Vector DB  │
             └─────┬──────┘
                   │
                   ▼
        ┌──────────────────────┐
        │ Sentence Transformer │
        │     Embeddings       │
        └──────────────────────┘



🔄 RAG Pipeline

EnterpriseIQ uses a Retrieval-Augmented Generation pipeline to ground responses in indexed documents.

PDF Documents
      │
      ▼
PDF Loader
      │
      ▼
Text Splitting
      │
      ▼
Sentence Transformer Embeddings
      │
      ▼
ChromaDB
      │
      ▼
User Question
      │
      ▼
Semantic Retrieval
      │
      ▼
Relevant Context
      │
      ▼
Gemini
      │
      ▼
Grounded Answer + Sources


🛠️ Tech Stack


----------------------------------------------------
| Technology            | Purpose                  |
| --------------------- | ------------------------ |
| Python                | Application development  |
| Gemini                | Large Language Model     |
| LangGraph             | AI agent orchestration   |
| LangChain             | LLM and tool integration |
| ChromaDB              | Vector database          |
| Sentence Transformers | Local text embeddings    |
| Streamlit             | Web interface            |
| PyPDF                 | PDF document loading     |
| GitHub Actions        | CI validation            |




📁 Project Structure


EnterpriseIQ/
│
├── app/
│   ├── agent.py          # LangGraph AI agent
│   ├── ingest.py         # PDF ingestion and indexing
│   ├── main.py           # Streamlit application
│   ├── rag_tool.py       # Document retrieval tool
│   └── tools.py          # Calculator and support-ticket tools
│
├── documents/
│   ├── company_policy.txt
│   ├── employee_handbook.pdf
│   ├── it_security_policy.pdf
│   └── travel_policy.pdf
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .gitignore
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── create_pdfs.py
└── README.md


⚙️ Installation

1. Clone the repository
git clone https://github.com/Piyush-K-IIT/EnterpriseIQ.git
cd EnterpriseIQ
2. Create a virtual environment
python3 -m venv venv

Activate it:

macOS / Linux

source venv/bin/activate

Windows

venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Configure the Gemini API key

Create a .env file in the project root:

GEMINI_API_KEY=your_api_key_here

Do not commit the .env file.

5. Run the application
streamlit run app/main.py

The application will open in your browser.

💡 Example Queries
📚 Document Search
What is the annual leave entitlement?
What are the company's password requirements?
What is the maximum hotel reimbursement for domestic travel?
🧮 Calculator
Calculate 6000 * 3 + 1200
🎫 Support Ticket
Create a support ticket for my laptop not connecting to Wi-Fi.
🔗 Multi-Tool Query
What is the hotel reimbursement limit for three nights?
Calculate the total reimbursement.
📄 Adding Documents

EnterpriseIQ allows users to upload PDF documents directly through the Streamlit interface.

Upload PDF
     │
     ▼
Save Document
     │
     ▼
Extract Text
     │
     ▼
Split into Chunks
     │
     ▼
Generate Embeddings
     │
     ▼
Store in ChromaDB
     │
     ▼
Ready for Retrieval

After indexing, users can immediately ask questions about the newly added documents.

🔧 Agent Tools

EnterpriseIQ currently provides three tools to the AI agent.

1. Document Search

Retrieves relevant information from the indexed enterprise documents.

search_documents(question)
2. Calculator

Performs mathematical expressions using a restricted AST-based evaluator.

calculate(expression)
3. Support Ticket

Creates a support ticket for an employee issue.

create_support_ticket(issue)

The LangGraph agent decides when a tool is required and executes the appropriate tool.

🔐 Security
API credentials are stored using environment variables.
.env is excluded using .gitignore.
The calculator uses a restricted AST-based evaluator instead of unrestricted code execution.
Uploaded documents are processed through the controlled ingestion pipeline.
🧪 CI

GitHub Actions is configured to perform basic project validation.

The CI workflow:

Installs project dependencies.
Sets up the Python environment.
Compiles the application modules to detect syntax errors.
Runs automatically on pushes and pull requests to the main branch.
🚀 Future Improvements

Potential future improvements include:

Improved RAG retrieval and re-ranking
Automated RAG evaluation
Conversation memory
Authentication and role-based access
Streaming responses
Production observability
Cloud deployment
Persistent production vector storage
👨‍💻 Author

Piyush Kumar

B.Tech. Mathematics & Computing
Indian Institute of Technology Mandi

📄 License

This project is intended for educational and portfolio purposes.
