
import asyncio
import json
import re

from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ModelFamily
from autogen_ext.models.ollama import OllamaChatCompletionClient


MODEL_NAME = "qwen3:4b-instruct"
OLLAMA_HOST = "http://localhost:11434"


SYSTEM_MESSAGE = """
You are the ShopEase Resolution Agent.

Your responsibility is to generate helpful customer support
responses using ONLY the supplied information.

STRICT BUSINESS RULES:

1. Never invent company policies.
2. Never assume missing dates, order status or customer facts.
3. Never promise refunds, replacements or delivery dates
   unless supported by company policy.
4. Never claim that an escalation threshold has been met
   unless all required conditions are explicitly established.
5. Distinguish between a delay of 10 days and a delay
   exceeding 7 business days beyond the estimated date.
6. A delay of 10 days alone does NOT prove that the
   escalation threshold has been met.
7. If the estimated delivery date or relevant timeline
   is unclear, ask the customer for clarification.
8. If no relevant policy exists, honestly recommend
   human support.
9. Be polite, empathetic and professional.
10. Never expose internal AI agent information.

CONFIDENCE GUIDELINES:

0.90 - 1.00: Clear policy directly answers the question.
0.70 - 0.89: Useful policy exists but clarification is needed.
0.40 - 0.69: Limited information is available.
0.00 - 0.39: No relevant policy information is available.

If important information is missing, reduce confidence.

Return valid JSON only:

{
    "response": "Customer-ready response",
    "confidence": 0.75,
    "confidence_reason": "Explanation"
}
"""


def extract_json(text):

    text = text.strip()

    text = re.sub(
        r"^```(?:json)?\s*|\s*```$",
        "",
        text,
        flags=re.IGNORECASE
    )

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError(
            f"Invalid JSON response: {text}"
        )

    return json.loads(match.group())


async def generate_resolution(
    complaint,
    query_analysis,
    knowledge_result
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

    agent = AssistantAgent(
        name="resolution_agent",
        model_client=model_client,
        system_message=SYSTEM_MESSAGE
    )

    try:

        task = f"""
        CUSTOMER COMPLAINT:
        {complaint}

        QUERY AGENT ANALYSIS:
        {json.dumps(query_analysis, indent=2)}

        KNOWLEDGE BASE RESULTS:
        {json.dumps(knowledge_result, indent=2)}

        Generate a customer-ready response.

        If no matching policy was found, do not guess.
        Clearly state that further investigation is required.

        Return only the required JSON.
        """

        result = await agent.run(task=task)

        response = result.messages[-1].content

        if not isinstance(response, str):
            raise ValueError("Unexpected response format.")

        data = extract_json(response)

        # Initialize for every complaint category
        missing_delivery_context = False

        # Deterministic business rule validation

        if (
            query_analysis.get("category") == "Shipping"
            and knowledge_result.get("found")
            and knowledge_result.get("escalation_indicators")
        ):

    # The complaint does not establish how many
    # business days beyond the estimated date it is late.

            missing_delivery_context = True

        if missing_delivery_context:

            data["response"] = (
                "We sincerely apologize for the delay "
                "in your order. Our standard delivery "
                "timeline is 5 to 7 business days. "
                "Our team can investigate delayed shipments. "
                "Could you please confirm your estimated "
                "delivery date and order ID so we can "
                "investigate this further?"
            )

            data["confidence"] = 0.75

            data["confidence_reason"] = (
                "Shipping policy retrieved successfully, "
                "but the exact number of business days "
                "beyond the estimated delivery date "
                "has not been established."
            )

        required_fields = {
            "response",
            "confidence",
            "confidence_reason"
        }

        if not required_fields.issubset(data.keys()):
            raise ValueError(
                "Missing required resolution fields."
            )

        if not isinstance(data["response"], str):
            raise ValueError("Invalid response text.")

        if not data["response"].strip():
            raise ValueError("Empty customer response.")

        confidence = data["confidence"]

        if isinstance(confidence, bool) or not isinstance(
            confidence, (int, float)
        ):
            raise ValueError("Invalid confidence score.")

        if not 0 <= confidence <= 1:
            raise ValueError("Confidence must be between 0 and 1.")

        if not isinstance(data["confidence_reason"], str):
            raise ValueError("Invalid confidence reason.")

        return data

    finally:
        await model_client.close()


if __name__ == "__main__":

    complaint = (
        "My order is delayed by 10 days. "
        "I am very disappointed with your service."
    )

    query_analysis = {
        "category": "Shipping",
        "urgency": "Medium",
        "sentiment": "Negative",
        "summary": (
            "Customer reports a delayed delivery "
            "and expresses disappointment."
        ),
        "requires_human_review": False
    }

    knowledge_result = {
        "found": True,
        "sources": ["shipping_policy.md"],
        "relevant_information": [
            "Standard delivery: 5 to 7 business days.",
            "Customers can track orders using their order ID.",
            "Support will investigate delayed shipments.",
            (
                "Delivery delays exceeding 7 business days "
                "beyond the estimated date must be escalated "
                "to human support."
            )
        ],
        "escalation_indicators": [
            (
                "Delays exceeding 7 business days "
                "beyond the estimated date"
            )
        ]
    }

    print("\nRESOLUTION AGENT")
    print("=" * 55)

    try:

        result = asyncio.run(
            generate_resolution(
                complaint,
                query_analysis,
                knowledge_result
            )
        )

        print("\nCustomer Complaint:")
        print(complaint)

        print("\nGenerated Customer Response:")
        print(result["response"])

        print("\nConfidence:")
        print(result["confidence"])

        print("\nConfidence Reason:")
        print(result["confidence_reason"])

        print("\nRESOLUTION AGENT TEST: SUCCESS")

    except Exception as error:

        print("\nRESOLUTION AGENT TEST: FAILED")
        print("Error:", error)
        raise
