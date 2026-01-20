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

tab1,tab2 = st.tabs(["AI Assistant", "About"],width="stretch")


with tab1:
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
with tab2:
    st.header("About This App")
    st.markdown(
        """
        This application is designed to provide an interactive AI-powered assistant that can answer questions about my professional portfolio. 
        It leverages advanced language models and a retrieval-augmented generation (RAG) approach to deliver accurate and contextually relevant responses.

        ### Features:
        - **AI-Powered Q&A**: Ask questions about my projects, skills, experience, and architecture decisions.
        - **Contextual Responses**: The AI retrieves relevant information from my portfolio to provide informed answers.
        - **Source Documents**: View the source documents used to generate the responses for transparency.

        ### Technologies Used:
        - **Streamlit**: For building the interactive web application.
        - **LangChain**: To create the RAG chain for handling queries.
        - **Chroma**: As the vector store for efficient document retrieval.
        - **Groq LLM**: For generating human-like responses based on retrieved information.

        ### Instructions:
        1. Type your questions in the chat input box.
        2. The AI will process your query and respond based on the portfolio data.
        3. If available, you can view the source documents used for the response.

        Feel free to explore and ask any questions related to my professional journey!
        """
    )