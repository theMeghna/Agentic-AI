import streamlit as st
import sys
import os

# --- 1. CHROMA DB FIX FOR STREAMLIT CLOUD ---
# Streamlit Cloud's Linux version has an old SQLite. 
# We force it to use the new 'pysqlite3' we just installed.
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# --- 2. IMPORT YOUR BRAIN ---
from core.rag import get_qa_chain

# --- 3. PAGE CONFIG ---
st.set_page_config(page_title="Project Nucleus", page_icon="🤖")

st.title("🤖 Project Nucleus: FinRAG Analyst")
st.caption("Live Analysis of Apple 2025 10-K Report")

# --- 4. INITIALIZE THE BRAIN (Cached) ---
# We use @st.cache_resource so it doesn't reload the database on every click
@st.cache_resource
def load_brain():
    return get_qa_chain()

try:
    rag_chain = load_brain()
    st.success("✅ Brain Loaded! Ask a question below.")
except Exception as e:
    st.error(f"Error loading RAG Engine: {e}")

# --- 5. CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What are the risks in 2025?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Direct call to the Brain (No API in the middle)
                response = rag_chain.invoke(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {e}")
