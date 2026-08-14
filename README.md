# 🤖 RAG Chatbot

A document-based Retrieval-Augmented Generation (RAG) chatbot that allows users to upload a PDF and ask questions about its contents.

The system retrieves the most relevant sections from the uploaded document and provides them as context to a locally running Qwen3:4B language model through Ollama.

The application is built with Python, LangChain, ChromaDB, Hugging Face embeddings, Ollama, and Streamlit.

---

## 🚀 Features

- 📄 Upload PDF documents directly through the application
- ✂️ Recursive text chunking
- 🧠 Semantic embeddings using Hugging Face
- 🗄️ Persistent vector storage using ChromaDB
- 🔎 Top-K similarity-based retrieval
- 🤖 Local LLM inference using Qwen3:4B
- ⚡ Ollama-based local model execution
- 📚 Source page references
- 🔄 Support for different uploaded PDF documents
- 🌐 Simple Streamlit interface

---

# 🏗️ Architecture

```text
                    ┌──────────────────┐
                    │   PDF Upload     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   PyPDFLoader    │
                    │  Text Extraction │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Recursive        │
                    │ Text Splitter    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Hugging Face     │
                    │ Embeddings       │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    ChromaDB      │
                    │ Vector Database  │
                    └────────┬─────────┘
                             │
                     User Question
                             │
                             ▼
                    ┌──────────────────┐
                    │ Similarity Search │
                    │    Top-K = 2     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Retrieved Context│
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Qwen3:4B       │
                    │   via Ollama     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Grounded Answer  │
                    │ + Source Pages   │
                    └──────────────────┘

🔄 How the RAG Pipeline Works

The chatbot follows a Retrieval-Augmented Generation workflow.

1. PDF Upload

The user uploads a PDF through the Streamlit interface.

2. Document Loading

PyPDFLoader extracts the text and metadata from the PDF.

3. Text Chunking

The extracted text is divided into smaller chunks using RecursiveCharacterTextSplitter.

Current configuration:

Chunk size: 1000
Chunk overlap: 200

The overlap helps preserve context between neighboring chunks.

4. Embedding Generation

Each chunk is converted into a numerical vector using:

sentence-transformers/all-MiniLM-L6-v2

These embeddings allow the system to compare the semantic meaning of the user's question with document content.

5. Vector Storage

The embeddings and their corresponding document chunks are stored in ChromaDB.

The vector database is persisted locally so that previously processed documents do not have to be embedded again unnecessarily.

6. Retrieval

When the user asks a question, the system performs semantic similarity search and retrieves the top 2 relevant chunks.

7. Context Construction

The retrieved chunks are combined into a context that is passed to the language model.

8. Local LLM Generation

The context and question are sent to:

Qwen3:4B

running locally through:

Ollama
9. Grounded Response

The model generates an answer using the retrieved document context.

The application also displays the source pages used to generate the response.

🧠 Why RAG?

Instead of retraining a language model every time a new document is provided, RAG separates knowledge retrieval from language generation.

New PDF
   ↓
Chunk
   ↓
Embed
   ↓
Store
   ↓
Retrieve relevant information
   ↓
Give context to LLM

This allows the same language model to work with different documents without retraining the model.

🛠️ Tech Stack
Technology	Purpose
Python	Core programming language
Streamlit	Web application interface
LangChain	RAG pipeline orchestration
PyPDF	PDF document loading
RecursiveCharacterTextSplitter	Text chunking
Hugging Face	Text embeddings
ChromaDB	Vector database
Ollama	Local LLM runtime
Qwen3:4B	Local language model
💻 Installation
1. Clone the repository
git clone https://github.com/irshadahmedr3dev/RAG-Chatbot.git

Navigate into the project:

cd RAG-Chatbot
2. Install Python dependencies
pip install -r requirements.txt
3. Install Ollama

Install Ollama on your system and make sure it is available from the terminal.

Then download the Qwen3:4B model:

ollama pull qwen3:4b

You can verify the model is available with:

ollama list
▶️ Running the Application

Start the Streamlit application:

streamlit run app.py

The application will open in your browser.

📚 Usage
Step 1

Upload a PDF using the file uploader.

Step 2

Wait for the document to be processed.

The system:

PDF
 ↓
Text extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
ChromaDB
Step 3

Ask a question about the uploaded document.

Step 4

The system retrieves the most relevant chunks.

Step 5

Qwen3:4B generates an answer using the retrieved context.

Step 6

The application displays the answer together with the source pages.

🔐 Local AI Processing

The language model used by this project runs locally through Ollama.

User Question
      ↓
ChromaDB Retrieval
      ↓
Relevant Context
      ↓
Qwen3:4B
      ↓
Ollama
      ↓
Local Response

No external LLM API key is required for the generation step.

📂 Project Structure
RAG-Chatbot/
│
├── screenshots/
│   ├── rag-pipeline.png
│   └── local-llm.png
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore

Runtime-generated directories such as uploaded documents and the local vector database are excluded from Git using .gitignore.

🎯 Project Objectives

This project was developed to understand and implement a complete Retrieval-Augmented Generation pipeline from the ground up.

The main objectives were:

Understand document ingestion
Implement document chunking
Generate semantic embeddings
Store embeddings in a vector database
Implement similarity-based retrieval
Connect retrieved context to an LLM
Run an LLM locally
Build a usable document-question-answering application
🚧 Future Improvements

Potential future improvements include:

Conversation memory
Improved document management
Multiple-document collections
Retrieval score visualization
Better chunking strategies
Streaming LLM responses
Retrieval evaluation
RAG performance benchmarking
Support for additional document formats
Improved error handling
📌 Project Status

Completed

The current implementation includes:

PDF upload
Document processing
Text chunking
Embedding generation
Persistent ChromaDB storage
Semantic retrieval
Local Qwen3:4B inference
Source attribution
Streamlit interface
👨‍💻 Author

Irshad Ahmed