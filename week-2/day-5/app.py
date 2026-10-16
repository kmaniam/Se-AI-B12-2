
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Step 1: Connect to the local AI model
llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)

# Step 2: Create a prompt with a history placeholder
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an experienced database trainer. "
               "Explain concepts in simple English with examples."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
])

# Step 3: Create the basic chain
chain = prompt | llm | StrOutputParser()

# Step 4: Create an in-memory conversation store
chat_history = {}

def get_session_history(session_id: str):
    if session_id not in chat_history:
        chat_history[session_id] = InMemoryChatMessageHistory()
    return chat_history[session_id]

# Step 5: Add conversation history support
chatbot = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history"
)

# Step 6: Start the chat
session_id = "my_first_chat"

while True:
    question = input("\nYou: ")

    if question.strip().lower() == "exit":
        print("Goodbye!")
        break

    if not question.strip():
        print("Please enter a question.")
        continue

    try:
        answer = chatbot.invoke(
            {"question": question},
            config={"configurable": {"session_id": session_id}}
        )
        print("\nAI:", answer)
    except Exception as e:
        print(f"An error occurred: {e}")
