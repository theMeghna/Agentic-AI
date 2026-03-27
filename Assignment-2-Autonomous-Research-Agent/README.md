# Autonomous Research Agent
### Assignment 2 — LangChain + Ollama (Mistral:7b)

An AI agent that automatically researches any topic using **web search** and **Wikipedia**, then generates a fully structured academic-style report — all running **100% locally** with Ollama.

---

## Architecture

```
User Input (topic)
       │
       ▼
┌─────────────────────┐
│   ReAct Agent       │  ← LangChain AgentExecutor
│   (Mistral:7b via   │
│    Ollama)          │
└─────────┬───────────┘
          │  uses
    ┌─────┴──────┐
    │            │
    ▼            ▼
WebSearch    Wikipedia
(DuckDuckGo) (langchain-
             community)
    │            │
    └─────┬──────┘
          │  collects
          ▼
   Raw Research Text
          │
          ▼
┌─────────────────────┐
│   report_builder.py │  ← Parses raw agent output &
│                     │    formats into structured report
└─────────────────────┘
          │
          ▼
  Structured .txt Report
  (Cover Page + 5 Sections)
  saved to sample_outputs/
```

---

## Requirements

| Requirement | Detail |
|-------------|--------|
| Python | 3.10 or higher |
| Ollama | Running locally (`http://localhost:11434`) |
| Model | `mistral:7b` |
| Internet | Needed for DuckDuckGo + Wikipedia |

---

## Setup & Run

### 1. Install Ollama & pull model
```bash
# Install Ollama from https://ollama.com
ollama pull mistral:7b
ollama serve           # keep this terminal open
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the agent
```bash
# Default topic: "AI in Education"
python agent.py

# Custom topic
python agent.py Impact of AI in Healthcare
python agent.py Climate Change and Renewable Energy
```

---

## Output Format

Every run produces a timestamped `.txt` file inside `sample_outputs/`:

```
=================================================================
        AUTONOMOUS RESEARCH AGENT — GENERATED REPORT
=================================================================
  TITLE   : AI IN EDUCATION
  DATE    : March 27, 2026
  MODEL   : Ollama / Mistral:7b
  TOOLS   : DuckDuckGo Web Search | Wikipedia
  AGENT   : LangChain ReAct Agent
=================================================================

  SECTION 1 — INTRODUCTION
  SECTION 2 — KEY FINDINGS       (5 numbered findings)
  SECTION 3 — CHALLENGES         (3 numbered challenges)
  SECTION 4 — FUTURE SCOPE       (3 numbered directions)
  SECTION 5 — CONCLUSION
=================================================================
```

---

## Project Structure

```
research-agent/
├── agent.py              # ReAct agent + tools + entry-point
├── report_builder.py     # Parses raw agent output → formatted report
├── requirements.txt      # Python dependencies
├── README.md
└── sample_outputs/
    ├── report_ai_in_education_<timestamp>.txt
    └── report_impact_of_ai_in_healthcare_<timestamp>.txt
```

---

## File Descriptions

| File | Role |
|------|------|
| `agent.py` | Defines the LLM, tools, ReAct prompt, and AgentExecutor. Entry-point for running the agent. |
| `report_builder.py` | Receives raw agent output, parses sections using regex, formats a professional cover page + 5-section report, and saves it as a `.txt` file. |
| `requirements.txt` | All Python dependencies needed to run the project. |

---

## Tools Used

| Tool | Purpose | API Key? |
|------|---------|----------|
| `DuckDuckGoSearchRun` | Live web search | ❌ None needed |
| `WikipediaAPIWrapper` | Background knowledge | ❌ None needed |
| `Ollama (Mistral:7b)` | LLM reasoning (runs locally) | ❌ Local only |

---

## Sample Topics Tested
- **AI in Education** *(primary topic)*
- **Impact of AI in Healthcare**

---

## License
MIT
