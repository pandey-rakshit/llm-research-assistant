import streamlit as st


def chat_ui(rag_chain):
    query = st.chat_input("Ask a question")

    if not query:
        return

    # User message (immediate render)
    st.session_state.chat.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    # Assistant response
    with st.chat_message("assistant"):
        answer, sources = rag_chain.run(query)
        st.markdown(answer)

        if sources:
            with st.expander("📚 Sources"):
                for src in sources:
                    st.markdown(f"- {src}")

    st.session_state.chat.append({"role": "assistant", "content": answer})
