
from langchain_ollama import OllamaEmbeddings
import math

# Step 1: Connect to the local embedding model
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Step 2: Define two sentences
text1 = "Oracle indexes help improve SQL query performance."
text2 = "Indexes make Oracle database queries faster."

# Step 3: Generate embeddings
vector1 = embeddings.embed_query(text1)
vector2 = embeddings.embed_query(text2)

# Step 4: Calculate cosine similarity
dot_product = sum(a * b for a, b in zip(vector1, vector2))

magnitude1 = math.sqrt(sum(a * a for a in vector1))
magnitude2 = math.sqrt(sum(b * b for b in vector2))

similarity = dot_product / (magnitude1 * magnitude2)

# Step 5: Display results
print("Sentence 1:", text1)
print("Sentence 2:", text2)
print("Vector 1 length:", len(vector1))
print("Vector 2 length:", len(vector2))
print("Cosine similarity:", round(similarity, 4))
