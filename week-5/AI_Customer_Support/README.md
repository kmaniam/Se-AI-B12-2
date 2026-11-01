# ShopEase AI Customer Support Automation

An AI-powered customer support automation system built using **Microsoft AutoGen, Ollama, Python, Streamlit and SQLite**.

The application analyzes customer complaints, searches company knowledge-base documents, generates policy-based responses, identifies escalation requirements and records support tickets.

## 1. Project Overview

ShopEase AI Customer Support automates the initial handling of customer complaints through four specialized AI agents.

The system helps to:
- Understand and classify customer complaints.
- Identify urgency and customer sentiment.
- Retrieve relevant company policies.
- Generate accurate, policy-based customer responses.
- Escalate sensitive or unsupported cases to human support.
- Maintain ticket history and agent execution logs.
- Track and review escalated tickets.

## 2. Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python 3.13 |
| AI Agent Framework | Microsoft AutoGen |
| Local LLM Runtime | Ollama |
| Language Model | qwen3:4b-instruct |
| User Interface | Streamlit |
| Database | SQLite |
| Data Processing | Pandas |
| Knowledge Base | Markdown documents |
| Workflow | AutoGen RoundRobinGroupChat |

## 3. System Architecture

The application uses four agents in the following sequence:

**Customer Complaint → Query Agent → Knowledge Agent → Resolution Agent → Log Agent → SQLite Database**

### Agent 1: Query Agent
- Understands the customer complaint.
- Identifies the complaint category.
- Determines urgency.
- Analyzes customer sentiment.
- Generates a complaint summary.
- Identifies whether human review is required.

### Agent 2: Knowledge Agent
- Searches the company knowledge base.
- Retrieves relevant policy information.
- Identifies matching source documents.
- Returns relevant information and escalation indicators.
- Avoids making unsupported policy assumptions.

### Agent 3: Resolution Agent
- Uses the complaint analysis and retrieved policy information.
- Generates a customer-friendly response.
- Assigns a confidence score.
- Applies deterministic business-rule validation where required.

### Agent 4: Log Agent
- Evaluates escalation conditions.
- Determines ticket status.
- Saves ticket information in SQLite.
- Records agent execution details.
- Creates escalation records for human support.

## 4. Knowledge Base

The application currently uses four Markdown documents:

| Document | Purpose |
|---|---|
| shipping_policy.md | Delivery timelines and shipping delays |
| refund_policy.md | Refund eligibility and processing |
| account_and_login.md | Password reset and account support |
| product_faq.md | Product information and damaged products |

The Knowledge Agent retrieves relevant information from these documents before the Resolution Agent generates a response.

## 5. Escalation Rules

The system escalates complaints when conditions such as the following are detected:

- High urgency.
- Angry customer sentiment.
- No matching knowledge-base document.
- Legal threats.
- Fraud or suspicious payment activity.
- Duplicate or disputed payments.
- Low response confidence.
- Query Agent requests human review.
- Unsupported corporate gift-card requests.

Tickets requiring additional customer information can be marked **Pending** for follow-up rather than incorrectly marked Resolved.

## 6. Database Design

The application uses SQLite for persistent storage.

Main database tables:

| Table | Purpose |
|---|---|
| customers | Customer information |
| tickets | Customer complaints and resolution details |
| agent_execution_logs | Individual agent execution records |
| knowledge_sources | Knowledge-base source information |
| escalations | Human support escalation tracking |

The application also provides ticket history, status filtering, search and report download functionality.

## 7. Application Features

- Streamlit customer complaint submission form.
- Four-agent AI workflow.
- Local Ollama model integration.
- Knowledge-base document retrieval.
- AI-generated customer responses.
- Confidence scoring.
- Automated escalation detection.
- Pending, Resolved and Escalated ticket statuses.
- SQLite ticket history.
- Agent execution logging.
- Escalation review and status updates.
- Ticket report download.

## 8. Installation and Execution

### Prerequisites

- Python 3.12 or later.
- Git.
- Ollama.
- Required Ollama model.

### Step 1: Download the Ollama model

```bash
ollama pull qwen3:4b-instruct
```

Ensure Ollama is running locally.

### Step 2: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd AI_Customer_Support
```

### Step 3: Create and activate a virtual environment

```bash
python -m venv venv
```

Windows CMD:

```cmd
venv\Scripts\activate
```

### Step 4: Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 5: Start the application

```bash
python -m streamlit run app.py
```

The Streamlit application will display a local URL in the terminal.

## 9. Testing and Validation

The following prescribed assignment scenarios were tested through the application:

| Test | Scenario | Observed Result |
|---|---|---|
| 1 | Shipping delay complaint | Pending follow-up after policy validation |
| 2 | Refund status request | Resolved |
| 3 | Password reset request | Resolved |
| 4 | Damaged blender complaint | Escalated |
| 5 | Duplicate payment and legal threat | Escalated |
| 6 | Unsupported corporate gift-card request | Escalated |

Additional validation:
- Python syntax compilation for agent modules.
- SQLite ticket creation and retrieval.
- Agent execution log verification.
- Escalation rule testing.
- Escalation record creation.
- Escalation review status update.
- Streamlit application testing.

## 10. Project Structure

```text
AI_Customer_Support/
│
├── agents/
│   ├── __init__.py
│   ├── query_agent.py
│   ├── knowledge_agent.py
│   ├── resolution_agent.py
│   └── log_agent.py
│
├── database/
│   ├── __init__.py
│   ├── db_connection.py
│   ├── db_operations.py
│   ├── schema.sql
│   └── knowledge_search.py
│
├── knowledge_base/
│   ├── shipping_policy.md
│   ├── refund_policy.md
│   ├── account_and_login.md
│   └── product_faq.md
│
├── logs/
├── screenshots/
├── app.py
├── team.py
├── requirements.txt
├── README.md
└── customer_support.db
```

## 11. Future Enhancements

- Vector database integration for semantic knowledge retrieval.
- Email and WhatsApp customer notifications.
- ServiceNow, Jira and CRM integration.
- Human-in-the-loop approval workflow.
- Multilingual customer support.
- Advanced reporting and analytics.
- Cloud deployment.

## 12. Conclusion

This project demonstrates how multiple AI agents can collaborate to automate customer support operations.

By combining local language models, policy-based knowledge retrieval, deterministic escalation rules and database logging, the application provides a practical foundation for an AI-powered customer support solution.

**Project:** ShopEase AI Customer Support Automation  
**Framework:** Microsoft AutoGen  
**LLM:** Ollama – Qwen3 4B Instruct  
**Interface:** Streamlit  
**Database:** SQLite
