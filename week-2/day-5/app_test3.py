
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Step 1: Connect to the local AI model
llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)

# Step 2: Create the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an experienced database trainer. "
               "Explain concepts in simple English with an example."),
    ("human", "{question}")
])

# Step 3: Create the LangChain pipeline
chain = prompt | llm | StrOutputParser()

# Step 4: Get a question from the user
question = input("Enter your question: ")

# Step 5: Execute the complete chain
answer = chain.invoke({"question": question})

# Step 6: Display the answer
print("\nAI Answer:")
print(answer)
