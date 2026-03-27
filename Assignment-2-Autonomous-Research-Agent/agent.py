"""
============================================================
  Autonomous Research Agent (Modern LangChain v1+)
  LLM: Ollama (mistral:7b)
  Tools: DuckDuckGo + Wikipedia
============================================================
"""

import sys
import datetime

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_ollama import OllamaLLM
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper

from report_builder import build_report



# ───────────────────────────────────────────────────────────
# 1. LLM (Ollama)
# ───────────────────────────────────────────────────────────
def get_llm(model: str = "Mistral:7b", temperature: float = 0.3):
    return OllamaLLM(
        model=model,
        temperature=temperature,
        num_ctx=4096,
    )


# ───────────────────────────────────────────────────────────
# 2. Tools
# ───────────────────────────────────────────────────────────
search = DuckDuckGoSearchRun()
wiki = WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=4000)


@tool
def web_search(query: str) -> str:
    """Search the web for recent information."""
    return search.run(query)


@tool
def wikipedia_search(query: str) -> str:
    """Get detailed background info from Wikipedia."""
    return wiki.run(query)


def build_tools():
    return [web_search, wikipedia_search]


# ───────────────────────────────────────────────────────────
# 3. Agent (MODERN)
# ───────────────────────────────────────────────────────────
def create_research_agent(model: str = "Mistral:7b"):
    llm = get_llm(model)

    def run_agent(topic: str):
        print("🔍 Step 1: Searching web...")
        search_result = web_search.invoke(topic)

        print("📚 Step 2: Fetching Wikipedia...")
        wiki_result = wikipedia_search.invoke(topic)

        print("🧠 Step 3: Generating report...")

        context = f"""
Web Search Results:
{search_result}

Wikipedia Results:
{wiki_result}
"""

        prompt = f"""
You are an expert research analyst.

Using the following information:
{context}

Generate a structured academic report.

FORMAT:

INTRODUCTION:
(2–3 paragraphs)

KEY_FINDINGS:
1. Detailed explanation
2. Detailed explanation
3. Detailed explanation
4. Detailed explanation
5. Detailed explanation

CHALLENGES:
1. Explanation
2. Explanation
3. Explanation

FUTURE_SCOPE:
1. Future direction
2. Future direction
3. Future direction

CONCLUSION:
(2–3 paragraphs)
"""

        return llm.invoke(prompt)

    return run_agent


# ───────────────────────────────────────────────────────────
# 4. Run Research
# ───────────────────────────────────────────────────────────
def run_research(topic: str, model: str = "Mistral:7b") -> str:
    print(f"\n{'='*60}")
    print("  Research Agent Starting")
    print(f"  Topic  : {topic}")
    print(f"  Model  : {model}")
    print(f"  Time   : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    # Create agent (this is now a function, NOT LangChain agent)
    agent = create_research_agent(model)

    # Call agent directly (NO invoke, NO messages)
    raw_output = agent(topic)

    # Generate report
    report_path = build_report(topic=topic, raw_research=raw_output)

    print(f"\n{'='*60}")
    print(f"  Report saved -> {report_path}")
    print(f"{'='*60}\n")

    return report_path


# ───────────────────────────────────────────────────────────
# 5. Entry Point
# ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    topic = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "AI in Education"
    run_research(topic)