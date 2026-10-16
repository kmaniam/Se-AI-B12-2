
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

# Step 3: Create the LangChain chain
chain = prompt | llm | StrOutputParser()

# Step 4: Keep accepting questions
while True:
    question = input("\nEnter your question (or type 'exit'): ")

    # Stop when the user types exit
    if question.strip().lower() == "exit":
        print("Thank you for using the GenAI app!")
        break

    # Ignore empty questions
    if not question.strip():
        print("Please enter a question.")
        continue

    # Step 5: Run the chain
    try:
        answer = chain.invoke({"question": question})
        print("\nAI Answer:")
        print(answer)
    except Exception as e:
        print(f"An error occurred: {e}")
