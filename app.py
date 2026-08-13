import os
import hashlib

import streamlit as st

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖"
)


# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("🤖 RAG Chatbot")

st.write(
    "Upload a PDF and ask questions about its contents."
)


# --------------------------------------------------
# Upload PDF
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload your PDF",
    type=["pdf"]
)


# --------------------------------------------------
# Load models
# --------------------------------------------------

@st.cache_resource
def load_embeddings():

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


@st.cache_resource
def load_llm():

    return ChatOllama(
        model="qwen3:4b"
    )


embeddings = load_embeddings()
llm = load_llm()


# --------------------------------------------------
# Process PDF
# --------------------------------------------------

if uploaded_file is not None:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    pdf_bytes = uploaded_file.getvalue()

    # Create unique ID for the uploaded PDF
    file_hash = hashlib.md5(
        pdf_bytes
    ).hexdigest()

    # Create required folders
    os.makedirs(
        "uploads",
        exist_ok=True
    )

    os.makedirs(
        "chroma_db",
        exist_ok=True
    )

    # Save uploaded PDF
    pdf_path = os.path.join(
        "uploads",
        uploaded_file.name
    )

    with open(
        pdf_path,
        "wb"
    ) as f:

        f.write(pdf_bytes)

    # Unique database for this PDF
    db_path = os.path.join(
        "chroma_db",
        file_hash
    )


    # --------------------------------------------------
    # Load or create vector database
    # --------------------------------------------------

    if os.path.exists(db_path):

        vectorstore = Chroma(
            collection_name="documents",
            embedding_function=embeddings,
            persist_directory=db_path
        )

        st.info(
            "Loaded existing vector database."
        )

    else:

        with st.spinner(
            "Processing PDF and creating embeddings..."
        ):

            # Load PDF
            loader = PyPDFLoader(
                pdf_path
            )

            documents = loader.load()


            # Split into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )

            chunks = text_splitter.split_documents(
                documents
            )


            # Create vector database
            vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=embeddings,
                collection_name="documents",
                persist_directory=db_path
            )

        st.success(
            f"PDF processed successfully — "
            f"{len(chunks)} chunks created."
        )


    # --------------------------------------------------
    # Question input
    # --------------------------------------------------

    question = st.text_input(
        "Ask a question about your PDF:"
    )


    if question:

        with st.spinner(
            "Thinking..."
        ):

            # Retrieve relevant chunks
            results = vectorstore.similarity_search(
                question,
                k=2
            )


            # Combine retrieved chunks
            context = "\n\n".join(
                result.page_content
                for result in results
            )


            # Create prompt
            prompt = f"""
Answer the question using only the context provided below.

Context:
{context}

Question:
{question}

If the answer is not present in the context,
say that the information is not available
in the provided document.
"""


            # Generate answer
            response = llm.invoke(
                prompt
            )


        # --------------------------------------------------
        # Display answer
        # --------------------------------------------------

        st.subheader(
            "Answer"
        )

        st.write(
            response.content
        )


        # --------------------------------------------------
        # Display sources
        # --------------------------------------------------

        st.subheader(
            "Sources"
        )

        sources = []


        for result in results:

            page = result.metadata.get(
                "page"
            )

            if page is not None:

                source_name = os.path.basename(
                    result.metadata.get(
                        "source",
                        uploaded_file.name
                    )
                )

                source_info = (
                    f"📄 {source_name} — Page {page + 1}"
                )

                if source_info not in sources:

                    sources.append(
                        source_info
                    )


        for source in sources:

            st.write(
                source
            )