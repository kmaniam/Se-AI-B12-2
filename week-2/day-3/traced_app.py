
from langchain_openai import ChatOpenAI


def main():
    # LangSmith tracing is configured through environment variables.
    # No tracing-specific code is required here.
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    prompts = [
        (
            "Prompt 1 - Simple",
            "What is a database? Explain in two sentences."
        ),
        (
            "Prompt 2 - Technical",
            "Explain Oracle Data Guard physical standby, redo transport, "
            "redo apply, and switchover versus failover. Use a DBA example."
        ),
        (
            "Prompt 3 - Detailed analysis",
            "A production Oracle database is experiencing slow queries. "
            "Create a structured troubleshooting plan covering wait events, "
            "execution plans, CPU, memory, I/O, blocking sessions, and "
            "statistics. Explain the diagnostic purpose of each step and "
            "prioritize the actions."
        ),
    ]

    print("LangChain + OpenAI + LangSmith Tracing Demo")
    print("-" * 55)

    for title, prompt in prompts:
        print(f"\n{title}")
        print(f"Prompt: {prompt}")

        try:
            response = llm.invoke(prompt)
            print(f"Answer:\n{response.content}")

            # Usage metadata is displayed when the model/provider returns it.
            usage = response.usage_metadata
            if usage:
                print(f"Token usage: {usage}")

        except Exception as exc:
            print(f"Request failed: {exc}")

        print("-" * 55)


if __name__ == "__main__":
    main()
