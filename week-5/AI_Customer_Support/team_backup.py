
import asyncio
import json

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import (
    MaxMessageTermination,
    TextMentionTermination,
)
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core.models import ModelFamily
from autogen_core.tools import FunctionTool
from autogen_ext.models.ollama import OllamaChatCompletionClient

from agents.query_agent import analyze_complaint
from agents.knowledge_agent import retrieve_knowledge
from agents.resolution_agent import generate_resolution
from agents.log_agent import log_ticket
from database.db_connection import initialize_database


MODEL_NAME = "qwen3:4b-instruct"
OLLAMA_HOST = "http://localhost:11434"


def create_model_client():
    return OllamaChatCompletionClient(
        model=MODEL_NAME,
        host=OLLAMA_HOST,
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": ModelFamily.UNKNOWN,
            "structured_output": True,
        },
        options={"temperature": 0},
    )


async def run_support_workflow(
    customer_name,
    order_id,
    complaint,
):
    print("\nSHOP EASE - AI CUSTOMER SUPPORT")
    print("=" * 60)

    initialize_database()

    # Shared information passed between the four agents.
    state = {
        "customer_name": customer_name,
        "order_id": order_id,
        "complaint": complaint,
    }

    # -----------------------------------------------
    # Agent 1: Query Agent tool
    # -----------------------------------------------

    async def query_stage(customer_complaint: str) -> str:
        result = await analyze_complaint(customer_complaint)
        state["query_analysis"] = result

        print("\n[1] QUERY AGENT COMPLETED")
        print(json.dumps(result, indent=2))

        return json.dumps(result, indent=2)

    # -----------------------------------------------
    # Agent 2: Knowledge Agent tool
    # -----------------------------------------------

    async def knowledge_stage(search_request: str) -> str:
        query = state["query_analysis"]

        result = await retrieve_knowledge(
            complaint=state["complaint"],
            category=query["category"],
            summary=query["summary"],
        )

        state["knowledge_result"] = result

        print("\n[2] KNOWLEDGE AGENT COMPLETED")
        print(json.dumps(result, indent=2))

        return json.dumps(result, indent=2)

    # -----------------------------------------------
    # Agent 3: Resolution Agent tool
    # -----------------------------------------------

    async def resolution_stage(instruction: str) -> str:
        result = await generate_resolution(
            complaint=state["complaint"],
            query_analysis=state["query_analysis"],
            knowledge_result=state["knowledge_result"],
        )

        state["resolution_result"] = result

        print("\n[3] RESOLUTION AGENT COMPLETED")
        print(json.dumps(result, indent=2))

        return json.dumps(result, indent=2)

    # -----------------------------------------------
    # Agent 4: Log Agent tool
    # -----------------------------------------------

    async def logging_stage(save_ticket: bool) -> str:
        
        # Prevent duplicate ticket creation
        if state.get("log_result"):
            return json.dumps({
                "success": True,
                "message": "Ticket was already saved.",
                "ticket_id": state["log_result"]["ticket_id"],
                "duplicate_prevented": True
            })
        
        if not save_ticket:
            return json.dumps({
                "success": False,
                "message": "Ticket saving was not authorized.",
            })

        result = log_ticket(
            customer_name=state["customer_name"],
            order_id=state["order_id"],
            complaint=state["complaint"],
            query_analysis_json=json.dumps(
                state["query_analysis"]
            ),
            knowledge_result_json=json.dumps(
                state["knowledge_result"]
            ),
            resolution_result_json=json.dumps(
                state["resolution_result"]
            ),
        )

        state["log_result"] = json.loads(result)

        print("\n[4] LOG AGENT COMPLETED")
        print(json.dumps(state["log_result"], indent=2))

        return result

    # -----------------------------------------------
    # Create AutoGen tools
    # -----------------------------------------------

    query_tool = FunctionTool(
        query_stage,
        description=(
            "Analyze the customer's complaint. "
            "Call this tool with the complete complaint."
        ),
    )

    knowledge_tool = FunctionTool(
        knowledge_stage,
        description=(
            "Retrieve relevant company policies. "
            "Call this tool after Query Agent completes."
        ),
    )

    resolution_tool = FunctionTool(
        resolution_stage,
        description=(
            "Generate a customer response using "
            "the Query and Knowledge Agent results."
        ),
    )

    logging_tool = FunctionTool(
        logging_stage,
        description=(
            "Save the completed ticket to SQLite. "
            "Call with save_ticket=true after resolution."
        ),
    )

    # -----------------------------------------------
    # Create four AutoGen team members
    # -----------------------------------------------

    clients = [
        create_model_client()
        for _ in range(4)
    ]

    query_agent = AssistantAgent(
        name="query_agent",
        model_client=clients[0],
        tools=[query_tool],
        system_message="""
You are the ShopEase Query Agent.

Your task is to analyze the customer's complaint.

Call the query_stage tool exactly once.
Do not skip the tool.
After receiving its result, summarize the classification.
Do not generate a customer response.
""",
        reflect_on_tool_use=True,
        max_tool_iterations=2,
    )

    knowledge_agent = AssistantAgent(
        name="knowledge_agent",
        model_client=clients[1],
        tools=[knowledge_tool],
        system_message="""
You are the ShopEase Knowledge Agent.

Wait until the Query Agent has completed its work.

Call the knowledge_stage tool exactly once.
Summarize the retrieved company policies and sources.
Never invent policies.
Do not generate a customer response.
""",
        reflect_on_tool_use=True,
        max_tool_iterations=2,
    )

    resolution_agent = AssistantAgent(
        name="resolution_agent",
        model_client=clients[2],
        tools=[resolution_tool],
        system_message="""
You are the ShopEase Resolution Agent.

Wait until the Query and Knowledge Agents have completed.

Call the resolution_stage tool exactly once.
Generate a customer-ready response based only on the
retrieved company policy and supplied information.
Do not invent policies or promise unsupported outcomes.
""",
        reflect_on_tool_use=True,
        max_tool_iterations=2,
    )

    log_agent = AssistantAgent(
        name="log_agent",
        model_client=clients[3],
        tools=[logging_tool],
        system_message="""
You are the ShopEase Log Agent.

Wait until the first three agents have completed.

Call the logging_stage tool exactly once with
save_ticket=true.

Report the ticket ID and final status returned by the tool.

After successful logging, include this exact marker:
WORKFLOW_COMPLETE
""",
        reflect_on_tool_use=True,
        max_tool_iterations=2,
    )

    # -----------------------------------------------
    # Configure Round Robin Group Chat
    # -----------------------------------------------

    termination = (
        TextMentionTermination("WORKFLOW_COMPLETE")
        | MaxMessageTermination(12)
    )

    team = RoundRobinGroupChat(
        participants=[
            query_agent,
            knowledge_agent,
            resolution_agent,
            log_agent,
        ],
        termination_condition=termination,
    )

    try:
        task = f"""
Process this ShopEase customer support complaint.

Customer name: {customer_name}
Order ID: {order_id}

Customer complaint:
{complaint}

Execute the four agents in this order:
1. Query Agent
2. Knowledge Agent
3. Resolution Agent
4. Log Agent

Each agent must execute its assigned tool.
Do not skip any stage.
"""

        print("\nStarting AutoGen RoundRobinGroupChat...")
        print("Agent sequence: Query -> Knowledge -> Resolution -> Log")

        result = await team.run(task=task)

        print("\n" + "=" * 60)
        print("WORKFLOW EXECUTION FINISHED")
        print("=" * 60)

        if "log_result" in state:
            print("\nFINAL TICKET DETAILS")
            print(json.dumps(state["log_result"], indent=2))

            print("\nCUSTOMER RESPONSE")
            print(state["resolution_result"]["response"])
        else:
            print(
                "\nWARNING: The Log Agent did not complete "
                "the SQLite operation."
            )

        return state

    finally:
        await team.reset()

        for client in clients:
            await client.close()


if __name__ == "__main__":
    asyncio.run(
        run_support_workflow(
            customer_name="Priya",
            order_id="ORD-4512",
            complaint=(
                "My order is delayed by 10 days. "
                "I am very disappointed with your service."
            ),
        )
    )
