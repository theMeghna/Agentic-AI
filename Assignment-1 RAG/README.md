# 📈 FinRAG-Analyst: Automated Financial Insight Engine

> **Assignment 1: Retrieval-Augmented Generation (RAG) System**
> *Analyzes the Apple 2025 10-K Financial Report using Llama 3 & Vector Search.*

---

## 🚀 Project Overview
**FinRAG-Analyst** (codenamed "Project Nucleus") is an AI-powered financial research tool designed to answer complex queries about SEC 10-K filings. 

Unlike standard LLMs, this system uses a **RAG (Retrieval-Augmented Generation)** architecture to fetch real-time evidence from the document before answering. This ensures **zero hallucination** and provides accurate, citation-backed insights for financial analysts.

### 🌟 Key Features
* **Zero-Hallucination Mode:** Uses `temperature=0` to ensure strict factual accuracy.
* **Source Citations:** Retrieves and references specific chunks from the 10-K PDF.
* **Hybrid Architecture:** Decoupled **FastAPI** backend and **Streamlit** frontend.
* **Vector Search:** Powered by **ChromaDB** and **HuggingFace Embeddings**.
* **Dockerized:** Fully containerized for one-click deployment.

---

## 🛠️ Tech Stack
| Component | Technology | Description |
| :--- | :--- | :--- |
| **LLM** | **Llama 3.3-70b** | High-speed inference via **Groq API** |
| **Orchestration** | **LangChain** | Manages the RAG pipeline & retrieval logic |
| **Database** | **ChromaDB** | Stores vector embeddings of the PDF |
| **Backend** | **FastAPI** | High-performance API server |
| **Frontend** | **Streamlit** | Interactive chat interface |
| **Container** | **Docker** | Ensures consistent deployment environment |

---

## 📂 Project Structure
```text
Assignment-1 RAG/
├── api/                # FastAPI Backend
│   └── server.py       # API Endpoints & Logic
├── core/               # AI Engine (The Brain)
│   ├── ingest.py       # PDF Loader & Vectorization Script
│   └── rag.py          # RAG Retrieval Chain
├── ui/                 # Frontend Interface
│   └── app.py          # Streamlit Chat Dashboard
├── data/               # Raw Data
│   └── apple_2025_10k.pdf  # Financial Report Source
├── vectorstore/        # Pre-computed Vector Database
├── notebooks/          # Lab Experiments
│   └── RAG_Demonstration.ipynb # Step-by-step logic proof
├── Dockerfile          # Container Configuration
├── docker-compose.yml  # Multi-container Setup
└── requirements.txt    # Python Dependencies
⚡ Installation & Setup
1. Clone the Repository
Bash
git clone [https://github.com/theMeghna/Agentic-AI.git](https://github.com/theMeghna/Agentic-AI.git)
cd "Agentic-AI/Assignment-1 RAG"
2. Create a Virtual Environment
Bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
3. Install Dependencies
Bash
pip install -r requirements.txt
4. Configure Environment Keys
Create a .env file in the root directory and add your Groq API Key:

Ini, TOML
GROQ_API_KEY=gsk_your_actual_key_here
🏃‍♂️ How to Run
You can run the system using Docker (Recommended) or Manually.

Option A: Using Docker (One-Click)
Bash
docker-compose up --build
Frontend: http://localhost:8501

Backend API: http://localhost:8000/docs

Option B: Manual Execution
Open two separate terminals:

Terminal 1: Start the Backend API

Bash
python api/server.py
(Wait until you see "Uvicorn running on https://www.google.com/search?q=http://0.0.0.0:8000")

Terminal 2: Start the Frontend UI

Bash
streamlit run ui/app.py
🧪 Testing & Verification
We have included a Jupyter Notebook to verify the RAG logic step-by-step:

Open notebooks/RAG_Demonstration.ipynb

Run all cells to see the Ingestion -> Retrieval -> Generation process in action.

Example Queries
"What are the primary risk factors for Apple in 2025?"

"How much did the company invest in Research and Development?"

"Summarize the legal proceedings mentioned in Item 3."

👥 Team Members
Meghna Sahu - Team Lead & AI Core (Core RAG Logic)

Kusuma - Frontend Developer (Streamlit UI)

Harshit Sangwan - Backend Developer (FastAPI Integration)
