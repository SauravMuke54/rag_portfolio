import streamlit as st
from rag_chain import build_rag_chain

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Saurav Muke | AI Portfolio",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 Chat with My Portfolio")
st.caption("Ask about my projects, skills, experience, and architecture decisions.")

# -------------------------------
# Session State
# -------------------------------
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = build_rag_chain()

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------
# Example Prompts
# -------------------------------
with st.expander("💡 Example questions"):
    st.markdown("""
    - Tell me about your data engineering experience  
    - Which project reduced processing time?  
    - Explain your Airflow + AKS setup  
    - What GenAI work have you done?  
    """)

# -------------------------------
# Display Chat History
# -------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------------
# Chat Input
# -------------------------------
prompt = st.chat_input("Ask me anything about my work...")

if prompt:
    # User message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = st.session_state.qa_chain(
                {"question": prompt}
            )
            answer = result["answer"]

            st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
