
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

# Step 1: Connect to the local AI model
llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)

# Step 2: Create a reusable prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an experienced database trainer. "
               "Explain concepts in simple English with an example."),
    ("human", "{question}")
])

# Step 3: Get the user's question
question = input("Enter your question: ")

# Step 4: Insert the question into the template
messages = prompt.format_messages(question=question)

# Step 5: Send the formatted messages to the model
response = llm.invoke(messages)

# Step 6: Display the answer
print("\nAI Answer:")
print(response.content)
