import streamlit as st
import requests
import json

# 1. Page Configuration (The "Look and Feel")
st.set_page_config(
    page_title="FinRAG Analyst",
    page_icon="📈",
    layout="wide"
)

# 2. Sidebar for Context
with st.sidebar:
    st.title("🤖 Project Nucleus")
    st.markdown("### FinRAG Analyst")
    st.info(
        "This tool uses **RAG (Retrieval-Augmented Generation)** "
        "to analyze the Apple 2025 10-K Financial Report."
    )
    st.markdown("---")
    st.markdown("**Powered By:**")
    st.text("• Llama 3.3 (Groq)")
    st.text("• ChromaDB")
    st.text("• FastAPI")

# 3. Main Chat Interface
st.title("📈 Financial Report Analyst")
st.caption("Ask questions about risks, revenue, and R&D expenses.")

# Initialize chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Input Box
if prompt := st.chat_input("Ask a question about Apple's 10-K..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5. Call the API (The "Handshake")
    with st.chat_message("assistant"):
        with st.spinner("Analyzing financial data..."):
            try:
                # Send request to your FastAPI server
                api_url = "http://localhost:8000/chat"
                payload = {"query": prompt}
                
                response = requests.post(api_url, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    ai_answer = data.get("answer", "Error: No answer received.")
                    
                    st.markdown(ai_answer)
                    
                    # Save AI answer to history
                    st.session_state.messages.append({"role": "assistant", "content": ai_answer})
                else:
                    st.error(f"Server Error: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to the API Server.")
                st.warning("Did you forget to run `python api/server.py` in a separate terminal?")