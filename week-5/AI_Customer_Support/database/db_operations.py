import uuid
from datetime import datetime
from database.db_connection import get_connection


def generate_ticket_id():

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    unique_id = uuid.uuid4().hex[:4].upper()

    return f"TKT-{timestamp}-{unique_id}"


def create_ticket(
    complaint,
    customer_name=None,
    order_id=None,
    category=None,
    urgency=None,
    sentiment=None,
    kb_sources=None,
    response=None,
    confidence=None,
    status="Open",
    escalation_reason=None
):

    ticket_id = generate_ticket_id()

    created_at = datetime.now().astimezone().isoformat()

    with get_connection() as connection:

        cursor = connection.execute(
            """
            INSERT INTO tickets (
                ticket_id,
                customer_name,
                order_id,
                complaint,
                category,
                urgency,
                sentiment,
                kb_sources,
                response,
                confidence,
                status,
                escalation_reason,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                ticket_id,
                customer_name,
                order_id,
                complaint,
                category,
                urgency,
                sentiment,
                kb_sources,
                response,
                confidence,
                status,
                escalation_reason,
                created_at
            )
        )

    return ticket_id


def get_all_tickets():

    with get_connection() as connection:

        rows = connection.execute(
            """
            SELECT *
            FROM tickets
            ORDER BY created_at DESC
            """
        ).fetchall()

    return [dict(row) for row in rows]


def get_ticket(ticket_id):

    with get_connection() as connection:

        row = connection.execute(
            """
            SELECT *
            FROM tickets
            WHERE ticket_id = ?
            """,
            (ticket_id,)
        ).fetchone()

    return dict(row) if row else None


def log_agent_execution(
    ticket_id,
    agent_name,
    input_data,
    output_data,
    execution_status="Success"
):

    with get_connection() as connection:

        connection.execute(
            """
            INSERT INTO agent_execution_logs (
                ticket_id,
                agent_name,
                input_data,
                output_data,
                execution_status
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                ticket_id,
                agent_name,
                input_data,
                output_data,
                execution_status
            )
        )


def create_escalation(ticket_id, reason):

    with get_connection() as connection:

        connection.execute(
            """
            INSERT INTO escalations (
                ticket_id,
                escalation_reason
            )
            VALUES (?, ?)
            """,
            (ticket_id, reason)
        )

# --------------------------------------------------
# Escalation Management
# --------------------------------------------------

def get_all_escalations():
    with get_connection() as connection:
        rows = connection.execute("""
            SELECT
                e.escalation_id,
                e.ticket_id,
                t.customer_name,
                t.order_id,
                t.complaint,
                t.response,
                e.escalation_reason,
                e.assigned_to,
                e.escalation_status,
                e.created_at,
                e.resolved_at
            FROM escalations e
            JOIN tickets t
                ON e.ticket_id = t.ticket_id
            ORDER BY e.created_at DESC
        """).fetchall()

        return rows



def update_escalation(
    escalation_id,
    assigned_to=None,
    escalation_status=None,
):
    with get_connection() as connection:

        # Retrieve the ticket linked to this escalation
        escalation = connection.execute("""
            SELECT ticket_id
            FROM escalations
            WHERE escalation_id = ?
        """, (escalation_id,)).fetchone()

        if not escalation:
            raise ValueError(
                f"Escalation {escalation_id} not found."
            )

        ticket_id = escalation["ticket_id"]

        if assigned_to is not None:
            connection.execute("""
                UPDATE escalations
                SET assigned_to = ?
                WHERE escalation_id = ?
            """, (assigned_to, escalation_id))

        if escalation_status is not None:

            if escalation_status not in [
                "Pending",
                "In Progress",
                "Resolved",
            ]:
                raise ValueError("Invalid escalation status.")

            connection.execute("""
                UPDATE escalations
                SET escalation_status = ?,
                    resolved_at = CASE
                        WHEN ? = 'Resolved'
                        THEN CURRENT_TIMESTAMP
                        ELSE NULL
                    END
                WHERE escalation_id = ?
            """, (
                escalation_status,
                escalation_status,
                escalation_id,
            ))

            # Synchronize the main ticket status
            ticket_status = (
                "Resolved"
                if escalation_status == "Resolved"
                else "Escalated"
            )

            connection.execute("""
                UPDATE tickets
                SET status = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE ticket_id = ?
            """, (ticket_status, ticket_id))



def get_escalation_by_ticket(ticket_id):
    with get_connection() as connection:
        return connection.execute("""
            SELECT *
            FROM escalations
            WHERE ticket_id = ?
        """, (ticket_id,)).fetchone()



if __name__ == "__main__":

    from database.db_connection import initialize_database

    initialize_database()

    ticket_id = create_ticket(
        customer_name="Priya",
        order_id="ORD-4512",
        complaint="My order is delayed by 10 days.",
        category="Shipping",
        urgency="High",
        sentiment="Negative",
        kb_sources="shipping_policy.md",
        response="We apologize for the delay. Our support team will investigate.",
        confidence=0.90,
        status="Escalated",
        escalation_reason="High urgency"
    )

    print("\nTicket created successfully!")
    print("Ticket ID:", ticket_id)

    ticket = get_ticket(ticket_id)

    print("\nRetrieved ticket:")
    print(ticket)