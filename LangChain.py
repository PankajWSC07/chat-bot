import os

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

print("Loading data...")

documents = []
file_path = "data/data.txt"


if os.path.exists(file_path):
    loader = TextLoader(file_path, encoding="utf-8")
    documents.extend(loader.load())

if not documents or len(documents) == 0:
    print("No data file found")
    exit()

print(f"Loaded {len(documents)} documents")


splitter = RecursiveCharacterTextSplitter(separators='\n\n')

chunks = splitter.split_documents(documents)

if not chunks:
    print("no chunk found")
    exit()

print(f"Splitting into {len(chunks)} chunks...")

print("Creating embeddings...")

embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

print("Storing in ChromaDB...")

db = Chroma.from_documents(chunks, embedding, persist_directory="chroma_db")

db.persist()

print("Stored successfully!")

print("\nTesting retrieval...")

while True:
    query = input("\nEnter a query (or 'exit' to quit): ")
    if len(query.strip()) == 0:
        print("Enter the valide query")
        continue
        
    if query.lower() == "exit":
        print("Goodbye")
        break
    
    retriever = db.as_retriever(search_kwargs={"k": 2})

    results = retriever.invoke(query)

    print(f"\nQuery: {query}")
    print("\nTop Results:\n")

    for i, doc in enumerate(results):
        print(f"{i+1}. {doc.page_content}\n")
