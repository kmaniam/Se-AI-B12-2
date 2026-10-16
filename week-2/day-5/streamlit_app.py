
import uuid
import streamlit as st

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Page configuration
st.set_page_config(
    page_title="My GenAI Chatbot",
    page_icon="🤖"
)

st.title("My First LangChain GenAI App")
st.caption("Powered by LangChain, Ollama and Qwen 2.5")

# Initialize chatbot once
@st.cache_resource
def create_chatbot():
    llm = ChatOllama(
        model="qwen2.5:3b",
        temperature=0
    )

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a helpful database trainer. "
            "Explain concepts in simple English with examples."
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}")
    ])

    chain = prompt | llm | StrOutputParser()
    histories = {}

    def get_session_history(session_id: str):
        if session_id not in histories:
            histories[session_id] = InMemoryChatMessageHistory()
        return histories[session_id]

    return RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="history"
    )

chatbot = create_chatbot()

# Initialize a fresh conversation
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear Chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.session_state.session_id = str(uuid.uuid4())
    st.rerun()

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept a new question
question = st.chat_input("Ask a database question...")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Generating answer..."):
            try:
                answer = chatbot.invoke(
                    {"question": question},
                    config={
                        "configurable": {
                            "session_id": st.session_state.session_id
                        }
                    }
                )

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception:
                st.error(
                    "Unable to generate an answer. "
                    "Check that Ollama is running and "
                    "the qwen2.5:3b model is available."
                )
