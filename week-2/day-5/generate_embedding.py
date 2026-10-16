
from langchain_ollama import OllamaEmbeddings

# Step 1: Connect to the local embedding model
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# Step 2: Choose a sample text
text = "Oracle indexes help improve query performance."

# Step 3: Convert the text into a numerical vector
vector = embeddings.embed_query(text)

# Step 4: Display the results
print("Original text:")
print(text)

print("\nEmbedding vector length:")
print(len(vector))

print("\nFirst 10 numerical values:")
print(vector[:10])

# Step 5: Confirm the vector contains numbers
print("\nConfirm the vector contains numbers:")
print("Vector type:", type(vector))
print(
    "All values are numbers:",
    all(isinstance(value, (int, float)) for value in vector)
)