
import asyncio
import json

from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ModelFamily
from autogen_core.tools import FunctionTool
from autogen_ext.models.ollama import OllamaChatCompletionClient

from database.knowledge_search import search_kb


MODEL_NAME = "qwen3:4b-instruct"
OLLAMA_HOST = "http://localhost:11434"


# Python tool used by the Knowledge Agent
def search_knowledge_base(query: str) -> str:

    results = search_kb(query, max_results=5)

    if not results:
        return json.dumps({
            "found": False,
            "message": "No matching company policy was found.",
            "sources": [],
            "passages": []
        }, indent=2)

    return json.dumps({
        "found": True,
        "sources": list({
            result["source"] for result in results
        }),
        "passages": results
    }, indent=2)


SYSTEM_MESSAGE = """
You are the ShopEase Knowledge Base Agent.

Your responsibility is to retrieve relevant company policies.

Instructions:

1. Always use the search_knowledge_base tool.
2. Search using the customer's complaint, category and summary.
3. Return only information found in company documents.
4. Include the source filename for every relevant passage.
5. Never invent policies, refund periods or delivery timelines.
6. If no matching information is found, clearly state that.
7. Do not generate a customer response.

Return valid JSON only.

Expected format:

{
    "found": true,
    "sources": ["shipping_policy.md"],
    "relevant_information": [
        "Standard delivery: 5 to 7 business days."
    ],
    "escalation_indicators": [
        "Delays exceeding 7 business days beyond the estimated date"
    ]
}

If no information is found, return:

{
    "found": false,
    "sources": [],
    "relevant_information": [],
    "escalation_indicators": [],
    "message": "No matching policy found."
}
"""


async def retrieve_knowledge(
    complaint,
    category,
    summary
):

    model_client = OllamaChatCompletionClient(
        model=MODEL_NAME,
        host=OLLAMA_HOST,
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": ModelFamily.UNKNOWN,
            "structured_output": True,
        },
        options={
            "temperature": 0
        }
    )

    search_tool = FunctionTool(
        search_knowledge_base,
        description=(
            "Search ShopEase company policy documents. "
            "Input a search query and return matching "
            "policy passages with source filenames."
        )
    )

    agent = AssistantAgent(
        name="knowledge_base_agent",
        model_client=model_client,
        tools=[search_tool],
        system_message=SYSTEM_MESSAGE,
        reflect_on_tool_use=True,
        max_tool_iterations=2
    )

    try:

        task = f"""
        Customer complaint:
        {complaint}

        Category:
        {category}

        Summary:
        {summary}

        Search the company documents and identify
        relevant policy information and escalation rules.
        """

        result = await agent.run(task=task)

        response = result.messages[-1].content

        if not isinstance(response, str):
            raise ValueError("Unexpected agent response format.")

        # Extract JSON
        start = response.find("{")
        end = response.rfind("}")

        if start == -1 or end == -1:
            raise ValueError(
                f"Knowledge Agent did not return JSON: {response}"
            )

        data = json.loads(response[start:end + 1])

        if not isinstance(data.get("found"), bool):
            raise ValueError("Invalid knowledge search status.")

        if not isinstance(data.get("sources"), list):
            raise ValueError("Invalid knowledge sources.")

        if not isinstance(data.get("relevant_information"), list):
            raise ValueError("Invalid policy information.")

        if not isinstance(data.get("escalation_indicators"), list):
            raise ValueError("Invalid escalation indicators.")

        return data

    finally:
        await model_client.close()


if __name__ == "__main__":

    complaint = (
        "My order is delayed by 10 days. "
        "I am very disappointed with your service."
    )

    category = "Shipping"

    summary = (
        "Customer reports a delayed delivery "
        "and expresses disappointment."
    )

    print("\nKNOWLEDGE BASE AGENT")
    print("=" * 55)

    try:

        result = asyncio.run(
            retrieve_knowledge(
                complaint,
                category,
                summary
            )
        )

        print("\nCustomer Complaint:")
        print(complaint)

        print("\nKnowledge Agent Results:")

        print(json.dumps(
            result,
            indent=4
        ))

        print("\nKNOWLEDGE AGENT TEST: SUCCESS")

    except Exception as error:

        print("\nKNOWLEDGE AGENT TEST: FAILED")
        print("Error:", error)
        raise
