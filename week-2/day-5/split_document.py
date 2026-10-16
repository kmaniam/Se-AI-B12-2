
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Step 1: Load the original document
loader = TextLoader("oracle_notes.txt", encoding="utf-8")
documents = loader.load()

# Step 2: Configure the text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=30
)

# Step 3: Split the document
chunks = text_splitter.split_documents(documents)

# Step 4: Display the results
print("Original document count:", len(documents))
print("Number of chunks:", len(chunks))

for i, chunk in enumerate(chunks, start=1):
    print(f"\n--- Chunk {i} ---")
    print(chunk.page_content)
    print("Metadata:", chunk.metadata)
