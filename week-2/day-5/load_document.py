
from langchain_community.document_loaders import TextLoader

# Step 1: Load the text file
loader = TextLoader("oracle_notes.txt", encoding="utf-8")

# Step 2: Read the file into Document objects
documents = loader.load()

# Step 3: Display the results
print("Number of documents:", len(documents))

print("\nDocument content:")
print(documents[0].page_content)

print("\nDocument metadata:")
print(documents[0].metadata)
