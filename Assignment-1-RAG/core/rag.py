import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 1. Load Keys
load_dotenv()

def get_qa_chain():
    # 2. Setup Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # 3. Load DB & Retriever
    db = Chroma(persist_directory="vectorstore/db_chroma", embedding_function=embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 3})
    
    # 4. Setup Groq Llama 3
    llm = ChatGroq(
        temperature=0, 
        model_name="llama-3.3-70b-versatile", 
        groq_api_key=os.getenv("GROQ_API_KEY")
    )

    # 5. Define the Professional Prompt
    template = """You are an expert financial analyst. Use the provided context to answer the question.
    Context: {context}
    Question: {question}
    Answer:"""
    
    prompt = ChatPromptTemplate.from_template(template)

    # 6. The "Modern Chain" (LCEL)
    # This replaces 'create_retrieval_chain' and is much more stable
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain

if __name__ == "__main__":
    print("🤖 Testing Modern LCEL RAG Brain...")
    try:
        chain = get_qa_chain()
        response = chain.invoke("What are the financial risks for Apple?")
        print(f"\n✅ AI Answer: {response}")
    except Exception as e:
        print(f"❌ Still getting an error: {e}")