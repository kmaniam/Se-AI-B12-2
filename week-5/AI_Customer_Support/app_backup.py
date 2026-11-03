
import asyncio
import streamlit as st

from team import run_support_workflow


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
                    run_support_workflow(
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

                if ticket["status"] == "Escalated":
                    st.error("🚨 Ticket Escalated to Human Support")
                else:
                    st.success("✅ Ticket Resolved")

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
