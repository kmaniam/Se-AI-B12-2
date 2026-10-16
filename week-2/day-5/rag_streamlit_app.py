import hashlib
import io
import os
import uuid

import streamlit as st
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader


# --------------------------------------------------
# Step 1: Configure the Streamlit page
# --------------------------------------------------
st.set_page_config(
    page_title="Oracle DBA Knowledge Assistant",
    page_icon="🗄️",
    layout="wide"
)

st.title("🗄️ Oracle DBA Knowledge Assistant")
st.caption(
    "Powered by LangChain, Chroma, and local Ollama models"
)

# --------------------------------------------------
# Step 2: Initialize models and the vector database
# --------------------------------------------------
@st.cache_resource
def initialize_rag():

    # Step 1: Create the embedding model
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    # Step 2: Load the Chroma vector database
    st.write("Chroma database path:", os.path.abspath("./oracle_chroma_db"))
    vector_store = Chroma(
        collection_name="oracle_notes",
        embedding_function=embeddings,
        persist_directory="./oracle_chroma_db"
    )

    # Step 3: Initialize the local chat model
    llm = ChatOllama(
        model="qwen2.5:3b",
        temperature=0
    )

            # Step 4: Prompt for answering questions
    prompt = ChatPromptTemplate.from_template("""
        You are an experienced Oracle DBA assistant.

            Answer the user's question using the supplied context
            and conversation history.

            Rules:
            1. Use the supplied context as the primary evidence
            for factual Oracle DBA answers.
            2. Do not invent facts, SQL results, configuration
            values, or document references.
            3. If the context does not support a requested detail,
            explicitly state that the available documentation
            does not establish it.
            4. Distinguish documented facts from general recommendations.
            5. For potentially risky production changes, explain
            the need for validation and an appropriate change plan.
            6. Keep the answer relevant to the user's question.
            7. Before answering, check whether the supplied context
            directly supports the requested topic. If it does not,
            state that the indexed documents do not contain enough
            evidence. Do not answer from general knowledge as if
            it came from the retrieved documents.

            Conversation history:
            {chat_history}

            Context:
            {context}

            Question:
            {question}

            Answer:
            """)

    # Step 5: Prompt for rewriting follow-up questions
    rewrite_prompt = ChatPromptTemplate.from_template("""
        Rewrite the latest user question as a standalone question
        that can be understood without reading the conversation history.

        Use the conversation history to resolve references such as
        "it", "they", "those", and "that".

        Do not answer the question. Return only the rewritten question.

        Conversation history:
        {chat_history}

        Latest question:
        {question}

        Standalone question:
        """)
    
    # Step 6: Return all four components
    return vector_store, llm, prompt, rewrite_prompt


# Initialize the RAG components
vector_store, llm, prompt, rewrite_prompt = initialize_rag()

# Step 17.4: List indexed documents
st.subheader("Indexed Oracle DBA Documents")

try:
    stored_data = vector_store.get(
        include=["metadatas"]
    )

    indexed_files = sorted({
        metadata.get("source", "Unknown")
        for metadata in stored_data.get("metadatas", [])
        if metadata
    })

    if indexed_files:
        for filename in indexed_files:
            st.write(f"📄 {filename}")
    else:
        st.info("No documents are indexed yet.")

except Exception as error:
    st.error("Unable to list indexed documents.")
    print(f"Document listing error: {error}")



with st.expander("View Indexed Documents"):
    stored_data = vector_store.get(include=["metadatas"])

    sources = sorted({
        metadata.get("source", "Unknown")
        for metadata in (stored_data.get("metadatas") or [])
        if metadata
    })

    if sources:
        st.write(f"Indexed documents: {len(sources)}")

        for source in sources:
            st.write(f"📄 {source}")

        selected_source = st.selectbox(
            "Select a document to remove",
            sources,
            key="document_to_remove"
        )

        if st.button("Remove Selected Document"):
            matching_records = vector_store.get(
                where={"source": selected_source},
                include=["metadatas"]
            )

            record_ids = matching_records.get("ids", [])

            if record_ids:
                vector_store.delete(ids=record_ids)
                st.success(
                    f"Removed {len(record_ids)} chunks from {selected_source}."
                )
                st.rerun()
            else:
                st.warning("No indexed chunks found for this document.")
    else:
        st.info("No documents have been indexed yet.")

# Step 16.6A: Upload additional DBA documents
st.subheader("📚 Add DBA Documents")

uploaded_files = st.file_uploader(
    "Upload Oracle DBA documentation",
    type=["txt", "pdf"],
    accept_multiple_files=True,
    help="Upload TXT or PDF documents to expand your local knowledge base."
)


if st.button("Index Selected Documents"):
    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        total_chunks = 0
        indexed_files = 0
        skipped_files = 0

        for uploaded_file in uploaded_files:
            file_bytes = uploaded_file.getvalue()
            file_hash = hashlib.sha256(file_bytes).hexdigest()

            # Check whether this exact file was indexed before
            existing = vector_store.get(
                where={"file_hash": file_hash},
                limit=1
            )

            if existing.get("ids"):
                st.info(
                    f"Skipped {uploaded_file.name}: "
                    "this file is already indexed."
                )
                skipped_files += 1
                continue

            # Read the uploaded file
            if uploaded_file.name.lower().endswith(".txt"):
                text = file_bytes.decode("utf-8-sig")
            else:
                pdf_reader = PdfReader(io.BytesIO(file_bytes))
                text = "\n".join(
                    page.extract_text() or ""
                    for page in pdf_reader.pages
                )

            if not text.strip():
                st.warning(
                    f"No extractable text found in "
                    f"{uploaded_file.name}."
                )
                continue

            document = Document(
                page_content=text,
                metadata={
                    "source": uploaded_file.name,
                    "file_hash": file_hash
                }
            )

            chunks = splitter.split_documents([document])

            if not chunks:
                st.warning(
                    f"No text chunks created for {uploaded_file.name}."
                )
                continue

            vector_store.add_documents(chunks)

            total_chunks += len(chunks)
            indexed_files += 1

        if indexed_files:
            st.success(
                f"Indexed {indexed_files} file(s), "
                f"adding {total_chunks} chunks."
            )

        if skipped_files:
            st.info(f"Skipped {skipped_files} previously indexed file(s).")

        if indexed_files == 0 and skipped_files == 0:
            st.warning("No documents were indexed.")

    except Exception as error:
        st.error("Document indexing failed.")
        st.exception(error)
        print(f"Indexing error: {error}")


# --------------------------------------------------
# Step 3: Initialize Streamlit session state
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())


# --------------------------------------------------
# Step 4: Clear Chat button
# --------------------------------------------------
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.session_state.session_id = str(uuid.uuid4())
    st.rerun()


# --------------------------------------------------
# Step 5: Display previous conversation messages
# --------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --------------------------------------------------
# Step 6: Accept a new question
# --------------------------------------------------
question = st.chat_input("Ask an Oracle DBA question...")


if question:

    # Display the user's question
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # Generate the assistant's response
    with st.chat_message("assistant"):

        with st.spinner(
            "Searching Oracle notes and generating an answer..."
        ):

            try:
                # ------------------------------------------
                # Step 7: Retrieve documents and scores
                # ------------------------------------------
                
                # Build history from previous conversation messages.
                # The latest user question is already stored in session state.
                history_messages = st.session_state.messages[:-1]

                chat_history = "\n".join(
                    f"{'User' if message['role'] == 'user' else 'Assistant'}: "
                    f"{message['content']}"
                    for message in history_messages
                )

                # Rewrite the latest question as a standalone search query.
                rewrite_messages = rewrite_prompt.format_messages(
                    chat_history=chat_history or "No previous conversation.",
                    question=question
                )

                standalone_question = llm.invoke(rewrite_messages).content.strip()


            # Use the rewritten question to search Chroma.
                results = vector_store.similarity_search_with_score(
                    standalone_question,
                    k=4
                )

                MAX_DISTANCE = 0.75

                relevant_results = [
                    (doc, distance)
                    for doc, distance in results
                    if distance <= MAX_DISTANCE
                ]

                if not relevant_results:
                    answer = (
                        "I couldn't find sufficiently relevant information "
                        "in the indexed Oracle DBA documents to answer "
                        "this question reliably. Please add relevant "
                        "documentation or rephrase your question."
                    )

                    # No LLM call when retrieval returns no relevant chunks.
                    st.warning(answer)

                else:
                    # Build context only from chunks that passed the threshold.
                    context = "\n\n".join(
                        doc.page_content
                        for doc, distance in relevant_results
                    )

                    # Use your existing answer prompt.
                    answer_prompt = prompt.format_messages(
                        chat_history=chat_history,
                        context=context,
                        question=standalone_question
                    )

                    # Qwen is called only when relevant chunks exist.
                    response = llm.invoke(answer_prompt)
                    answer = response.content

                    # Display sources used for this answer.
                    with st.expander("View retrieved source documents and scores"):
                        for index, (doc, distance) in enumerate(
                            relevant_results, start=1
                        ):
                            st.markdown(f"### Source {index}")
                            st.caption(
                                f"File: {doc.metadata.get('source', 'Unknown')}"
                            )
                            st.caption(f"Chroma distance score: {distance:.4f}")
                            st.write(doc.page_content)

# Keep your existing chat-history update logic after this block.
# Ensure the answer is displayed and stored only once.

                # # Extract retrieved documents.
                # documents = [document for document, score in results]

                # context = "\n\n".join(
                #     document.page_content for document in documents
                # )

                # # ------------------------------------------
                # # Step 8: Generate an answer using the LLM
                # # ------------------------------------------
                # if not documents:
                #     answer = (
                #         "No relevant Oracle notes were retrieved. "
                #         "Please add relevant documentation "
                #         "to the knowledge base."
                #     )
                # else:
                    
                #     # Build conversation history from previous messages.
                #     # Exclude the current question, which is passed separately.
                #     history_messages = st.session_state.messages[:-1]

                #     chat_history = "\n".join(
                #         f"{'User' if message['role'] == 'user' else 'Assistant'}: "
                #         f"{message['content']}"
                #         for message in history_messages
                #     )

                #     # Pass history, retrieved context, and current question to the prompt
                #     messages = prompt.format_messages(
                #         chat_history=chat_history or "No previous conversation.",
                #         context=context,
                #         question=question
                #     )

                #     response = llm.invoke(messages)
                #     answer = response.content

                # # Display the answer
                # st.markdown(answer)

                # # ------------------------------------------
                # # Step 9: Display source documents and scores
                # # ------------------------------------------
                
                # with st.expander(
                #     "View retrieved source documents and scores"
                # ):
                       
                #     if results:

                #         for i, (document, score) in enumerate(
                #             results,
                #             start=1
                #         ):

                #             st.markdown(f"### Source {i}")

                #             st.caption(
                #                 "File: "
                #                 + str(
                #                     document.metadata.get(
                #                         "source",
                #                         "Unknown"
                #                     )
                #                 )
                #             )

                #             st.metric(
                #                 label="Chroma distance score",
                #                 value=f"{float(score):.4f}"
                #             )

                #             st.text(document.page_content)

                #             st.divider()

                #     else:
                #         st.info(
                #             "No source documents were retrieved."
                #         )

            except Exception as error:

                answer = (
                    "I couldn't process your question. "
                    "Please check that Ollama is running, "
                    "the required models are available, and "
                    "the Chroma database can be accessed."
                )

                st.error(answer)

                # Print the detailed error in the terminal
                print(f"RAG error: {error}")


    # ----------------------------------------------
    # Step 10: Save the assistant's response
    # ----------------------------------------------
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
