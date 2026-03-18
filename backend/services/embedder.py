"""
embedder.py
===========
Converts resume text into vectors and stores
them in ChromaDB for later retrieval.

Why sentence-transformers (all-MiniLM-L6-v2)?
- Runs fully locally — no API calls needed
- Free to use — no quota or billing
- Small and fast — only 80MB model size
- Good quality for technical resume content

Why split text into chunks?
- LLMs have a maximum input size (token limit)
- Smaller chunks = more precise search results
- Each chunk covers one specific section of resume

Why ChromaDB?
- Purpose-built for storing and searching vectors
- Works locally — no external database needed
- Simple Python API — easy to use
"""

import uuid
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter


# ── Initialize embedding model ────────────────────────────────────────────────
# This runs ONCE when the file is imported
# Downloads the model on first run (~80MB) — takes 1-2 minutes
# After that it loads from cache instantly
print("Loading embedding model...")
EMBEDDING_MODEL = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)
print("Embedding model loaded ✅")

# Path where ChromaDB saves data on disk
VECTORSTORE_PATH = "data/vectorstore"


def _split_text(text: str) -> list:
    """
    Split resume text into smaller overlapping chunks.

    Why RecursiveCharacterTextSplitter?
    - Tries to split on paragraphs first, then sentences,
      then words — keeps meaning intact
    - Better than splitting by fixed character count

    chunk_size=500    → each chunk is ~500 characters
    chunk_overlap=50  → chunks overlap by 50 characters
                        so we don't cut sentences in half
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_text(text)
    return chunks


def create_temp_vectorstore(resume_text: str) -> Chroma:
    """
    Create a temporary in-memory vector store.

    Why temporary?
    - We only need it for one request
    - Faster than writing to disk
    - Gets deleted automatically after request is done

    Used by: question_gen.py (Day 5)

    Args:
        resume_text : full plain text of the resume

    Returns:
        ChromaDB vectorstore object ready for searching
    """
    # Split resume into chunks
    chunks = _split_text(resume_text)

    # Create unique collection name for this resume
    # uuid4() generates a random unique ID every time
    collection_name = f"temp_{uuid.uuid4().hex}"

    # Create ChromaDB from the chunks
    # from_texts() does two things:
    # 1. Converts each chunk to a vector using EMBEDDING_MODEL
    # 2. Stores all vectors in ChromaDB
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=EMBEDDING_MODEL,
        collection_name=collection_name
    )

    return vectorstore


def create_vectorstore(resume_text: str,
                       candidate_id: str) -> Chroma:
    """
    Create a persistent vector store saved to disk.

    Why persistent?
    - Useful if you want to reload the same resume later
    - Stored in data/vectorstore/ folder

    Args:
        resume_text  : full plain text of the resume
        candidate_id : unique ID to identify this candidate

    Returns:
        ChromaDB vectorstore object
    """
    chunks = _split_text(resume_text)

    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=EMBEDDING_MODEL,
        persist_directory=VECTORSTORE_PATH,
        collection_name=candidate_id
    )

    return vectorstore


def load_vectorstore(candidate_id: str) -> Chroma:
    """
    Load an existing vector store from disk.

    Used when you want to search a resume
    that was already processed and saved.

    Args:
        candidate_id : unique ID used when creating the store

    Returns:
        ChromaDB vectorstore object
    """
    return Chroma(
        persist_directory=VECTORSTORE_PATH,
        embedding_function=EMBEDDING_MODEL,
        collection_name=candidate_id
    )