
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate

# Step 1: Connect to the local embedding model
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Step 2: Load the existing Chroma database
vector_store = Chroma(
    collection_name="oracle_notes",
    embedding_function=embeddings,
    persist_directory="./oracle_chroma_db"
)

# Step 3: Connect to the local chat model
llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)

# Step 4: Define the prompt
prompt = ChatPromptTemplate.from_template("""
You are an Oracle DBA assistant.

Answer the question using only the context below.
If the context does not contain the answer, say:
"The provided Oracle notes do not contain enough information
to answer this question."

Context:
{context}

Question:
{question}
""")

# Step 5: Ask a question
question = input("Ask an Oracle DBA question: ")

# Step 6: Retrieve relevant notes
documents = vector_store.similarity_search(question, k=2)

context = "\n\n".join(
    document.page_content for document in documents
)

# Step 7: Generate an answer using the retrieved notes
messages = prompt.format_messages(
    context=context,
    question=question
)

response = llm.invoke(messages)

# Step 8: Display the answer
print("\nOracle DBA Assistant:")
print(response.content)
