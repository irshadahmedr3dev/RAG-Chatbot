# RAG Chatbot

A document-based Retrieval-Augmented Generation (RAG) chatbot that allows users to upload a PDF and ask questions about its contents.

The application retrieves relevant sections from the uploaded document and provides them as context to a locally running Qwen3:4B language model.

## Features

- Upload PDF documents directly through the application
- Recursive text chunking
- Hugging Face embeddings
- Semantic similarity search using ChromaDB
- Persistent vector storage
- Top-k document retrieval
- Local LLM inference using Qwen3:4B and Ollama
- Source page references
- Streamlit interface

## Architecture

PDF
→ Text Extraction
→ Chunking
→ Embeddings
→ ChromaDB
→ Similarity Retrieval
→ Context Construction
→ Qwen3:4B
→ Grounded Answer
→ Source Pages

## Tech Stack

- Python
- LangChain
- Streamlit
- ChromaDB
- Hugging Face Embeddings
- Ollama
- Qwen3:4B
- PyPDF

## How It Works

1. The user uploads a PDF.
2. The PDF is loaded and divided into smaller chunks.
3. Each chunk is converted into an embedding.
4. The embeddings are stored in ChromaDB.
5. When the user asks a question, the most relevant chunks are retrieved.
6. The retrieved chunks are provided as context to Qwen3:4B.
7. The local LLM generates an answer based on the retrieved context.
8. The application displays the source pages used for the response.

## Installation

Clone the repository and install the required packages:

```bash
pip install -r requirements.txt