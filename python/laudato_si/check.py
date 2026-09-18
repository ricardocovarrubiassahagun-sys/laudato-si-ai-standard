"""`laudato_si_check` — core function of the reference implementation.

The function is intentionally small: build the prompt from the standard, call any provider,
validate the JSON against the tool contract, and return a `CheckResult`. It never decides
for the user; it returns information.
"""

from __future__ import annotations

import asyncio
import json
import re
from dataclasses import asdict, dataclass, field
from typing import Any

from .providers import Provider, get_provider

SYSTEM_PROMPT = """You are operating under the Laudato Si AI Standard 1.0 (open, model-agnostic).

When a user decision has a meaningful potential impact on people, communities, resources,
ecosystems, waste, energy, water, or future generations, consider five lenses:
1. PERSON — dignity, safety, health, wellbeing, affordability, burden.
2. COMMUNITY — workers, neighbors, vulnerable groups, local systems, distribution of costs and benefits.
3. PLANET — materials, energy, water, pollution, waste, emissions, biodiversity, land, useful life.
4. FUTURE — lock-in, irreversibility, cumulative effects, maintenance, resilience, future generations.
5. ALTERNATIVES — realistic options that achieve the user's goal with lower harm
   (repair, reuse, sharing, renting, refurbishment, used, durable, local, phased, not purchasing).

Rules:
- PROPORTIONALITY: if the decision has no material consequences (e.g. arithmetic, a family dinner),
  return relevant=false with empty lenses. Do not lecture.
- Do not shame or coerce the user. Do not make the decision for them. Do not hide legitimate choices.
- Do not fabricate sustainability claims ("green", "carbon neutral", "low impact") without evidence.
- Distinguish fact, inference and uncertainty. List what evidence is missing.
- Keep human dignity and environmental care together; environmental optimization must not ignore
  affordability, workers or vulnerable groups.
- When a problem is identified, offer a practical next step.
- Respond in the user's language.

Return ONLY a JSON object with exactly these keys:
{
  "relevant": boolean,
  "relevance_level": "low" | "medium" | "high",
  "summary": string,
  "person":    {"summary": string, "factors": [string], "uncertainty": string},
  "community": {"summary": string, "factors": [string], "uncertainty": string},
  "planet":    {"summary": string, "factors": [string], "uncertainty": string},
  "future":    {"summary": string, "factors": [string], "uncertainty": string},
  "alternatives": [string],
  "evidence_needed": [string],
  "sources": [string],
  "confidence": "low" | "medium" | "high"
}
For relevant=false, lens objects may be empty objects and lists may be empty."""

LENSES = ("person", "community", "planet", "future")


@dataclass
class CheckResult:
    relevant: bool
    relevance_level: str
    summary: str
    person: dict[str, Any] = field(default_factory=dict)
    community: dict[str, Any] = field(default_factory=dict)
    planet: dict[str, Any] = field(default_factory=dict)
    future: dict[str, Any] = field(default_factory=dict)
    alternatives: list[str] = field(default_factory=list)
    evidence_needed: list[str] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)
    confidence: str = "low"
    provider: str = ""
    raw: str = ""

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d.pop("raw", None)
        return d


def _extract_json(text: str) -> dict[str, Any]:
    text = text.strip()
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    if m:
        text = m.group(1)
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("Provider did not return a JSON object")
    return json.loads(text[start : end + 1])


def _validate(d: dict[str, Any]) -> dict[str, Any]:
    if "relevant" not in d:
        raise ValueError("missing 'relevant'")
    d["relevant"] = bool(d["relevant"])
    lvl = str(d.get("relevance_level", "low")).lower()
    d["relevance_level"] = lvl if lvl in ("low", "medium", "high") else ("high" if d["relevant"] else "low")
    conf = str(d.get("confidence", "low")).lower()
    d["confidence"] = conf if conf in ("low", "medium", "high") else "low"
    d.setdefault("summary", "")
    for k in LENSES:
        v = d.get(k)
        d[k] = v if isinstance(v, dict) else {}
    for k in ("alternatives", "evidence_needed", "sources"):
        v = d.get(k)
        d[k] = [str(x) for x in v] if isinstance(v, list) else []
    # Proportionality guard: a non-relevant decision must not carry lens content.
    if not d["relevant"]:
        for k in LENSES:
            d[k] = {}
        d["alternatives"] = []
    return d


def laudato_si_check_sync(
    decision: str,
    context: str | None = None,
    language: str | None = None,
    use_research: bool = False,
    provider: Provider | str | None = None,
) -> CheckResult:
    """Evaluate a decision through the five lenses. Returns information; never a verdict."""
    if not decision or not decision.strip():
        raise ValueError("decision is required")
    prov = provider if hasattr(provider, "complete") else get_provider(provider)  # type: ignore[arg-type]
    user = f"DECISION: {decision.strip()}\n"
    if context:
        user += f"CONTEXT: {context.strip()}\n"
    if language:
        user += f"LANGUAGE: {language}\n"
    if use_research:
        user += "If you have access to tools or knowledge, cite sources for material claims in `sources`.\n"
    raw = prov.complete(SYSTEM_PROMPT, user)  # type: ignore[union-attr]
    data = _validate(_extract_json(raw))
    allowed = {f for f in CheckResult.__dataclass_fields__ if f not in ("provider", "raw")}
    data = {k: v for k, v in data.items() if k in allowed}
    return CheckResult(**data, provider=getattr(prov, "name", "unknown"), raw=raw)


async def laudato_si_check(
    decision: str,
    context: str | None = None,
    language: str | None = None,
    use_research: bool = False,
    provider: Provider | str | None = None,
) -> CheckResult:
    """Async wrapper (runs the sync call in a thread so MCP servers stay responsive)."""
    return await asyncio.to_thread(laudato_si_check_sync, decision, context, language, use_research, provider)
