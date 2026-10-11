# Social Eagle AI - Week 2: Day -3 

LangChain Ecosystem & Core Components

This repository contains high-level notes, code examples, and key takeaways from Week 2 of the **Social Eagle AI** curriculum covering LangChain and RAG fundamentals.

---

## **1. LangChain Ecosystem**
* **Overview:** LangChain provides a modular software stack designed to compose LLM-driven applications. It bridges the gap between raw foundational models and application logic.
* **Core Libraries:** 
  * `langchain-core`: Base abstractions (prompts, models, runnables).
  * `langchain-community`: Third-party integrations (vector stores, document loaders).
  * **LCEL (LangChain Expression Language):** A declarative way to chain components together using the pipe (`|`) operator.

### **Example Code (LCEL Pipeline)**
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_template("Explain {concept} in one sentence.")
parser = StrOutputParser()

chain = prompt | model | parser
response = chain.invoke({"concept": "LangChain"})
print(response)
```
📌 Important Points:LCEL simplifies building and streaming pipelines natively via the pipe (|) operator.It standardizes interfaces across various third-party LLMs.

2. LangChain Components
  Overview:Modular building blocks that can be combined or used independently. Key components include Model I/O (Prompts, LLMs/Chat Models, Output Parsers), Retrieval (Loaders, Text Splitters, Vector Stores), and Agents.

Example Code (Configuring a Chat Model)
```python
Python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
message = llm.invoke("Hello, how are you?")
print(message.content)
```

📌 Important Points:Components are decoupled, making it easy to swap out an underlying LLM or database without rewriting application logic.

3. Data Ingestion
   Overview: The process of pulling unstructured or structured data from external sources (files, web pages, APIs) into the application using Document Loaders.

   Example Code (Manually Creating Documents)
```
   Python
   from langchain_core.documents import Document

doc = Document(
    page_content="Social Eagle AI teaches practical AI engineering skills.",
    metadata={"source": "classroom_notes"}
)
print(doc.page_content)

```

📌 Important Points:Ingested data is encapsulated into standard Document objects containing page_content and descriptive metadata.

4. Text Splitter
   Overview: Breaks large documents into smaller chunks so they fit within an LLM's context window while preserving semantic continuity using overlapping windows.

   Example Code (Recursive Splitting)
```
   Pythonf
   rom langchain_text_splitters import RecursiveCharacterTextSplitter

text = "LangChain makes building context-aware LLM apps simple. Text splitting ensures chunks fit into context limits."
splitter = RecursiveCharacterTextSplitter(chunk_size=40, chunk_overlap=10)

chunks = splitter.create_documents([text])
for chunk in chunks:
    print(chunk.page_content)

```

📌 Important Points:chunk_overlap ensures critical context isn't lost at boundaries where text is cut.RecursiveCharacterTextSplitter tries splitting by semantic markers (like paragraphs or sentences) first.

5. Embeddings
   Overview: Converts text chunks into high-dimensional numerical vectors, allowing machines to measure semantic similarity mathematically.

   Example Code (Generating Embeddings)
```
   Python
   from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector = embeddings.embed_query("Vector search is powerful.")

print(f"Dimension size: {len(vector)}")
```

📌 Important Points:Semantic meaning is preserved: sentences with similar meanings map close to each other in vector space.

6. Vector Store
   Overview: A specialized database optimized to store embeddings and execute fast approximate nearest neighbor (ANN) similarity searches.

   Example Code (FAISS Vector Store)
```
   Python
   from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

docs = [Document(page_content="FAISS handles fast similarity searches.")]
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = FAISS.from_documents(docs, embeddings)

results = vector_store.similarity_search("fast search", k=1)
print(results[0].page_content)
```

📌 Important Points:FAISS runs efficiently in-memory, making it ideal for local testing and lightweight prototypes.

7. Retriever & Chain
   Retriever: An interface that queries the vector store to fetch relevant documents based on user intent.
   Chain: Connects the retriever, prompt template, and LLM to form a complete RAG workflow.

   Example Code (Retriever Setup)
```
   Python
retriever = vector_store.as_retriever()
relevant_docs = retriever.invoke("What handles fast search?")
```
📌 Important Points:Retrievers extract top-$k$ context pieces to ground LLM generations and prevent hallucinations.
