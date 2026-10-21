import os

os.environ.pop("NEMOGUARDRAILS_LLM_FRAMEWORK", None)

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from nemoguardrails import RailsConfig
from nemoguardrails.integrations.langchain.runnable_rails import (
    RunnableRails,
)

llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0,
    disable_streaming=True,
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an Oracle DBA assistant. "
        "Answer database questions accurately."
    ),
    ("human", "{input}"),
])

chain = prompt | llm

config = RailsConfig.from_path("./config")
guarded_chain = RunnableRails(config, runnable=chain)

question = "What is Oracle Data Guard?"
result = guarded_chain.invoke({"input": question})

print("\nQuestion:", question)
print("\nGuarded answer:", result)