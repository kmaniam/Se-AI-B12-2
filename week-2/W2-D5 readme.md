Markdown

# Week 2 - Day 5: Langchain Advanced

## 1. Model Integration

Model integration means connecting LangChain to an AI model so we can send it messages and get replies. The main model in this course is OpenAI's GPT, but LangChain can connect to many providers (such as Ollama, Claude, and Google Gemini).

### Step 1: Install and set your key
In the terminal, install the required library:
```
Python
pip install langchain-openai
```

Set your API key (PowerShell example):

```
PowerShell$env:OPENAI_API_KEY="your-key-here"
```
📌 Important Note: The key is how OpenAI knows it's you. Never share it or put it directly in your code.

Step 2: Create the model

We use ChatOpenAI and select a model. gpt-4o-mini is a fast, low-cost model ideal for development.

```
Python
from langchain_openai import ChatOpenAI

# Initialize the model
llm = ChatOpenAI(model="gpt-4o-mini")

# Invoke the model with a simple prompt
response = llm.invoke("Hello, introduce yourself briefly.")
print(response.content)
```

2. Messages

Chat models in LangChain process structured messages rather than raw strings. This standardizes conversation roles and context management across different AI providers.
	SystemMessage: Sets the persona, behavior, and rules for the AI.
	HumanMessage: Represents input from the user.
	AIMessage: Represents the model's response.

```	
Python

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

chat = ChatOpenAI(model="gpt-4o-mini")

# Structuring a conversational context
messages = [
    SystemMessage(content="You are a precise technical tutor specializing in Python."),
    HumanMessage(content="What is a list comprehension?"),
    AIMessage(content="A list comprehension is a concise way to create lists in Python."),
    HumanMessage(content="Give me a quick 1-line example.")
]

response = chat.invoke(messages)
print(response.content)
```

📌 Important Note: Always pass system instructions at the beginning of the message sequence to ensure the model adheres strictly to its persona throughout the conversation.

3. Guardrails - Basic

Guardrails ensure LLM outputs strictly follow required formats and stay within predefined constraints. Basic guardrails utilize Pydantic schemas along with Output Parsers to guarantee valid, structured JSON output.

```
Python
from langchain_core.output_parsers import JsonOutputParser

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# Define the expected schema
class UserInfo(BaseModel):
    name: str = Field(description="Name of the person")
    role: str = Field(description="Job role or title of the person")

parser = JsonOutputParser(pydantic_object=UserInfo)

prompt = PromptTemplate(
    template="Extract user details from the text.\n{format_instructions}\nText: {text}",
    input_variables=["text"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | ChatOpenAI(model="gpt-4o-mini") | parser

result = chain.invoke({"text": "Alice is currently working as a Senior Software Engineer."})
print(result)  # Output: {'name': 'Alice', 'role': 'Senior Software Engineer'}

```

📌 Important Note: Output parsers enforce structure, but you must validate non-empty inputs and handle potential parsing errors using try-except blocks in production.

4. Evaluation Basic

Evaluation measures the accuracy and quality of model outputs against expected references or defined criteria using LLM-as-a-judge patterns.

```
Python
from langchain.evaluation import load_evaluator
from langchain_openai import ChatOpenAI

evaluator = load_evaluator("qa", llm=ChatOpenAI(model="gpt-4o-mini"))

# Evaluate prediction against reference answer
eval_result = evaluator.evaluate_strings(
    prediction="LangChain is a framework designed to build LLM-powered applications.",
    reference="LangChain is a developer framework for building applications using language models.",
    input="What is LangChain?"
)

print(eval_result)
```

📌 Important Note: Automated evaluations are valuable for regression testing, but always review a statistical sample manually to ensure evaluator alignment with user needs.

5. How to Build a Basic Gen AI Application
Building a complete Gen AI application in LangChain involves chaining components together using LangChain Expression Language (LCEL). The fundamental flow follows: Prompt $\rightarrow$ Model $\rightarrow$ Output Parser.

```
Python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# 1. Define Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert concise technical summary assistant."),
    ("user", "Summarize the key concept of {topic} in two bullet points.")
])

# 2. Initialize Model
model = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

# 3. Define Parser
parser = StrOutputParser()

# 4. Assemble Chain via LCEL
app_chain = prompt | model | parser

# 5. Execute Chain
output = app_chain.invoke({"topic": "Model Context Protocol (MCP)"})
print(output)
```

📌 Important Note: Keeping temperature low (e.g., 0.0–0.2) ensures deterministic and reproducible results in production applications, 
whereas higher values (e.g., 0.7+) increase creativity.