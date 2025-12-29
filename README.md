# 📘 Research Paper RAG Assistant

A **modular, production-oriented GenAI application** for ingesting research papers (PDFs) and enabling **semantic search, question answering, and summarization** using **Retrieval-Augmented Generation (RAG)**.

Built with **LangChain**, **FAISS**, **Groq LLM**, and **Streamlit**, following **clean architecture, SOLID principles**, and strict separation of concerns.

---

## ✨ Key Features

* 📄 Upload and process research papers (PDF)
* 🧠 Semantic search over document content
* 💬 Context-aware Q&A using RAG
* 🧩 Optional section-aware retrieval
* 📚 Source-grounded answers with citations
* 🧼 Explicit document lifecycle (select → process → replace)
* 🖥️ Clean, interactive Streamlit UI

---

## 🧱 High-Level Architecture

```text
Streamlit UI (app.py)
│
├── ui/
│   ├── components.py        # sidebar, upload, session state
│   ├── chat_interface.py    # chat rendering
│   └── helpers.py           # system wiring
│
├── orchestrator.py          # system coordinator
│
├── core/
│   ├── loaders/             # PDF loaders
│   ├── processors/          # section extractor, chunker
│   ├── embeddings/          # embedding providers
│   ├── vectorstore/         # FAISS store
│   ├── retriever/           # semantic retrieval
│   ├── chains/              # RAG & summarization chains
│   └── pipeline/            # document ingestion pipeline
│
└── config/
    └── settings.py
```

---



## 🧱 Architecture Diagram (Single-Document RAG)

```text
┌─────────────────────────────────────────────┐
│                Streamlit UI                 │
│                 (app.py)                    │
│                                             │
│  ┌───────────────┐    ┌──────────────────┐  │
│  │ File Uploader │    │   Chat Interface │  │
│  │ (select only) │    │  (Q&A / Answer)  │  │
│  └───────┬───────┘    └────────┬─────────┘  │
│          │ Process Document                 │
│          ▼                                  │
│  ┌──────────────────────────────────────┐   │
│  │        KnowledgeBaseOrchestrator     │   │
│  │                                      │   │
│  │  - resets previous document          │   │
│  │  - coordinates ingestion & retrieval │   │
│  └───────────────┬──────────────────────┘   │
│                  │                          │
└──────────────────┼──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│        Document Ingestion Pipeline          │
│                                             │
│  ┌─────────────┐  ┌──────────────────────┐  │
│  │ PDF Loader  │→ │ Section Extractor    │  │
│  │             │  │ (heuristic / fallback│  │
│  │             │  │  Full Document)      │  │
│  └─────────────┘  └───────────┬──────────┘  │
│                               │             │
│                       ┌───────▼────────┐    │
│                       │   Chunker      │    │
│                       │ (text chunks)  │    │
│                       └───────┬────────┘    │
└───────────────────────────────┼─────────────┘
                                │
                                ▼
┌────────────────────────────────────────────┐
│           Vector Store (FAISS)             │
│                                            │
│  ┌─────────────────────────────────────┐   │
│  │  Embeddings (HuggingFace)           │   │
│  │  + Chunk Metadata                   │   │
│  └─────────────────────────────────────┘   │
└───────────────────────────────┼────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────┐
│               RAG Chain                     │
│                                             │
│  ┌─────────────┐    ┌────────────────────┐  │
│  │ Retriever   │ →  │ Groq LLM           │  │
│  │ (Top-K)     │    │ (Answer generation │  │
│  │             │    │  with context)     │  │
│  └─────────────┘    └────────────────────┘  │
└─────────────────────────────────────────────┘
```

---

## 🔒 Single-Document Guarantee

* Only **one document** exists in memory at any time
* Selecting a new document:

  * clears vector store
  * clears chat
  * removes previous context
* Processing happens **only** on explicit user action

```text
Select File → (no action)
Click Process → replace old document → ingest → index
```

---


## 📁 Project Structure

```text
.
├── app.py                  # ✅ Single Streamlit entry point
├── orchestrator.py
│
├── core/
│   ├── loaders/
│   ├── processors/
│   ├── embeddings/
│   ├── vectorstore/
│   ├── retriever/
│   ├── chains/
│   └── pipeline/
│
├── ui/
│   ├── components.py
│   ├── chat_interface.py
│   └── helpers.py
│
├── config/
│   └── settings.py
│
├── pyproject.toml
└── README.md
```

---

## 🖥️ Streamlit Entry Point

* **`app.py` (root)** is the **only UI entry**
* It:

  * initializes session state
  * wires core components via `ui/helpers.py`
  * renders sidebar, upload flow, and chat UI

> There is **no `ui/app.py`** — UI logic is modularized, but execution starts from root `app.py`.

---

## 🔄 Document Lifecycle (Important)

1. User selects a document
2. No processing happens automatically
3. User clicks **Process Document**
4. Any previously processed document is:

   * removed from vector store
   * cleared from memory
5. New document is indexed and becomes active context

This ensures **predictable, explicit behavior**.

---

## 🧪 Technology Stack

* Python
* LangChain
* FAISS
* Groq LLM
* HuggingFace Embeddings
* Streamlit
* uv (dependency management)

---

## ▶️ Running the App

```bash
uv sync
uv run streamlit run app.py
```

---

## 🛠 Development Tools

```bash
uv run ruff check . && uv run black . && uv run isort .
```

---

## 📌 Engineering Principles Followed

* Single Streamlit entry point
* Explicit state transitions
* No side effects on file selection
* Clear ownership of responsibilities
* UI ↔ Core isolation
* Production-ready RAG patterns

---

## 📄 License

MIT License — open for reuse and extension.
