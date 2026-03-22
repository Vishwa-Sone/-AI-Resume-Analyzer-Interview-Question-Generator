

import uuid
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter



print("Loading embedding model...")
EMBEDDING_MODEL = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)
print("Embedding model loaded")


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
   
    chunks = _split_text(resume_text)
    collection_name = f"temp_{uuid.uuid4().hex}"
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=EMBEDDING_MODEL,
        collection_name=collection_name
    )

    return vectorstore


def create_vectorstore(resume_text: str,
                       candidate_id: str) -> Chroma:

    chunks = _split_text(resume_text)

    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=EMBEDDING_MODEL,
        persist_directory=VECTORSTORE_PATH,
        collection_name=candidate_id
    )
    
    return vectorstore

def load_vectorstore(candidate_id: str) -> Chroma:
    return Chroma(
        persist_directory=VECTORSTORE_PATH,
        embedding_function=EMBEDDING_MODEL,
        collection_name=candidate_id
    )