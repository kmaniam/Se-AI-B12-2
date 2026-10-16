
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# Step 1: Connect to the same embedding model
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Step 2: Load the existing local Chroma database
vector_store = Chroma(
    collection_name="oracle_notes",
    embedding_function=embeddings,
    persist_directory="./oracle_chroma_db"
)

# Step 3: Ask a question
question = input("Ask an Oracle DBA question: ")

# Step 4: Search for the 2 most relevant chunks
results = vector_store.similarity_search(
    question,
    k=2
)

# Step 5: Display the retrieved information
print("\nRelevant Oracle notes:")

for i, document in enumerate(results, start=1):
    print(f"\n--- Result {i} ---")
    print(document.page_content)
    print("Source:", document.metadata.get("source", "Unknown"))
