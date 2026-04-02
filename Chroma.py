import os
import re
import chromadb
from chromadb.utils import embedding_functions

client = chromadb.PersistentClient(path="./chroma_db")

embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = client.get_or_create_collection(
    name="knowledge_base", embedding_function=embedding_function
)


def chunk_text(text):
    paragraphs = re.split(r"\n\s*\n", text.strip())

    chunks = []
    for para in paragraphs:
        para = para.strip()

        if len(para) > 20:
            chunks.append(para)

    return chunks


def initialize_database():
    global collection

    file_path = "data/data.txt"

    if not os.path.exists(file_path):
        print(f" File not found: {file_path}")
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    print(" File loaded successfully")
    print(" Text length:", len(text))

    chunks = chunk_text(text)

    print("\n Total chunks:", len(chunks))

    if len(chunks) == 0:
        print(" No data to insert")
        return False

    if collection.count() > 0:
        print(" Clearing old data...")
        client.delete_collection("knowledge_base")
        collection = client.get_or_create_collection(
            name="knowledge_base", embedding_function=embedding_function
        )

    ids = [f"id_{i}" for i in range(len(chunks))]

    collection.add(documents=chunks, ids=ids)

    print("\n Data stored successfully")
    return True


def query_collection(query_text, n_results=3):
    """Query the vector database"""
    results = collection.query(query_texts=[query_text], n_results=n_results)

    docs = results.get("documents", [[]])[0]
    return docs

# run in terminal
if __name__ == "__main__":
    initialize_database()

    print("\n Ask something (type 'exit' to quit)\n")

    while True:
        query = input(" Query: ")
        if not query.strip():
            print(" Please enter a valid query")
            continue

        if query.lower() == "exit":
            print(" Goodbye!")
            break

        docs = query_collection(query)

        print("\n Result:\n")

        if not docs:
            print(" No relevant result found\n")
            continue

        print(">>>", docs[0])
        print("\n" + "-" * 50)

        if not docs:
            print(" No relevant result found\n")
            continue

    print(">>>", docs[0])
    print("\n" + "-" * 50)
