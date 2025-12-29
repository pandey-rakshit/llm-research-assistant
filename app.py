import streamlit as st

from ui.chat_interface import chat_ui
from ui.components import (
    init_session_state,
    render_chat_history,
    render_sidebar,
    save_uploaded_file,
)
from ui.helpers import build_rag_system

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="Research Paper RAG Assistant",
    layout="wide",
)
st.title("📘 Research Paper RAG Assistant")


# -------------------------------------------------
# Init state & core system
# -------------------------------------------------
init_session_state()

if "rag_ready" not in st.session_state:
    orchestrator, rag_chain = build_rag_system()
    st.session_state.orchestrator = orchestrator
    st.session_state.rag_chain = rag_chain
    st.session_state.rag_ready = True

if "selected_file" not in st.session_state:
    st.session_state.selected_file = None

if "is_processing" not in st.session_state:
    st.session_state.is_processing = False


# -------------------------------------------------
# Chat area
# -------------------------------------------------
st.subheader("💬 Chat")
render_chat_history()


# -------------------------------------------------
# Sidebar
# -------------------------------------------------
render_sidebar(st.session_state.orchestrator, st.session_state.document_metadata)


# -------------------------------------------------
# Actual processing (SINGLE SOURCE OF TRUTH)
# -------------------------------------------------
if st.session_state.is_processing and st.session_state.selected_file:

    with st.spinner("Processing and indexing document..."):
        path = save_uploaded_file(st.session_state.selected_file)

        # single-document mode → reset context)
        st.session_state.uploaded_files = None
        st.session_state.document_metadata = None
        st.session_state.orchestrator.store.store = None
        st.session_state.processed_files.clear()
        st.session_state.chat.clear()

        metadata = st.session_state.orchestrator.ingest(path)
        st.session_state.document_metadata = metadata

    st.session_state.processed_files.add(st.session_state.selected_file.name)

    if st.session_state.selected_file.name != st.session_state.uploaded_files:
        st.session_state.uploaded_files = st.session_state.selected_file.name

    
    st.session_state.is_processing = False
    st.success("Document processed successfully")
    st.rerun()



# -------------------------------------------------
# Chat input
# -------------------------------------------------
if st.session_state.processed_files:
    chat_ui(st.session_state.rag_chain)
else:
    st.warning("Upload and process a document to start chatting.")


# -------------------------------------------------
# Upload / Manage Documents (PASSIVE)
# -------------------------------------------------
with st.expander(
    "📄 Upload / Manage Documents",
    expanded=not bool(st.session_state.processed_files)
):
    uploaded_file = st.file_uploader(
        "Upload research paper (PDF)",
        type=["pdf"],
        key="file_uploader",
    )

    if uploaded_file:
        # passive selection only
        st.session_state.selected_file = uploaded_file
        st.info(f"Selected file: **{uploaded_file.name}**")

    # Show process button only when a file is selected
    if st.session_state.selected_file:
        filename = st.session_state.selected_file.name

        if filename not in st.session_state.processed_files:
            if st.button("📄 Process Document", type="primary"):
                st.session_state.is_processing = True
                st.rerun()
        else:
            st.success("Document already processed")