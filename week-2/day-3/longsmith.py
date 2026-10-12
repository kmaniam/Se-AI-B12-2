import os

# Turn LangSmith tracking ON
os.environ["LANGSMITH_TRACING"] = ""
os.environ["LANGSMITH_API_KEY"] = ""   # <-- paste your key
os.environ["LANGSMITH_PROJECT"] = "my-first-app"          # runs are grouped under this name
os.environ["OPENAI_API_KEY"] = ""          # <-- paste your key
