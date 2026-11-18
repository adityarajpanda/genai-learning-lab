from collections.abc import Sequence

import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document

EMBEDDING_MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"


def initialize_faiss_index(embedding_model: Embeddings | None = None) -> FAISS:
    """Create an empty FAISS index using the configured sentence embedding model."""
    if embedding_model is None:
        embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    dimension = len(embedding_model.embed_query(""))
    if dimension == 0:
        raise ValueError("The embedding model returned an empty embedding.")

    index = faiss.IndexFlatL2(dimension)
    return FAISS(embedding_model, index, InMemoryDocstore(), {})


def add_document_chunks(
    faiss_index: FAISS,
    document_chunks: Sequence[str],
    chunk_embeddings: Sequence[Sequence[float]] | None = None,
) -> list[str]:
    """Add text chunks, optionally with precomputed embeddings, to a FAISS index."""
    if isinstance(document_chunks, str):
        raise TypeError("document_chunks must be a sequence of text chunks.")

    chunks = list(document_chunks)
    if not chunks:
        return []

    if chunk_embeddings is None:
        return faiss_index.add_texts(chunks)

    if len(chunks) != len(chunk_embeddings):
        raise ValueError("Each document chunk must have exactly one embedding.")

    text_embeddings = [
        (chunk, [float(value) for value in embedding])
        for chunk, embedding in zip(chunks, chunk_embeddings)
    ]
    return faiss_index.add_embeddings(text_embeddings)


def search_similar_chunks(
    faiss_index: FAISS,
    query_embedding: Sequence[float],
    k: int = 4,
) -> list[Document]:
    """Return up to k document chunks nearest to a query embedding."""
    if k < 0:
        raise ValueError("k must be non-negative.")
    if k == 0:
        return []

    return faiss_index.similarity_search_by_vector(
        [float(value) for value in query_embedding],
        k=k,
    )


def create_faiss_index(
    text: Sequence[str],
    embedding_model: Embeddings | None = None,
) -> FAISS:
    """Create and populate a FAISS index (kept for the chatbot's existing API)."""
    faiss_index = initialize_faiss_index(embedding_model)
    add_document_chunks(faiss_index, text)
    return faiss_index


def retrieve_similar_documents(
    faiss_index: FAISS,
    query: str | Sequence[float],
    k: int = 4,
) -> list[Document]:
    """Retrieve similar documents from either a query string or query embedding."""
    if k < 0:
        raise ValueError("k must be non-negative.")
    if k == 0:
        return []
    if isinstance(query, str):
        return faiss_index.similarity_search(query, k=k)
    return search_similar_chunks(faiss_index, query, k)
