Markdown
# Social Eagle AI - Week 2, Day 4: Advanced Retrieval & Agents -> RAG

Comprehensive high-level notes, practical code examples, and key takeaways covering Day 4 of the curriculum.

---

## **1. Multi-Query & Contextual Compression Retrievers**

### **High-Level Overview**
Standard vector search can fail if user queries lack specific keywords or if retrieved text chunks contain excessive noise. Advanced retrievers solve this by expanding or refining what gets sent to the LLM.

* **MultiQueryRetriever**: Automatically generates multiple perspectives of a user's query using an LLM, retrieves documents for each, and takes the unique union of results to improve recall.
* **Contextual Compression**: Passes raw retrieved documents through a compressor or LLM chain to extract *only* the relevant sentences, reducing token bloat and removing noisy context.

* **The main types of RAG
	Type					Main idea (in one line)
	Self RAG				The AI checks and corrects itself while answering.
	Corrective RAG (CRAG)	If retrieved data is bad, it searches again (e.g. the web).
	Fusion RAG				Asks the question in many ways and combines the results.
	BM25 + Rerank			Uses keyword search + re-orders results by relevance.

### **Code Example**
```
python
from langchain.retrievers import MultiQueryRetriever
from langchain_openai import ChatOpenAI

# Initialize LLM for query generation
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Wrap an existing retriever with MultiQueryRetriever
advanced_retriever = MultiQueryRetriever.from_llm(
    retriever=vector_store.as_retriever(),
    llm=llm
)

# Executes multiple query variants under the hood
unique_docs = advanced_retriever.invoke("How do vector databases handle similarity?")
```

📌 Important Points:

	Multi-query retrieval dramatically improves recall when users use ambiguous or brief search phrasing.

	Contextual compression saves token costs and prevents LLMs from getting distracted by irrelevant details inside large document chunks.

2. Conversational RAG & History-Aware Retrievers
High-Level Overview
In a multi-turn chat interface, users often ask follow-up questions (e.g., "How do I set that up?"). A standard retriever would fail because "that" lacks context.

History-Aware Retriever: Takes the conversation history and the latest user follow-up, then reformulates it into a standalone question before searching the vector store.

Code Example
```
Python
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Prompt to turn conversational follow-ups into standalone queries
contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", "Given a chat history and the latest user question, formulate a standalone question."),
    MessagesPlaceholder("chat_history"),
    ("user", "{input}")
])

history_aware_retriever = create_history_aware_retriever(
    model, vector_store.as_retriever(), contextualize_q_prompt
)
```
📌 Important Points:

	Essential for building chatbots that remember previous turns in a conversation.

	Prevents semantic search errors caused by pronoun references or missing nouns in follow-up queries.

3. LangChain Agents & Tools

High-Level Overview
While chains follow a rigid, pre-defined sequence of steps, Agents use an LLM as a reasoning engine to dynamically choose which tools to invoke, when to invoke them, and how to process the output based on user input.

	Tools: Functions or APIs wrapped with descriptions so the LLM knows their purpose (e.g., calculators, web search, custom database queries).

	Agent Executor: The runtime loop that takes user input, prompts the LLM to choose a tool, executes the tool, and loops until a final answer is reached.

Code Example
```
Python
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate

# 1. Define a custom tool using the @tool decorator
@tool
def calculate_storage_cost(num_documents: int) -> float:
    """Calculates vector database storage cost based on document count."""
    cost_per_doc = 0.0005
    return num_documents * cost_per_doc

tools = [calculate_storage_cost]

# 2. Setup prompt and agent
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant with access to tools."),
    MessagesPlaceholder("chat_history"),
    ("user", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

agent = create_openai_tools_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 3. Run the agent
response = agent_executor.invoke({"input": "How much will it cost to store 5000 documents?", "chat_history": []})
print(response["output"])
```

📌 Important Points:

	Clear docstrings on custom tools are vital because the LLM reads them to decide when a tool is appropriate.

	Agents introduce dynamic problem-solving capabilities beyond linear prompt chains.