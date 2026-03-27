"""
============================================================
  Autonomous Research Agent
  LangChain + Ollama (Mistral:7b)
  Tools: DuckDuckGo Web Search + Wikipedia
============================================================
"""

import sys
import datetime
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
from langchain_community.llms import Ollama
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.callbacks import StdOutCallbackHandler
from report_builder import build_report


# ───────────────────────────────────────────────────────────
# 1.  LLM  (Ollama – Mistral 7B running locally)
# ───────────────────────────────────────────────────────────
def get_llm(model: str = "mistral:7b", temperature: float = 0.3) -> Ollama:
    """Return an Ollama-backed LLM instance."""
    return Ollama(
        model=model,
        temperature=temperature,
        num_ctx=4096,          # wider context for long research
    )


# ───────────────────────────────────────────────────────────
# 2.  Tools
# ───────────────────────────────────────────────────────────
def build_tools() -> list:
    """Construct the tool-list the agent can use."""

    # Tool 1 – Web Search (DuckDuckGo, no API key required)
    search = DuckDuckGoSearchRun()
    web_search_tool = Tool(
        name="WebSearch",
        func=search.run,
        description=(
            "Searches the web using DuckDuckGo. "
            "Use this to find recent news, statistics, and articles. "
            "Input should be a concise search query string."
        ),
    )

    # Tool 2 – Wikipedia Knowledge Base
    wiki = WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=4000)
    wikipedia_tool = Tool(
        name="Wikipedia",
        func=wiki.run,
        description=(
            "Looks up detailed background information on Wikipedia. "
            "Use this for definitions, history, and established facts. "
            "Input should be a topic name or concept."
        ),
    )

    return [web_search_tool, wikipedia_tool]


# ───────────────────────────────────────────────────────────
# 3.  ReAct Prompt Template
# ───────────────────────────────────────────────────────────
REACT_PROMPT = PromptTemplate.from_template(
    """You are an expert research analyst. Your task is to thoroughly research the given
topic and collect enough information to write a comprehensive, structured academic report.

You have access to the following tools:
{tools}

Use the following format STRICTLY:

Question: the input question you must answer
Thought: think step-by-step about what information you need
Action: the action to take, must be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (repeat Thought/Action/Action Input/Observation up to 8 times)
Thought: I now have enough information to compile a full research report.
Final Answer: A comprehensive research summary with ALL of the following sections:

INTRODUCTION: [2-3 paragraphs introducing the topic, its relevance and scope]

KEY_FINDINGS:
1. [Finding 1 – detailed explanation with statistics or examples]
2. [Finding 2 – detailed explanation with statistics or examples]
3. [Finding 3 – detailed explanation with statistics or examples]
4. [Finding 4 – detailed explanation with statistics or examples]
5. [Finding 5 – detailed explanation with statistics or examples]

CHALLENGES:
1. [Challenge 1 – explanation and impact]
2. [Challenge 2 – explanation and impact]
3. [Challenge 3 – explanation and impact]

FUTURE_SCOPE:
1. [Future direction 1 – what it means for the field]
2. [Future direction 2 – what it means for the field]
3. [Future direction 3 – what it means for the field]

CONCLUSION: [2-3 paragraphs summarising insights and significance]

Begin!

Question: Research the topic: {input}
Thought: {agent_scratchpad}"""
)


# ───────────────────────────────────────────────────────────
# 4.  Agent factory
# ───────────────────────────────────────────────────────────
def create_research_agent(model: str = "mistral:7b") -> AgentExecutor:
    """Build and return the ReAct AgentExecutor."""
    llm   = get_llm(model)
    tools = build_tools()

    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=REACT_PROMPT,
    )

    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=10,
        handle_parsing_errors=True,
        callbacks=[StdOutCallbackHandler()],
        return_intermediate_steps=True,
    )
    return executor


# ───────────────────────────────────────────────────────────
# 5.  Run research + generate report
# ───────────────────────────────────────────────────────────
def run_research(topic: str, model: str = "mistral:7b") -> str:
    """
    Run the full research pipeline for a given topic.
    Returns the path to the generated .txt report file.
    """
    print(f"\n{'='*60}")
    print(f"  Research Agent Starting")
    print(f"  Topic  : {topic}")
    print(f"  Model  : {model}")
    print(f"  Time   : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    agent_executor = create_research_agent(model)
    result         = agent_executor.invoke({"input": topic})
    raw_output     = result.get("output", "")

    report_path = build_report(topic=topic, raw_research=raw_output)

    print(f"\n{'='*60}")
    print(f"  Report saved -> {report_path}")
    print(f"{'='*60}\n")

    return report_path


# ───────────────────────────────────────────────────────────
# 6.  Entry-point
# ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    topic = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "AI in Education"
    run_research(topic)
