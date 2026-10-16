
from langchain_ollama import ChatOllama

# Step 1: Connect to the local AI model
llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)

# Step 2: Get input from the user
question = input("Enter your question: ")

# Step 3: Send the question to the AI model
response = llm.invoke(question)

# Step 4: Display the answer
print("\nAI Answer:")
print(response.content)
