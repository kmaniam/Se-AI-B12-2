
import os
import hashlib
import tempfile

import streamlit as st
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

st.set_page_config(
    page_title="Multi-PDF RAG Assistant",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Multi-PDF RAG Assistant")
st.write(
    "Upload multiple PDFs, index them together, and ask questions "
    "with file and page citations."
)

# --------------------------------------------------
# 1. Initialize Streamlit session state
# --------------------------------------------------
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "indexed_files" not in st.session_state:
    st.session_state.indexed_files = []

if "chunk_count" not in st.session_state:
    st.session_state.chunk_count = 0

if "index_signature" not in st.session_state:
    st.session_state.index_signature = None


# --------------------------------------------------
# 2. Configure the OpenAI API
# --------------------------------------------------
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error(
        "OPENAI_API_KEY is missing. Set it in your environment "
        "or in a .env file."
    )
    st.stop()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=api_key
)

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=api_key
)


# --------------------------------------------------
# 3. Upload multiple PDFs
# --------------------------------------------------
uploaded_files = st.file_uploader(
    "Upload your PDF documents",
    type=["pdf"],
    accept_multiple_files=True
)

chunk_size = st.sidebar.slider(
    "Chunk size",
    min_value=300,
    max_value=1500,
    value=800,
    step=100
)

chunk_overlap = st.sidebar.slider(
    "Chunk overlap",
    min_value=0,
    max_value=300,
    value=100,
    step=25
)

top_k = st.sidebar.slider(
    "Number of chunks to retrieve",
    min_value=2,
    max_value=10,
    value=5
)

if chunk_overlap >= chunk_size:
    st.error("Chunk overlap must be smaller than chunk size.")
    st.stop()


# --------------------------------------------------
# 4. Create a signature for the uploaded PDFs
# --------------------------------------------------
def get_upload_signature(files):
    digest = hashlib.sha256()

    for file in sorted(files, key=lambda item: item.name):
        digest.update(file.name.encode("utf-8"))
        digest.update(file.getvalue())

    digest.update(str(chunk_size).encode())
    digest.update(str(chunk_overlap).encode())

    return digest.hexdigest()


# --------------------------------------------------
# 5. Extract PDF pages and preserve metadata
# --------------------------------------------------
def load_pdf_pages(files):
    documents = []
    errors = []

    for uploaded_file in files:
        temp_path = None

        try:
            with tempfile.NamedTemporaryFile(
                suffix=".pdf", delete=False
            ) as temp_file:
                temp_file.write(uploaded_file.getvalue())
                temp_path = temp_file.name

            loader = PyPDFLoader(temp_path)
            pages = loader.load()

            for page_doc in pages:
                text = page_doc.page_content.strip()

                if not text:
                    continue

                # PyPDFLoader normally uses zero-based page metadata.
                original_page = page_doc.metadata.get("page", 0)

                page_doc.metadata["source"] = uploaded_file.name
                page_doc.metadata["page_number"] = int(original_page) + 1

                documents.append(page_doc)

        except Exception as exc:
            errors.append(
                f"{uploaded_file.name}: {exc}"
            )

        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)

    return documents, errors


# --------------------------------------------------
# 6. Chunk, embed, and build one FAISS index
# --------------------------------------------------
if st.button("Build / Rebuild Knowledge Base", type="primary"):

    if not uploaded_files:
        st.warning("Please upload at least one PDF.")
    else:
        with st.spinner("Reading PDFs and building FAISS index..."):

            try:
                pages, errors = load_pdf_pages(uploaded_files)

                for error in errors:
                    st.warning(f"Could not process {error}")

                if not pages:
                    st.error(
                        "No readable text was extracted. "
                        "Check whether the PDFs contain selectable text."
                    )
                    st.stop()

                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap,
                    add_start_index=True
                )

                chunks = splitter.split_documents(pages)

                if not chunks:
                    st.error("No text chunks were created.")
                    st.stop()

                # Every PDF is indexed in this one vector store.
                vector_store = FAISS.from_documents(
                    documents=chunks,
                    embedding=embeddings
                )

                st.session_state.vector_store = vector_store
                st.session_state.chunk_count = len(chunks)
                st.session_state.indexed_files = [
                    file.name for file in uploaded_files
                ]
                st.session_state.index_signature = (
                    get_upload_signature(uploaded_files)
                )

                st.success("Knowledge base built successfully!")

            except Exception as exc:
                st.error(f"Indexing failed: {exc}")


# --------------------------------------------------
# 7. Show indexing statistics
# --------------------------------------------------
if st.session_state.vector_store is not None:

    st.subheader("Knowledge Base Status")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Chunks indexed",
            st.session_state.chunk_count
        )

    with col2:
        st.metric(
            "PDF files indexed",
            len(st.session_state.indexed_files)
        )

    st.write("**Indexed files:**")
    for filename in st.session_state.indexed_files:
        st.write(f"- {filename}")


# --------------------------------------------------
# 8. Ask questions across all indexed PDFs
# --------------------------------------------------
st.divider()
st.subheader("Ask a Question")

question = st.text_input(
    "Enter your question",
    placeholder="Example: What are the main differences between these documents?"
)

if st.button("Get Answer"):

    if st.session_state.vector_store is None:
        st.warning("Build the knowledge base first.")

    elif not question.strip():
        st.warning("Please enter a question.")

    else:
        with st.spinner("Searching all indexed PDFs..."):

            try:
                retriever = st.session_state.vector_store.as_retriever(
                    search_kwargs={"k": top_k}
                )

                retrieved_docs = retriever.invoke(question)

                if not retrieved_docs:
                    st.warning(
                        "No relevant document sections were retrieved."
                    )
                    st.stop()

                # Keep the exact source metadata beside each passage.
                context_parts = []
                sources = []
                seen_sources = set()

                for doc in retrieved_docs:
                    filename = doc.metadata.get(
                        "source", "Unknown file"
                    )
                    page_number = doc.metadata.get(
                        "page_number", "Unknown"
                    )

                    source_id = (filename, page_number)

                    context_parts.append(
                        f"[Source: {filename}, Page: {page_number}]\n"
                        f"{doc.page_content}"
                    )

                    if source_id not in seen_sources:
                        sources.append({
                            "file": filename,
                            "page": page_number,
                            "content": doc.page_content
                        })
                        seen_sources.add(source_id)

                context = "\n\n---\n\n".join(context_parts)

                prompt = ChatPromptTemplate.from_messages([
                    (
                        "system",
                        """You are a document question-answering assistant.

Answer using only the supplied retrieved document passages.

Rules:
1. Cite factual claims with the exact source filename and page number
   supplied in the context, using [filename, p. N].
2. Never invent a source, page number, quotation, or fact.
3. If the evidence is insufficient, say so clearly.
4. If two documents disagree about the same fact, explicitly explain
   the disagreement and cite both sources. Do not silently select one.
5. Distinguish direct evidence from your own inference.
6. If sources describe different dates, versions, definitions, or
   circumstances, check whether the apparent disagreement may be
   explained by those differences.
7. The retrieved passages may not represent every document. Do not
   claim that all documents agree or disagree unless the evidence
   supports that conclusion.
8. Be concise, factual, and transparent about uncertainty.

Retrieved passages:
{context}"""
                    ),
                    (
                        "human",
                        "Question: {question}"
                    )
                ])

                chain = prompt | llm

                response = chain.invoke({
                    "context": context,
                    "question": question
                })

                st.subheader("Answer")
                st.markdown(response.content)

                st.subheader("Retrieved Sources")
                st.caption(
                    "These are the passages supplied to the model, "
                    "not necessarily every relevant passage in the PDFs."
                )

                for index, source in enumerate(sources, start=1):
                    with st.expander(
                        f"{index}. {source['file']} — "
                        f"Page {source['page']}"
                    ):
                        st.write(source["content"])

            except Exception as exc:
                st.error(f"Question answering failed: {exc}")
