from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def create_vectorstore(documents, persist_directory):
    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=persist_directory
    )

    vectordb.persist()

    return vectordb

def load_vectorstore(persist_directory):
    return Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_model
    )