# Local Oracle DBA AI Assistant — Project Test Log

**Project:** `week-2/day-5`  
**Status:** RAG chatbot working; retrieval evaluation and agent capabilities are future work.  
**Last updated:** 16 October 2026

## 1. Project environment

- **LLM runtime:** Ollama
- **Chat model:** `qwen2.5:3b`
- **Embedding model:** `nomic-embed-text`
- **Framework:** LangChain
- **Vector store:** Chroma
- **UI:** Streamlit
- **Persistent Chroma directory:** `./oracle_chroma_db`
- **Collection:** `oracle_notes`

The Python virtual environment is in the parent `Program_AI\venv` directory. The project folder is:

```text
C:\Users\kesav\OneDrive\Documents\Program_AI\week-2\day-5
```

## 2. Features implemented

- Local chat using Ollama and LangChain.
- Chat prompt templates and LCEL chain.
- Conversation history and follow-up question rewriting.
- Retrieval-Augmented Generation (RAG) using Chroma.
- Oracle notes split into chunks and embedded locally.
- Streamlit chat interface.
- `.txt` and `.pdf` upload and indexing.
- Duplicate-upload check using a file hash.
- Indexed-document listing and document removal by source.
- Retrieval of up to four chunks (`k=4`).
- Distance filter set to `MAX_DISTANCE = 0.75`.
- Display of retrieved source passages and Chroma distance scores.
- Fallback response when no retrieved result passes the distance filter.

## 3. Knowledge-base files

### `oracle_notes.txt`

Contains ten Oracle DBA topics:

1. Tablespaces and datafiles
2. Indexes and SQL performance
3. RMAN backup, restore, and recovery
4. Database startup and shutdown
5. Alert log and ADR
6. Tablespace space management
7. Oracle Enterprise Manager (OEM)
8. Performance troubleshooting
9. Transactions and undo
10. Backup and recovery validation

### `oracle_test_notes.txt`

Contains a short Data Guard test document:

```text
Oracle Data Guard protects a database by maintaining a standby database.
A physical standby database applies redo data from the primary database.
```

## 4. Rebuilding the Chroma collection

The knowledge base was rebuilt after the collection was accidentally emptied. The rebuild loaded both files and reported:

```text
Loaded: oracle_notes.txt
Loaded: oracle_test_notes.txt
Documents loaded: 2
Chunks created: 29
Existing chunks: 28
Old collection deleted.
New chunks stored: 29
Oracle knowledge base rebuilt successfully!
```

A LangChain deprecation warning was observed during setup; it did not prevent the rebuild.

**Caution:** `store_oracle_notes.py` deletes and recreates the existing collection during a rebuild. Back up any documents indexed only through the UI before running it, because rebuilding from the two configured files will not preserve other uploaded documents unless the script is updated to include them.

## 5. Tests with recorded output

### Test A — RMAN purpose

**Question**

> What is the purpose of Oracle RMAN?

**Observed retrieved sources**

| Source | Chroma distance |
|---|---:|
| `oracle_notes.txt` — RMAN utility used to back up, restore, and recover; backup validation | `0.4091` |
| `oracle_notes.txt` — section heading “RMAN BACKUP, RESTORE, AND RECOVERY” | `0.6398` |

**Assessment:** The retrieved passages were relevant to the RMAN question.

### Test B — Oracle Data Guard

**Question**

> What is the purpose of Oracle Data Guard, and how does a physical standby database work?

**Observed retrieved sources**

| Source | Chroma distance | Assessment |
|---|---:|---|
| `oracle_test_notes.txt` — Data Guard protects the database with a standby; physical standby applies primary redo | `0.1627` | Strongly relevant |
| `oracle_notes.txt` — OEM monitoring | `0.6461` | Unrelated to the question |
| `oracle_notes.txt` — tablespaces and datafiles | `0.6892` | Unrelated to the question |
| `oracle_notes.txt` — startup and shutdown section | `0.7102` | Unrelated to the question |

**Assessment:** The correct Data Guard document ranked first, but the other chunks were also accepted by the current `0.75` distance threshold. This demonstrates that distance filtering alone does not guarantee that every retrieved chunk is topically relevant.

### Test C — Unsupported TDE question

**Question**

> How do I configure Oracle Transparent Data Encryption (TDE) and manage the keystore?

**Observed behavior:** The app displayed the fallback message:

> I couldn't find sufficiently relevant information in the indexed Oracle DBA documents to answer this question reliably. Please add relevant documentation or rephrase your question.

**Assessment:** This is the intended behavior when the indexed content does not provide sufficient evidence for an answer.

## 6. Tests run, but output not recorded here

The following questions were confirmed as tested, but their retrieved passages, scores, and full answers were not shared in the project conversation. Their outcomes therefore remain **unverified in this log**.

- **Tablespace:** “How do I troubleshoot a tablespace running out of space?”
- **Performance:** “What should I check when an Oracle database is running slowly?”

Record the top retrieved sources, distance scores, and whether the answer is supported before marking these tests as passed.

## 7. Current retrieval settings and limitations

- Retrieval count: `k=4`
- Distance threshold: `MAX_DISTANCE = 0.75`
- The app filters retrieved results by distance before building the context.
- The source expander displays the filtered results and their scores.
- The TDE test shows that the app can decline to answer when no result passes the configured threshold.
- A passing distance threshold is not proof of semantic relevance. The Data Guard test returned three unrelated chunks that were still under the threshold.
- The threshold should not be changed blindly; evaluate several representative questions first.
- The test corpus is small and is not yet a comprehensive Oracle DBA knowledge base.

## 8. Run commands

Run these commands from the project directory in Command Prompt, with the parent virtual environment activated:

```bat
cd C:\Users\kesav\OneDrive\Documents\Program_AI\week-2\day-5
streamlit run rag_streamlit_app.py
```

To rebuild the configured knowledge base:

```bat
python store_oracle_notes.py
```

Only run the rebuild command when you intend to replace the current Chroma collection with the files configured in `store_oracle_notes.py`.

## 9. Next steps

1. Record and review the actual outputs for the tablespace and performance tests.
2. Create a small repeatable evaluation set with expected relevant sources and expected answer behavior.
3. Improve retrieval quality based on measured results, rather than changing the distance threshold without evidence.
4. Add more trusted Oracle DBA documents and error-specific runbooks.
5. Add diagnostic analysis for uploaded alert logs and other reports.
6. Introduce read-only diagnostic tools with strict input validation and audit logging.
7. Add approval gates and test-environment checks before any state-changing operation. Do not allow an LLM to execute arbitrary SQL or production changes autonomously.

## 10. Project direction

The goal is to learn and gradually build a complete local Oracle DBA AI assistant, progressing from RAG to document-grounded diagnostics, controlled tool use, and eventually a safety-conscious agent. Each step should be tested and confirmed before moving to the next.
