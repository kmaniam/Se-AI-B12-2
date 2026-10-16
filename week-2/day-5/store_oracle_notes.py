
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# Step 1: Load the updated Oracle notes
# Step 1: Load both Oracle DBA documents
files_to_load = [
    "oracle_notes.txt",
    "oracle_test_notes.txt"
]

documents = []

for file_path in files_to_load:
    loader = TextLoader(file_path, encoding="utf-8")
    loaded_docs = loader.load()
    documents.extend(loaded_docs)
    print(f"Loaded: {file_path}")

print("Documents loaded:", len(documents))

# Step 2: Split the notes into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = text_splitter.split_documents(documents)

print("Chunks created:", len(chunks))

# Step 3: Initialize the embedding model
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Step 4: Open the existing Chroma collection
vector_store = Chroma(
    collection_name="oracle_notes",
    embedding_function=embeddings,
    persist_directory="./oracle_chroma_db"
)

# Step 5: Remove old records to prevent duplicates
existing_count = vector_store._collection.count()
print("Existing chunks:", existing_count)

if existing_count > 0:
    vector_store.delete_collection()
    print("Old collection deleted.")

# Step 6: Create a fresh collection with updated notes
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./oracle_chroma_db",
    collection_name="oracle_notes"
)

print("New chunks stored:", vector_store._collection.count())
print("Oracle knowledge base rebuilt successfully!")
