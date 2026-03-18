import os
import g4f
from dotenv import load_dotenv
from g4f.client import Client as G4FClient

load_dotenv(override=True)

# ── Provider registry ─────────────────────────────────────────────────────────
PROVIDERS = {
    "chatgpt": {
        "label":    "ChatGPT (GPT-4)",
        "model":    "gpt-4",
        "best_for": "research",
        "tagline":  "Best for research, writing & general knowledge",
        "icon":     "🟢",
    },
    "claude": {
        "label":    "Claude (Sonnet)",
        "model":    "claude-sonnet-4-5-20250929",
        "best_for": "coding",
        "tagline":  "Best for coding, debugging & technical tasks",
        "icon":     "🟡",
    },
    "gemini": {
        "label":    "Gemini 2.5 Flash",
        "model":    "gemini-2.5-flash",
        "best_for": "mathematics",
        "tagline":  "Best for mathematics, logic & data analysis",
        "icon":     "🔵",
    },
}

DEFAULT_PROVIDER = "chatgpt"

# ── Keyword hints used by main.py for smart suggestions ──────────────────────
RESEARCH_KEYWORDS  = {"research", "study", "history", "explain", "summarize",
                      "what is", "who is", "why does", "article", "essay",
                      "write", "news", "fact", "source", "report"}
CODING_KEYWORDS    = {"code", "bug", "error", "debug", "function", "class",
                      "script", "program", "python", "javascript", "html",
                      "css", "sql", "api", "algorithm", "implement", "fix",
                      "refactor", "test", "compile", "syntax", "lambda"}
MATH_KEYWORDS      = {"math", "maths", "calculate", "solve", "equation",
                      "integral", "derivative", "algebra", "geometry",
                      "statistics", "probability", "matrix", "formula",
                      "proof", "theorem", "calculus", "arithmetic", "compute"}


def detect_suggested_provider(text: str) -> str | None:
    """Return the recommended provider name based on query keywords, or None."""
    lower = text.lower()

    def hits(kw_set):
        return any(kw in lower for kw in kw_set)

    if hits(CODING_KEYWORDS):
        return "claude"
    if hits(MATH_KEYWORDS):
        return "gemini"
    if hits(RESEARCH_KEYWORDS):
        return "chatgpt"
    return None


# ── Public ask function ───────────────────────────────────────────────────────

def ask_ai(question: str, provider: str = DEFAULT_PROVIDER) -> str:
    """Route question to the requested provider and return the reply."""
    dispatch = {
        "chatgpt": _ask_chatgpt,
        "claude":  _ask_claude,
        "gemini":  _ask_gemini,
    }
    fn = dispatch.get(provider)
    if fn is None:
        return (f"Error: Unknown provider '{provider}'. "
                f"Available: {', '.join(dispatch)}")
    return fn(question)


# ── Provider implementations ──────────────────────────────────────────────────

def _ask_chatgpt(question: str) -> str:
    client = G4FClient()
    try:
        response = client.chat.completions.create(
            model    = "gpt-4",
            messages = [{"role": "user", "content": question}],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: ChatGPT connection failed — {e}"


def _ask_claude(question: str) -> str:
    client = G4FClient()
    try:
        response = client.chat.completions.create(
            model    = "claude-sonnet-4-5-20250929",
            provider = g4f.Provider.LMArena,
            messages = [{"role": "user", "content": question}],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: Claude connection failed — {e}"


def _ask_gemini(question: str) -> str:
    client = G4FClient()
    try:
        response = client.chat.completions.create(
            model    = "gemini-2.5-flash",
            provider = g4f.Provider.LMArena,
            messages = [{"role": "user", "content": question}],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: Gemini connection failed — {e}"