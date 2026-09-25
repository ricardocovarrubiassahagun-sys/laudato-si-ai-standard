"""Provider adapters. The standard is model-agnostic: any chat model that can return JSON works.

Selection (env var LAUDATO_PROVIDER, or `provider=` argument):
  - "anthropic"          → ANTHROPIC_API_KEY, model LAUDATO_MODEL (default claude-sonnet-4-5)
  - "openai"             → OPENAI_API_KEY, model LAUDATO_MODEL (default gpt-4o-mini)
  - "openai-compatible"  → OPENAI_BASE_URL + OPENAI_API_KEY (Mistral, Together, Groq, vLLM, Ollama…)
  - "mock"               → deterministic offline heuristic; used by tests and by `--offline`

Each adapter exposes `complete(system: str, user: str) -> str` (raw text; the caller parses JSON).
"""

from __future__ import annotations

import json
import os
import re
from typing import Protocol


class Provider(Protocol):
    name: str

    def complete(self, system: str, user: str) -> str: ...


class AnthropicProvider:
    name = "anthropic"

    def __init__(self, model: str | None = None) -> None:
        import anthropic  # lazy import

        self.client = anthropic.Anthropic()
        self.model = model or os.getenv("LAUDATO_MODEL", "claude-sonnet-4-5")

    def complete(self, system: str, user: str) -> str:
        msg = self.client.messages.create(
            model=self.model,
            max_tokens=int(os.getenv("LAUDATO_MAX_TOKENS", "4000")),
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return "".join(getattr(b, "text", "") for b in msg.content)


class OpenAIProvider:
    name = "openai"

    def __init__(self, model: str | None = None, base_url: str | None = None) -> None:
        from openai import OpenAI  # lazy import

        kwargs = {}
        base_url = base_url or os.getenv("OPENAI_BASE_URL")
        if base_url:
            kwargs["base_url"] = base_url
            self.name = "openai-compatible"
        self.client = OpenAI(**kwargs)
        self.model = model or os.getenv("LAUDATO_MODEL", "gpt-4o-mini")

    def complete(self, system: str, user: str) -> str:
        r = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            temperature=0.2,
        )
        return r.choices[0].message.content or ""


# Keywords that make a decision "materially relevant" under §1 of the standard.
_HIGH = re.compile(
    r"\b(\d{3,}|thousand|million|factory|plant|homes?|housing|infrastructure|land|acres?|hectares?|"
    r"procure|procurement|fleet|data ?center|mine|mining|packaging|disposable|demolish|demolition|"
    r"replace all|expand|construction|pipeline|water|energy|waste|emissions?)\b",
    re.IGNORECASE,
)
_MEDIUM = re.compile(
    r"\b(buy|purchase|replace|upgrade|laptop|phone|car|appliance|washing machine|fridge|"
    r"repair|renovat|travel|flight|commute|diet)\b",
    re.IGNORECASE,
)


class MockProvider:
    """Deterministic, offline stand-in that follows the standard's proportionality rule.

    It is NOT a model. It exists so the package can be installed and tested in minutes
    without API keys, and so CI stays reproducible.
    """

    name = "mock"

    def complete(self, system: str, user: str) -> str:
        decision = user.split("DECISION:", 1)[-1].split("\n", 1)[0].strip() if "DECISION:" in user else user
        if _HIGH.search(decision):
            level, relevant = "high", True
        elif _MEDIUM.search(decision):
            level, relevant = "medium", True
        else:
            level, relevant = "low", False
        if not relevant:
            return json.dumps(
                {
                    "relevant": False,
                    "relevance_level": "low",
                    "summary": "No material environmental or social consequences identified; answer normally.",
                    "person": {}, "community": {}, "planet": {}, "future": {},
                    "alternatives": [], "evidence_needed": [], "sources": [],
                    "confidence": "high",
                }
            )
        depth = "deep" if level == "high" else "brief"
        return json.dumps(
            {
                "relevant": True,
                "relevance_level": level,
                "summary": f"Decision has {level} relevance; {depth} analysis across the five lenses.",
                "person": {"summary": "Consider cost, safety and burden for the person deciding.", "factors": ["affordability", "safety"], "uncertainty": "unknown budget"},
                "community": {"summary": "Consider workers, neighbors and vulnerable groups.", "factors": ["jobs", "local services"], "uncertainty": "location not specified"},
                "planet": {"summary": "Consider materials, energy, water, waste and useful life.", "factors": ["materials", "energy", "waste"], "uncertainty": "no lifecycle data provided"},
                "future": {"summary": "Consider lock-in, maintenance and effects at 5/10/25 years.", "factors": ["lock-in", "maintenance"], "uncertainty": "time horizon unknown"},
                "alternatives": ["repair or extend useful life", "phased replacement", "reuse / refurbished option", "do not proceed yet; gather evidence"],
                "evidence_needed": ["current condition / remaining useful life", "cost comparison", "lifecycle or supplier data"],
                "sources": [],
                "confidence": "low",
                "note": "Generated by the offline mock provider — not a model output.",
            }
        )


def get_provider(name: str | None = None) -> Provider:
    name = (name or os.getenv("LAUDATO_PROVIDER") or "").lower()
    if name in ("", "auto"):
        if os.getenv("ANTHROPIC_API_KEY"):
            name = "anthropic"
        elif os.getenv("OPENAI_API_KEY"):
            name = "openai"
        else:
            name = "mock"
    if name == "anthropic":
        return AnthropicProvider()
    if name in ("openai", "openai-compatible"):
        return OpenAIProvider()
    if name == "mock":
        return MockProvider()
    raise ValueError(f"Unknown provider: {name}")
