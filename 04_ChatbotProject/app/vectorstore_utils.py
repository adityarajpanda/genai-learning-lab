# Functions to store data in vectorstore and retrieve data from vectorstore

# Vector database is created entirely in my computer's temporary RAM (memory).
# Because it is living in RAM, it is transient. The moment this Python script stops running, 
# this database is completely wiped out unless we explicitly save it to the local hard drive
# using a command like faiss_index.save_local("my_faiss_index").

from langchain_community.vectorstores.faiss import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

def create_faiss_index(text):
    embeddings =HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    return FAISS.from_texts(texts=text, embedding=embeddings)

def retrieve_similar_documents(faiss_index, query, k=4):
    return faiss_index.similarity_search(query, k=k)

