import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from app.services.vector_service import (
    create_vectorstore,
    load_vectorstore
)

from app.services.llm_service import llm


SUPPORTED_EXTENSIONS = [
    ".py",
    ".ts",
    ".js",
    ".html",
    ".css",
    ".java",
    ".json",
    ".md"
]


def load_project_files(project_path):

    documents = []

    for root, dirs, files in os.walk(project_path):

        for file in files:

            if any(file.endswith(ext) for ext in SUPPORTED_EXTENSIONS):

                file_path = os.path.join(root, file)

                try:
                    with open(file_path, "r", encoding="utf-8") as f:

                        content = f.read()

                        documents.append(
                            Document(
                                page_content=content,
                                metadata={
                                    "source": file_path
                                }
                            )
                        )

                except:
                    pass

    return documents


def ingest_repository(project_path, repo_name):

    docs = load_project_files(project_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    split_docs = splitter.split_documents(docs)

    vector_path = f"app/uploads/{repo_name}"

    create_vectorstore(split_docs, vector_path)

    return True


def ask_codebase(repo_name, question):

    vectordb = load_vectorstore(
        f"app/uploads/{repo_name}"
    )

    retriever = vectordb.as_retriever(search_type="mmr",search_kwargs={"k": 5})

    docs = retriever.get_relevant_documents(question)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
    You are an expert software architect.

    Answer user question based upon repository context.

    Context:
    {context}

    Question:
    {question}
    """

    response = llm.invoke(prompt)

    return response.content