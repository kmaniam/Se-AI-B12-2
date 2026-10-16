
from langchain_ollama import OllamaEmbeddings
import math

# Step 1: Connect to the local embedding model
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Step 2: Define three sentences
text1 = "Oracle indexes help improve SQL query performance."
text2 = "Indexes make Oracle database queries faster."
text3 = "Oracle RMAN is used to back up and recover databases."

# Step 3: Generate embeddings
vector1 = embeddings.embed_query(text1)
vector2 = embeddings.embed_query(text2)
vector3 = embeddings.embed_query(text3)

# Step 4: Define cosine similarity
def cosine_similarity(vector_a, vector_b):
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
    magnitude_a = math.sqrt(sum(a * a for a in vector_a))
    magnitude_b = math.sqrt(sum(b * b for b in vector_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)

# Step 5: Compare the sentences
score_12 = cosine_similarity(vector1, vector2)
score_13 = cosine_similarity(vector1, vector3)

# Step 6: Display results
print("Sentence 1:", text1)
print("Sentence 2:", text2)
print("Sentence 3:", text3)

print("\nVector lengths:")
print(len(vector1), len(vector2), len(vector3))

print("\nSimilarity between Sentence 1 and Sentence 2:")
print(round(score_12, 4))

print("\nSimilarity between Sentence 1 and Sentence 3:")
print(round(score_13, 4))
