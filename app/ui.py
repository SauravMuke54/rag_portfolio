import streamlit as st
from rag_chain import build_rag_chain

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Saurav Muke | AI Portfolio",
    page_icon="🤖",
    layout="wide",
)

# -------------------------------
# App Header
# -------------------------------
st.title("🤖 Saurav's Portfolio Manager")
st.caption("Ask about my projects, skills, experience, and architecture decisions.")

st.sidebar.markdown(
    """
    <div style="
        background: linear-gradient(135deg, #6a11cb, #2575fc);
        padding: 15px;
        border-radius: 10px;
        color: #ffffff;
        font-family: Arial, sans-serif;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    ">
        <h2 style="text-align: center;">✨ About This App ✨</h2>
        <p>🤖 This app lets you chat with my portfolio using AI.</p>
        <h4>📋 Instructions:</h4>
        <ul>
            <li>💬 Type your questions about my projects, skills, or experience.</li>
            <li>⚡ The AI will respond based on the portfolio data.</li>
        </ul>
        <p>⚠️ <strong>Note:</strong> If the information is unavailable, the AI will let you know.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------
# Initialize Session State
# -------------------------------
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = build_rag_chain()

if "messages" not in st.session_state:
    st.session_state.messages = []

st.chat_input("Type your question here...", key="user_input")

if st.session_state.user_input:
    user_message = st.session_state.user_input
    st.session_state.messages.append({"role": "user", "content": user_message})

    with st.spinner("AI is thinking..."):
        result = st.session_state.qa_chain.invoke({"question": user_message})
        ai_message = result["answer"]
        st.session_state.messages.append({"role": "assistant", "content": ai_message})
        source_docs = result.get("source_documents", [])
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.chat_message("user").markdown(message["content"])
        else:
            st.chat_message("assistant").markdown(message["content"])
    if source_docs:
        with st.expander("Source Documents 📚"):
            for i, doc in enumerate(source_docs):
                st.markdown(f"**Document {i+1}:**")
                st.markdown(f"- **Title:** {doc.metadata.get('title', 'N/A')}")
                st.markdown(f"- **Type:** {doc.metadata.get('type', 'N/A')}")
                st.markdown(f"- **Source:** {doc.metadata.get('source', 'N/A')}")
                content_preview = doc.page_content[:500] + ("..." if len(doc.page_content) > 500 else "")
                st.markdown(f"- **Content Preview:** {content_preview}")
                st.markdown("---")
