"""
report_builder.py
─────────────────
Parses the agent's raw research output and formats it into a
professional, structured text report with a cover page.
"""

import os
import re
import datetime


# ───────────────────────────────────────────────────────────
# helpers
# ───────────────────────────────────────────────────────────
def _extract_section(text: str, label: str, next_label: str = None) -> str:
    """Pull a named section out of the raw research text."""
    pattern = (
        rf"{re.escape(label)}[:\s]*(.*?)(?={re.escape(next_label)}|$)"
        if next_label
        else rf"{re.escape(label)}[:\s]*(.*)"
    )
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""


def _extract_numbered_list(text: str, label: str, next_label: str = None) -> list[str]:
    """Extract a numbered list section and return items as a Python list."""
    raw = _extract_section(text, label, next_label)
    items = re.findall(r"\d+\.\s+(.+?)(?=\d+\.|$)", raw, re.DOTALL)
    return [item.strip() for item in items if item.strip()] if items else [raw.strip()]


def _safe_filename(topic: str) -> str:
    return re.sub(r"[^\w\s-]", "", topic).strip().replace(" ", "_").lower()


# ───────────────────────────────────────────────────────────
# main builder
# ───────────────────────────────────────────────────────────
def build_report(topic: str, raw_research: str, output_dir: str = "sample_outputs") -> str:
    """
    Parse raw_research (agent Final Answer) and write a
    formatted .txt report. Returns the file path.
    """
    os.makedirs(output_dir, exist_ok=True)
    now       = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    date_str  = now.strftime("%B %d, %Y")
    filename  = f"{output_dir}/report_{_safe_filename(topic)}_{timestamp}.txt"

    # ── Parse sections from raw agent output ───────────────
    introduction  = _extract_section(raw_research,   "INTRODUCTION",  "KEY_FINDINGS")
    findings_list = _extract_numbered_list(raw_research, "KEY_FINDINGS",  "CHALLENGES")
    challenges_list = _extract_numbered_list(raw_research, "CHALLENGES", "FUTURE_SCOPE")
    future_list   = _extract_numbered_list(raw_research, "FUTURE_SCOPE", "CONCLUSION")
    conclusion    = _extract_section(raw_research,   "CONCLUSION")

    # Fall-back: if parsing missed sections, use the full text
    if not introduction:
        introduction = raw_research[:1200] + "\n[... see full agent output ...]"

    # ── Compose the formatted report ───────────────────────
    sep_thick = "=" * 65
    sep_thin  = "-" * 65

    lines = [
        sep_thick,
        "",
        "        AUTONOMOUS RESEARCH AGENT — GENERATED REPORT",
        "",
        sep_thick,
        "",
        f"  TITLE   : {topic.upper()}",
        f"  DATE    : {date_str}",
        f"  MODEL   : Ollama / Mistral:7b",
        f"  TOOLS   : DuckDuckGo Web Search | Wikipedia",
        f"  AGENT   : LangChain ReAct Agent",
        "",
        sep_thick,
        "",
        "",
        sep_thin,
        "  SECTION 1 — INTRODUCTION",
        sep_thin,
        "",
        _wrap(introduction, width=70),
        "",
        "",
        sep_thin,
        "  SECTION 2 — KEY FINDINGS",
        sep_thin,
        "",
    ]

    for i, finding in enumerate(findings_list, 1):
        lines.append(f"  [{i}] {_wrap(finding, width=66, subsequent_indent='      ')}")
        lines.append("")

    lines += [
        "",
        sep_thin,
        "  SECTION 3 — CHALLENGES",
        sep_thin,
        "",
    ]

    for i, challenge in enumerate(challenges_list, 1):
        lines.append(f"  [{i}] {_wrap(challenge, width=66, subsequent_indent='      ')}")
        lines.append("")

    lines += [
        "",
        sep_thin,
        "  SECTION 4 — FUTURE SCOPE",
        sep_thin,
        "",
    ]

    for i, future in enumerate(future_list, 1):
        lines.append(f"  [{i}] {_wrap(future, width=66, subsequent_indent='      ')}")
        lines.append("")

    lines += [
        "",
        sep_thin,
        "  SECTION 5 — CONCLUSION",
        sep_thin,
        "",
        _wrap(conclusion or "See introduction for summary.", width=70),
        "",
        "",
        sep_thick,
        "  END OF REPORT",
        sep_thick,
        "",
    ]

    report_text = "\n".join(lines)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(report_text)

    # Also print to console
    print(report_text)

    return filename


# ───────────────────────────────────────────────────────────
# word-wrap helper
# ───────────────────────────────────────────────────────────
def _wrap(text: str, width: int = 70, subsequent_indent: str = "") -> str:
    """Simple word-wrap preserving existing newlines."""
    import textwrap
    paragraphs = text.split("\n")
    wrapped = []
    for para in paragraphs:
        if para.strip() == "":
            wrapped.append("")
        else:
            wrapped.append(
                textwrap.fill(
                    para.strip(),
                    width=width,
                    subsequent_indent=subsequent_indent,
                )
            )
    return "\n".join(wrapped)
