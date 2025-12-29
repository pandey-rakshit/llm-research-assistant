import tempfile

import streamlit as st


# -------------------------------------------------
# File handling
# -------------------------------------------------
def save_uploaded_file(uploaded_file) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        return tmp.name


# -------------------------------------------------
# Session state
# -------------------------------------------------
def init_session_state():
    if "chat" not in st.session_state:
        st.session_state.chat = []

    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []

    if "processed_files" not in st.session_state:
        st.session_state.processed_files = set()

    if "document_metadata" not in st.session_state:
        st.session_state.document_metadata = None


# -------------------------------------------------
# Chat history
# -------------------------------------------------
def render_chat_history():
    for msg in st.session_state.chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


# -------------------------------------------------
# Sidebar (actions only)
# -------------------------------------------------
def render_sidebar(orchestrator, metadata=None):
    with st.sidebar:
        st.header("📘 Research RAG Assistant")

        with st.expander("ℹ️ How to use"):
            st.markdown(
                """
            1. Upload PDF
            2. Click Process Document
            3. Ask questions
            """
            )

        st.divider()

        st.subheader("📄 Uploaded Documents")

        if filename := st.session_state.uploaded_files:
            if st.button(f"{filename}", key=f"del_{filename}", icon="🗑️"):
                orchestrator.store.store = None
                st.session_state.uploaded_files = None
                st.session_state.processed_files.clear()
                st.session_state.chat.clear()
                st.session_state.document_metadata = None
                st.rerun()

        st.divider()

        if metadata:
            with st.expander("📄 Paper Metadata", expanded=True):
                if metadata.get("title"):
                    st.markdown(f"**Title:** {metadata['title']}")

                if metadata.get("author"):
                    st.markdown("**Authors:**")
                    authors = metadata.get("author")
                    authors = authors.split(";")
                    for a in authors:
                        st.markdown(f"- {a}")

                if metadata.get("year"):
                    st.markdown(f"**Year:** {metadata['year']}")

                if metadata.get("venue"):
                    st.markdown(f"**Venue:** {metadata['venue']}")

                if metadata.get("doi"):
                    st.markdown(f"**URL:** {metadata['doi']}")

                if metadata.get("total_pages"):
                    st.markdown(f"**Total Pages:** {metadata['total_pages']}")

                if metadata.get("source"):
                    st.markdown(f"**source:** {metadata['source']}")

                if metadata.get("sections"):
                    st.markdown("**Sections:**")
                    for s in metadata["sections"]:
                        st.markdown(f"- {s}")

        st.divider()
