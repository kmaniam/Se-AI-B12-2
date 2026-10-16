from langchain_openai import ChatOpenAI

# Initialize the model
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

prompt = """
Suggest exactly 5 healthy breakfast ideas.

Healthy means:
- Include a source of protein.
- Include fiber-rich whole grains, fruits, or vegetables.
- Prefer minimally processed ingredients.
- Limit added sugar.
- Provide balanced, practical breakfast options.

Format:
- Number the ideas from 1 to 5.
- Write one idea per line.
- No preamble or conclusion.
"""

# Step 1: Print the complete message object
response = llm.invoke(prompt)
print(response.content)