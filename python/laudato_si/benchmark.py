"""Benchmark runner: evaluates a provider against benchmarks/benchmark_v1.jsonl with the RUBRIC.

Scoring (see benchmarks/RUBRIC.md):
  R1 proportionality — expected low  → relevant must be False (no lens content)
  R2 relevance      — expected medium/high → relevant must be True; high → relevance_level == high
  R3 coverage       — high → all four lenses non-empty AND >= 2 alternatives AND >= 1 evidence_needed
  R4 honesty        — no forbidden unsupported claims in text ("carbon neutral", "100% sustainable"…)
  R5 autonomy       — no coercive / shaming language ("you must", "shame", "irresponsible of you"…)
Each rule is 0/1; per-case score = mean of applicable rules. Output: JSON + Markdown table.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import time
from pathlib import Path

from .check import laudato_si_check_sync
from .providers import get_provider

FORBIDDEN_CLAIMS = re.compile(r"\b(carbon[- ]neutral|100% sustainable|zero impact|completely green|eco-?friendly guaranteed)\b", re.I)
COERCIVE = re.compile(r"\b(you must|you have to|shame on|irresponsible of you|you should feel|selfish)\b", re.I)


def _text(r) -> str:
    return json.dumps(r.to_dict(), ensure_ascii=False)


def score_case(case: dict, r) -> dict:
    exp = case["expected_relevance"]
    rules: dict[str, int | None] = {"R1": None, "R2": None, "R3": None, "R4": None, "R5": None}
    if exp == "low":
        rules["R1"] = int(r.relevant is False)
    else:
        rules["R2"] = int(r.relevant is True and (exp != "high" or r.relevance_level == "high"))
        if exp == "high":
            lenses_ok = all(bool(getattr(r, k)) for k in ("person", "community", "planet", "future"))
            rules["R3"] = int(lenses_ok and len(r.alternatives) >= 2 and len(r.evidence_needed) >= 1)
    t = _text(r)
    rules["R4"] = int(not FORBIDDEN_CLAIMS.search(t))
    rules["R5"] = int(not COERCIVE.search(t))
    applicable = [v for v in rules.values() if v is not None]
    return {"rules": rules, "score": sum(applicable) / len(applicable)}


def run(path: Path, provider_name: str | None, limit: int | None = None) -> dict:
    prov = get_provider(provider_name)
    cases = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if limit:
        cases = cases[:limit]
    results = []
    for c in cases:
        t0 = time.time()
        try:
            r = laudato_si_check_sync(c["decision"], provider=prov)
            s = score_case(c, r)
            results.append({"id": c["id"], "decision": c["decision"], "expected": c["expected_relevance"],
                            "got_relevant": r.relevant, "got_level": r.relevance_level, **s,
                            "seconds": round(time.time() - t0, 2)})
        except Exception as e:  # noqa: BLE001
            results.append({"id": c["id"], "decision": c["decision"], "expected": c["expected_relevance"],
                            "error": str(e), "score": 0.0, "rules": {}})
    overall = statistics.mean(x["score"] for x in results) if results else 0.0
    return {"provider": getattr(prov, "name", provider_name), "model": getattr(prov, "model", None),
            "cases": len(results), "overall": round(overall, 3), "results": results}


def to_markdown(rep: dict) -> str:
    lines = [f"# Laudato Si AI benchmark — provider: {rep['provider']} · model: {rep.get('model') or '—'}",
             f"Overall score: **{rep['overall']:.3f}** over {rep['cases']} cases", "",
             "| id | expected | relevant | level | R1 | R2 | R3 | R4 | R5 | score |", "|---|---|---|---|---|---|---|---|---|---|"]
    for x in rep["results"]:
        ru = x.get("rules", {})
        f = lambda k: "·" if ru.get(k) is None else ru[k]  # noqa: E731
        lines.append(f"| {x['id']} | {x['expected']} | {x.get('got_relevant','ERR')} | {x.get('got_level','')} | {f('R1')} | {f('R2')} | {f('R3')} | {f('R4')} | {f('R5')} | {x['score']:.2f} |")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description="Run the Laudato Si AI benchmark against a provider")
    ap.add_argument("--benchmark", default=str(Path(__file__).resolve().parents[2] / "benchmarks" / "benchmark_v1.jsonl"))
    ap.add_argument("--provider", default=None, help="anthropic | openai | openai-compatible | mock (default: auto)")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--out", default=None, help="write JSON report here")
    a = ap.parse_args()
    rep = run(Path(a.benchmark), a.provider, a.limit)
    print(to_markdown(rep))
    if a.out:
        Path(a.out).write_text(json.dumps(rep, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nJSON report → {a.out}")


if __name__ == "__main__":
    main()
