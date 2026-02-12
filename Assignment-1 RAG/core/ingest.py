import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def create_vector_db():
    # 1. Path to your PDF
    pdf_path = "data/apple_2025_10k.pdf"
    # 2. Where to save the 'Brain'
    persist_directory = "vectorstore/db_chroma"
    
    print(f"📄 Loading {pdf_path}...")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # 3. Text Chunking Strategy
    # We use 1000 char chunks with a 200 char overlap to keep context intact
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200
    )
    texts = text_splitter.split_documents(documents)
    print(f"✂️ Split into {len(texts)} chunks.")

    # 4. Embedding Model (Local & Free)
    print("🧠 Generating embeddings (this may take a minute)...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    # 5. Save to Vector Database (ChromaDB)
    vector_db = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    
    print(f"✅ Success! Vector database saved at {persist_directory}")

if __name__ == "__main__":
    create_vector_db()