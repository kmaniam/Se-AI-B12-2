
import asyncio
import json
import re

from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ModelFamily
from autogen_core.tools import FunctionTool
from autogen_ext.models.ollama import OllamaChatCompletionClient

from database.db_connection import initialize_database
from database.db_operations import (
    create_ticket,
    create_escalation,
    log_agent_execution
)


MODEL_NAME = "qwen3:4b-instruct"
OLLAMA_HOST = "http://localhost:11434"

CONFIDENCE_THRESHOLD = 0.70


# --------------------------------------------------
# 1. Deterministic escalation engine
# --------------------------------------------------

def evaluate_escalation(
    complaint,
    query_analysis,
    knowledge_result,
    resolution_result
):

    reasons = []

    urgency = query_analysis.get("urgency", "Medium")
    sentiment = query_analysis.get("sentiment", "Neutral")

    confidence = resolution_result.get("confidence", 0)

    complaint_lower = complaint.lower()

    # High urgency
    if urgency == "High":
        reasons.append("High urgency")

    # Angry customer
    if sentiment == "Angry":
        reasons.append("Angry customer")

    # No matching knowledge document
    if not knowledge_result.get("found", False):
        reasons.append("No matching knowledge document")

    # Unsupported corporate gift-card requests
    unsupported_terms = [
        "corporate gift card",
        "corporate gift cards",
        "bulk gift card",
        "bulk gift cards",
        "employee gift card",
        "employee gift cards",
    ]

    complaint_lower = complaint.lower()

    if any(term in complaint_lower for term in unsupported_terms):
        reasons.append(
            "Unsupported corporate gift-card request"
        )

    # Legal threats
    legal_keywords = [
        "lawyer",
        "attorney",
        "legal action",
        "sue",
        "court"
    ]

    if any(word in complaint_lower for word in legal_keywords):
        reasons.append("Legal threat")

    # Fraud indicators
    fraud_keywords = [
        "fraud",
        "fraudulent",
        "unauthorized transaction",
        "identity theft",
        "stolen card"
    ]

    if any(word in complaint_lower for word in fraud_keywords):
        reasons.append("Possible fraud")

    # Payment disputes
    payment_keywords = [
        "charged my card",
        "duplicate charge",
        "charged twice",
        "charged three times",
        "payment dispute",
        "incorrect charge"
    ]

    if any(word in complaint_lower for word in payment_keywords):
        reasons.append("Payment dispute")

    # Low resolution confidence
    if confidence < CONFIDENCE_THRESHOLD:
        reasons.append("Low resolution confidence")

    # Query agent's review flag
    if query_analysis.get("requires_human_review", False):
        reasons.append("Query Agent requested human review")

        # Determine whether the customer issue needs follow-up
    response_text = resolution_result.get(
        "response", ""
    ).lower()

    follow_up_phrases = [
        "please confirm",
        "please provide",
        "could you confirm",
        "additional information",
        "further information",
        "investigate this further",
        "waiting for your response",
    ]

    needs_follow_up = (
        resolution_result.get("confidence", 0) < 0.80
        or any(
            phrase in response_text
            for phrase in follow_up_phrases
        )
    )

    if reasons:
        status = "Escalated"
    elif needs_follow_up:
        status = "Pending"
    else:
        status = "Resolved"

    return {
        "status": status,
        "escalate": bool(reasons),
        "reasons": reasons,
        "needs_follow_up": needs_follow_up,
    }


# --------------------------------------------------
# 2. Database logging tool
# --------------------------------------------------

def log_ticket(
    customer_name: str,
    order_id: str,
    complaint: str,
    query_analysis_json: str,
    knowledge_result_json: str,
    resolution_result_json: str
) -> str:

    query_analysis = json.loads(query_analysis_json)

    knowledge_result = json.loads(knowledge_result_json)

    resolution_result = json.loads(resolution_result_json)

    decision = evaluate_escalation(
        complaint,
        query_analysis,
        knowledge_result,
        resolution_result
    )

    status = decision["status"]

    escalation_reason = "; ".join(decision["reasons"]) or None

    sources = knowledge_result.get("sources", [])

    ticket_id = create_ticket(
        customer_name=customer_name,
        order_id=order_id,
        complaint=complaint,
        category=query_analysis.get("category"),
        urgency=query_analysis.get("urgency"),
        sentiment=query_analysis.get("sentiment"),
        kb_sources=", ".join(sources),
        response=resolution_result.get("response"),
        confidence=resolution_result.get("confidence"),
        status=status,
        escalation_reason=escalation_reason
    )

    # Record execution history for all four agents
    agent_outputs = [
        (
            "customer_query_agent",
            complaint,
            json.dumps(query_analysis)
        ),
        (
            "knowledge_base_agent",
            json.dumps(query_analysis),
            json.dumps(knowledge_result)
        ),
        (
            "resolution_agent",
            json.dumps(knowledge_result),
            json.dumps(resolution_result)
        ),
        (
            "log_agent",
            json.dumps(resolution_result),
            json.dumps(decision)
        )
    ]

    for agent_name, input_data, output_data in agent_outputs:

        log_agent_execution(
            ticket_id=ticket_id,
            agent_name=agent_name,
            input_data=input_data,
            output_data=output_data,
            execution_status="Success"
        )

    # Create human escalation record
    if decision["escalate"]:

        create_escalation(
            ticket_id,
            escalation_reason
        )

    return json.dumps({
        "ticket_id": ticket_id,
        "status": status,
        "escalated": decision["escalate"],
        "escalation_reason": escalation_reason,
        "agent_logs_created": len(agent_outputs),
        "message": "Ticket successfully saved to SQLite."
    }, indent=2)


# --------------------------------------------------
# 3. AutoGen Log Agent
# --------------------------------------------------

async def run_log_agent(
    customer_name,
    order_id,
    complaint,
    query_analysis,
    knowledge_result,
    resolution_result
):

    initialize_database()

    model_client = OllamaChatCompletionClient(
        model=MODEL_NAME,
        host=OLLAMA_HOST,
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": ModelFamily.UNKNOWN,
            "structured_output": True
        },
        options={
            "temperature": 0
        }
    )

    logging_tool = FunctionTool(
        log_ticket,
        description=(
            "Save a customer support ticket to SQLite, "
            "evaluate escalation rules, record agent logs "
            "and create human escalation records. "
            "Pass all six required fields."
        )
    )

    agent = AssistantAgent(
        name="log_agent",
        model_client=model_client,
        tools=[logging_tool],
        system_message="""
        You are the ShopEase Log Agent.

        Your responsibility is to save the completed
        customer support ticket.

        Instructions:

        1. Call the log_ticket tool exactly once.
        2. Pass all supplied customer and agent information.
        3. Do not change the complaint or agent outputs.
        4. Do not independently invent escalation decisions.
        5. The Python logging tool evaluates escalation rules.
        6. Report the ticket ID and final status returned
           by the tool.
        7. Do not claim success if the tool fails.
        """,
        reflect_on_tool_use=True,
        max_tool_iterations=2
    )

    try:

        task = f"""
        Save the following completed customer support ticket.

        Customer name:
        {customer_name}

        Order ID:
        {order_id}

        Complaint:
        {complaint}

        Query Agent output:
        {json.dumps(query_analysis)}

        Knowledge Agent output:
        {json.dumps(knowledge_result)}

        Resolution Agent output:
        {json.dumps(resolution_result)}

        Call the log_ticket tool to save the ticket.
        """

        result = await agent.run(task=task)

        final_message = result.messages[-1].content

        print("\nLog Agent Result:")
        print(final_message)

        # Verify that the tool actually created the ticket
        # Verify that the database tool was executed
        # Verify that the database tool was executed
        tool_executed = any(
            "ToolCallExecutionEvent" in type(message).__name__
            for message in result.messages
        )

        if not tool_executed:
            print("\nDEBUG: AutoGen message types:")
            for message in result.messages:
                print(type(message).__name__)

            raise RuntimeError(
                "Could not verify the database tool execution."
            )

        print("\nDatabase tool execution verified successfully.")

        return final_message

    finally:

        await model_client.close()


# --------------------------------------------------
# 4. Standalone testing
# --------------------------------------------------

if __name__ == "__main__":

    complaint = (
        "My order is delayed by 10 days. "
        "I am very disappointed with your service."
    )

    query_analysis = {
        "category": "Shipping",
        "urgency": "Medium",
        "sentiment": "Negative",
        "summary": "Customer reports a delayed delivery.",
        "requires_human_review": False
    }

    knowledge_result = {
        "found": True,
        "sources": ["shipping_policy.md"],
        "relevant_information": [
            "Standard delivery: 5 to 7 business days.",
            "Support will investigate delayed shipments."
        ],
        "escalation_indicators": [
            "Delays exceeding 7 business days beyond the estimated date"
        ]
    }

    resolution_result = {
        "response": (
            "We apologize for the delay. "
            "Please confirm your estimated delivery date "
            "and order ID so we can investigate."
        ),
        "confidence": 0.75,
        "confidence_reason": (
            "Additional delivery information is required."
        )
    }

    print("\nSHOP EASE - LOG AGENT")
    print("=" * 55)

    try:

        asyncio.run(
            run_log_agent(
                customer_name="Priya",
                order_id="ORD-4512",
                complaint=complaint,
                query_analysis=query_analysis,
                knowledge_result=knowledge_result,
                resolution_result=resolution_result
            )
        )

        print("\nLOG AGENT TEST: SUCCESS")

    except Exception as error:

        print("\nLOG AGENT TEST: FAILED")
        print("Error:", error)
        raise
