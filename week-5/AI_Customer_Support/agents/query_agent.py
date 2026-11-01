
import asyncio
import json
import re

from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ModelFamily
from autogen_ext.models.ollama import OllamaChatCompletionClient


MODEL_NAME = "qwen3:4b-instruct"
OLLAMA_HOST = "http://localhost:11434"


SYSTEM_MESSAGE = """
You are the Customer Query Agent for ShopEase online store.

Your only responsibility is to analyze customer complaints.

Extract these five fields:

1. category
2. urgency
3. sentiment
4. summary
5. requires_human_review

Allowed categories:
Shipping, Refund, Account, Product, Billing, Other

Allowed urgency:
Low, Medium, High

Allowed sentiment:
Positive, Neutral, Negative, Angry

Rules:

- High urgency for serious financial disputes, fraud,
  legal threats, serious account compromise, or severe complaints.
- Medium urgency for significant delivery delays,
  damaged products and unresolved service issues.
- Low urgency for general questions and routine requests.
- Identify Angry only when the customer expresses strong
  anger, threats or extreme frustration.
- Do not invent customer information.
- Do not generate a customer response.
- Return valid JSON only.
- Do not include Markdown code fences.

Expected JSON format:

{
  "category": "Shipping",
  "urgency": "Medium",
  "sentiment": "Negative",
  "summary": "Customer reports a delayed delivery.",
  "requires_human_review": false
}
"""


def extract_json(text):

    text = text.strip()

    # Remove Markdown code fences if present
    text = re.sub(
        r"^```(?:json)?\s*|\s*```$",
        "",
        text,
        flags=re.IGNORECASE
    )

    # Extract the JSON object
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError(
            f"Agent did not return valid JSON: {text}"
        )

    return json.loads(match.group())


async def analyze_complaint(complaint):

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

    agent = AssistantAgent(
        name="customer_query_agent",
        model_client=model_client,
        system_message=SYSTEM_MESSAGE
    )

    try:

        task = f"""
        Analyze this customer complaint:

        {complaint}

        Return only the required JSON object.
        """

        result = await agent.run(task=task)

        response = result.messages[-1].content

        if not isinstance(response, str):
            raise ValueError(
                "Unexpected response format from Query Agent."
            )

        data = extract_json(response)

        required_fields = {
            "category",
            "urgency",
            "sentiment",
            "summary",
            "requires_human_review"
        }

        if not required_fields.issubset(data.keys()):
            raise ValueError(
                "Query Agent response is missing required fields."
            )

        allowed_categories = {
            "Shipping", "Refund", "Account",
            "Product", "Billing", "Other"
        }

        allowed_urgencies = {"Low", "Medium", "High"}

        allowed_sentiments = {
            "Positive", "Neutral", "Negative", "Angry"
        }

        if data["category"] not in allowed_categories:
            raise ValueError("Invalid complaint category.")

        if data["urgency"] not in allowed_urgencies:
            raise ValueError("Invalid urgency value.")

        if data["sentiment"] not in allowed_sentiments:
            raise ValueError("Invalid sentiment value.")

        if not isinstance(data["requires_human_review"], bool):
            raise ValueError("Invalid human review flag.")

        return data

    finally:
        await model_client.close()


if __name__ == "__main__":

    complaint = (
        "My order is delayed by 10 days. "
        "I am very disappointed with your service."
    )

    print("\nCUSTOMER QUERY AGENT")
    print("=" * 50)

    try:

        result = asyncio.run(
            analyze_complaint(complaint)
        )

        print("\nCustomer Complaint:")
        print(complaint)

        print("\nAgent Analysis:")

        print(
            json.dumps(
                result,
                indent=4
            )
        )

        print("\nQUERY AGENT TEST: SUCCESS")

    except Exception as error:

        print("\nQUERY AGENT TEST: FAILED")
        print("Error:", error)
        raise
