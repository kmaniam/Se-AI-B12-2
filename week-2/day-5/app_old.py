
from langchain_ollama import ChatOllama

# Connect LangChain to our local AI model
llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)

# Send a question to the model
response = llm.invoke("Explain LangChain in simple words.")

# Display the AI's answer
print(response.content)
