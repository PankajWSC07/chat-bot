import os
import re
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


def load_chunk(file_path):
    print("Loading data...")

    if not os.path.exists(file_path):
        print("No data file found")
        return []

    loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()

    print(f"Loaded {len(documents)} document(s)")

    chunks = []

    for doc in documents:
        paragraphs = doc.page_content.split("\n\n")

        for para in paragraphs:
            para = para.strip()

            if para:
                chunks.append(Document(page_content=para))

    print(f"Created {len(chunks)} paragraph chunks")

    return chunks


def create_vector_db(chunks):
    if not chunks:
        print("No chunks to store")
        return None

    print("\nCreating embeddings...")

    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Storing in ChromaDB...")

    db = Chroma.from_documents(
        documents=chunks, embedding=embedding, persist_directory="chroma_db"
    )

    db.persist()

    print("Stored successfully!")
    return db


def initialize_db():
    FILE_PATH = "data/data.txt"
    chunks = load_chunk(FILE_PATH)
    
    if not chunks:
        return None
    
    db = create_vector_db(chunks)
    return db


def get_retriever(db):
    if db is None:
        return None

    return db.as_retriever(search_kwargs={"k": 3})


def retrieve_context(query, retriever):
    if retriever is None:
        return []

    results = retriever.invoke(query)
    return results


if __name__ == "__main__":
    FILE_PATH = "data/data.txt"

    chunks = load_chunk(FILE_PATH)

    if not chunks:
        exit()

    db = create_vector_db(chunks)

    if db is None:
        exit()

    retriever = get_retriever(db)

    print("\n RAG Retrieval Ready!")

    while True:
        query = input("\nEnter a query (or 'exit' to quit): ").strip()

        if not query:
            print("Enter a valid query")
            continue

        if query.lower() == "exit":
            print("Goodbye")
            break

        results = retrieve_context(query, retriever)

        print(f"\nQuery: {query}")
        print(f"\nTop Results: {len(results)}\n")

        for i, doc in enumerate(results):
            print(f"{i+1}. {doc.page_content}\n")
