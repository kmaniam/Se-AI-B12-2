
import asyncio
import streamlit as st
import pandas as pd

from database.db_operations import get_all_tickets
from team import run_support_workflow
from team import run_support_workflow_fast

from database.db_operations import (
    get_all_escalations,
    update_escalation,
)

# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="ShopEase AI Customer Support",
    page_icon="🎧",
    layout="wide",
)

st.title("🎧 ShopEase AI Customer Support")
st.caption(
    "AI-powered customer complaint analysis and resolution"
)

st.divider()


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:
    st.header("🤖 AI Support System")

    st.success("Ollama: Connected")
    st.success("SQLite: Enabled")

    st.markdown("### Agent Workflow")
    st.write("1. 🔍 Query Agent")
    st.write("2. 📚 Knowledge Agent")
    st.write("3. 💬 Resolution Agent")
    st.write("4. 📝 Log Agent")

    st.divider()

    st.caption("Powered by AutoGen + Ollama + Streamlit")


# --------------------------------------------------
# Customer input
# --------------------------------------------------

st.subheader("📝 Customer Complaint")

with st.form("customer_support_form"):

    customer_name = st.text_input(
        "Customer Name",
        placeholder="Enter customer name",
    )

    order_id = st.text_input(
        "Order ID",
        placeholder="Example: ORD-4512",
    )

    complaint = st.text_area(
        "Customer Complaint",
        placeholder="Describe the customer's issue...",
        height=150,
    )

    submitted = st.form_submit_button(
        "🚀 Process Complaint",
        type="primary",
        use_container_width=True,
    )


# --------------------------------------------------
# Process complaint
# --------------------------------------------------

if submitted:

    if not customer_name.strip():
        st.error("Please enter the customer name.")

    elif not order_id.strip():
        st.error("Please enter the order ID.")

    elif not complaint.strip():
        st.error("Please enter the customer complaint.")

    else:

        try:
            with st.spinner(
                "AI agents are processing the customer complaint..."
            ):
                result = asyncio.run(
                    run_support_workflow_fast(
                        customer_name=customer_name.strip(),
                        order_id=order_id.strip(),
                        complaint=complaint.strip(),
                    )
                )

            st.divider()
            st.subheader("📊 Support Workflow Result")

            if "log_result" not in result:
                st.error(
                    "Workflow did not complete ticket logging. "
                    "Please check the terminal output."
                )

            else:
                ticket = result["log_result"]
                query = result["query_analysis"]
                resolution = result["resolution_result"]

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Ticket ID",
                    ticket["ticket_id"],
                )

                col2.metric(
                    "Category",
                    query["category"],
                )

                col3.metric(
                    "Confidence",
                    f'{resolution["confidence"]:.0%}',
                )
                st.metric(
                    "Total Processing Time",
                    f'{result["total_execution_time"]} seconds',
                )

                if ticket["status"] == "Escalated":
                    st.error("🚨 Ticket Escalated to Human Support")

                elif ticket["status"] == "Pending":
                    st.warning("⏳ Ticket Pending - Awaiting Follow-up")

                elif ticket["status"] == "Resolved":
                    st.success("✅ Ticket Resolved")

                else:
                    st.info(f"Ticket Status: {ticket['status']}")

                st.markdown("### 💬 Customer Response")

                st.info(resolution["response"])

                with st.expander("View Agent Analysis"):
                    st.markdown("**Query Agent**")
                    st.json(query)

                    st.markdown("**Knowledge Agent**")
                    st.json(result["knowledge_result"])

                    st.markdown("**Resolution Agent**")
                    st.json(resolution)

                    st.markdown("**Log Agent**")
                    st.json(ticket)

        except Exception as error:
            st.error(f"Workflow failed: {error}")
            st.exception(error)

# --------------------------------------------------
# Ticket History Dashboard
# --------------------------------------------------


# --------------------------------------------------
# Ticket History Dashboard
# --------------------------------------------------

st.divider()
st.title("📋 Ticket History")

tickets = get_all_tickets()

if tickets:

    df = pd.DataFrame([dict(ticket) for ticket in tickets])

    # Status summary
    pending_count = (df["status"] == "Pending").sum()
    resolved_count = (df["status"] == "Resolved").sum()
    escalated_count = (df["status"] == "Escalated").sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("⏳ Pending", pending_count)
    col2.metric("✅ Resolved", resolved_count)
    col3.metric("🚨 Escalated", escalated_count)

    st.divider()

    # Filters
    filter_col, search_col = st.columns([1, 2])

    with filter_col:
        selected_status = st.selectbox(
            "Filter by Status",
            ["All", "Pending", "Resolved", "Escalated"],
        )

    with search_col:
        search_text = st.text_input(
            "Search Customer Name or Order ID"
        )

    filtered_df = df.copy()

    if selected_status != "All":
        filtered_df = filtered_df[
            filtered_df["status"] == selected_status
        ]

    if search_text:
        mask = (
            filtered_df["customer_name"].astype(str)
            .str.contains(search_text, case=False, na=False)
            |
            filtered_df["order_id"].astype(str)
            .str.contains(search_text, case=False, na=False)
        )
        filtered_df = filtered_df[mask]

    st.subheader(f"Tickets ({len(filtered_df)})")

    # Display only important columns
    display_columns = [
        "ticket_id",
        "customer_name",
        "order_id",
        "category",
        "urgency",
        "status",
        "created_at",
    ]

    available_columns = [
        col for col in display_columns
        if col in filtered_df.columns
    ]

    st.dataframe(
        filtered_df[available_columns],
        use_container_width=True,
        hide_index=True,
    )

    # Ticket details
    st.subheader("🔎 Ticket Details")

    if not filtered_df.empty:

        selected_ticket = st.selectbox(
            "Select Ticket ID",
            filtered_df["ticket_id"].tolist(),
        )

        ticket = df[
            df["ticket_id"] == selected_ticket
        ].iloc[0]

        st.markdown(f"**Customer:** {ticket['customer_name']}")
        st.markdown(f"**Order ID:** {ticket['order_id']}")
        st.markdown(f"**Category:** {ticket['category']}")
        st.markdown(f"**Urgency:** {ticket['urgency']}")
        st.markdown(f"**Status:** {ticket['status']}")

        st.markdown("**Customer Complaint**")
        st.info(ticket["complaint"])

        st.markdown("**Generated Customer Response**")
        st.success(ticket["response"])

        if ticket.get("escalation_reason"):
            st.warning(
                f"Escalation Reason: {ticket['escalation_reason']}"
            )

    else:
        st.info("No tickets match the selected filters.")

    # CSV export
    st.divider()

    csv_data = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "⬇️ Download Ticket Report",
        data=csv_data,
        file_name="shopease_ticket_history.csv",
        mime="text/csv",
    )

else:
    st.info("No customer support tickets available.")


# --------------------------------------------------
# Escalation Management Dashboard
# --------------------------------------------------

st.divider()
st.title("🚨 Escalation Management")

escalations = get_all_escalations()

if escalations:

    escalation_df = pd.DataFrame(
        [dict(row) for row in escalations]
    )

    pending_reviews = (
        escalation_df["escalation_status"] == "Pending"
    ).sum()

    resolved_reviews = (
        escalation_df["escalation_status"] == "Resolved"
    ).sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Escalations", len(escalation_df))
    col2.metric("Awaiting Review", int(pending_reviews))
    col3.metric("Reviewed", int(resolved_reviews))

    st.subheader("Escalated Tickets")

    st.dataframe(
        escalation_df[
            [
                "escalation_id",
                "ticket_id",
                "customer_name",
                "order_id",
                "escalation_reason",
                "assigned_to",
                "escalation_status",
                "created_at",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

    st.divider()
    st.subheader("🔎 Review Escalation")

    selected_id = st.selectbox(
        "Select Escalation",
        escalation_df["escalation_id"].tolist(),
        format_func=lambda value: (
            f"Escalation #{value} - "
            + str(
                escalation_df.loc[
                    escalation_df["escalation_id"] == value,
                    "customer_name"
                ].iloc[0]
            )
        ),
    )

    selected = escalation_df[
        escalation_df["escalation_id"] == selected_id
    ].iloc[0]

    st.markdown(f"**Ticket ID:** {selected['ticket_id']}")
    st.markdown(f"**Customer:** {selected['customer_name']}")
    st.markdown(f"**Order ID:** {selected['order_id']}")
    st.markdown(f"**Escalation Reason:** {selected['escalation_reason']}")

    st.markdown("**Original Complaint**")
    st.info(selected["complaint"])

    st.markdown("**AI-Generated Response**")
    st.write(selected["response"])

    with st.form("escalation_review_form"):

        assigned_to = st.text_input(
            "Assigned Support Person",
            value=selected["assigned_to"] or "Human Support",
        )

        current_status = selected["escalation_status"]

        status_options = [
            "Pending",
            "In Progress",
            "Resolved",
        ]

        status_index = (
            status_options.index(current_status)
            if current_status in status_options
            else 0
        )

        review_status = st.selectbox(
            "Review Status",
            status_options,
            index=status_index,
        )

        save_review = st.form_submit_button(
            "💾 Save Escalation Review",
            use_container_width=True,
        )

        if save_review:

            if not assigned_to.strip():
                st.error("Please enter an assigned support person.")

            else:
                update_escalation(
                    escalation_id=int(selected_id),
                    assigned_to=assigned_to.strip(),
                    escalation_status=review_status,
                )

                st.success("Escalation review updated successfully.")

                st.rerun()

else:
    st.success("No escalated tickets currently require review.")
