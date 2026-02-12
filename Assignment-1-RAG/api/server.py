from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os

# 1. Fix the path so we can import 'core' logic
# (Just like we did in the notebook, but for the server)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.rag import get_qa_chain
import uvicorn

# 2. Initialize the App
app = FastAPI(
    title="FinRAG Analyst API",
    version="1.0",
    description="A Professional RAG Engine for Financial Analysis"
)

# 3. Define the Request Structure
class QueryRequest(BaseModel):
    query: str

# 4. Load the AI Brain (Global Variable)
# We load it once when the server starts so it's fast!
print("🚀 Server starting... Loading RAG Engine...")
rag_chain = get_qa_chain()

@app.get("/")
def health_check():
    """Health check endpoint to ensure server is running."""
    return {"status": "online", "system": "FinRAG v1.0"}

@app.post("/chat")
def chat_endpoint(request: QueryRequest):
    """
    Main endpoint to ask questions.
    Receives JSON: {"query": "your question"}
    Returns JSON: {"answer": "AI response"}
    """
    try:
        # Get the answer from our RAG chain
        response = rag_chain.invoke(request.query)
        
        # Return a clean JSON response
        return {"answer": response}
    
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Run the server on localhost:8000
    uvicorn.run(app, host="0.0.0.0", port=8000)