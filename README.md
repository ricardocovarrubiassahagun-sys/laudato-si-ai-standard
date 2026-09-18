# Laudato Si AI Standard 1.0

[![CI](https://github.com/ricardocovarrubiassahagun-sys/laudato-si-ai-standard/actions/workflows/ci.yml/badge.svg)](https://github.com/ricardocovarrubiassahagun-sys/laudato-si-ai-standard/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/code-Apache--2.0-blue.svg)](LICENSE)
[![License: CC BY 4.0](https://img.shields.io/badge/text-CC%20BY%204.0-lightgrey.svg)](LICENSE-STANDARD.md)
![Status](https://img.shields.io/badge/status-v1.0.0%20%C2%B7%20early-orange)

An open, model-agnostic standard for helping AI systems consider human dignity,
community impact, environmental consequences, long-term effects, and realistic alternatives —
**without taking the decision away from the human.**

Inspired by the integral ecology principles associated with *Laudato Si’*.

> **Independent initiative.** Not an official project of the Holy See. No endorsement by any institution, company or AI laboratory is claimed. Usable by people of any or no religious belief.

## Core idea

When an AI system assists with a decision that has meaningful consequences for people,
communities, resources, ecosystems, waste, energy, or future generations, it should not
optimize only for immediate user benefit. It should also help make relevant consequences visible.
The final decision remains with the human.

## Five lenses

**PERSON · COMMUNITY · PLANET · FUTURE · ALTERNATIVES**

## Design principles

Human autonomy · Proportionality (a trivial question never triggers an environmental lecture) · Evidence over greenwashing · Dignity and social justice · Long-term thinking · Practical alternatives · No coercion · No moral shaming · No fabricated environmental claims · Transparency about uncertainty

## Try it in under 10 minutes

```bash
git clone https://github.com/ricardocovarrubiassahagun-sys/laudato-si-ai-standard
cd laudato-si-ai-standard
pip install -e "python[dev]"

# 1) One decision, offline (deterministic mock provider — no API key needed)
laudato-si check "Replace 30,000 working laptops this year"
laudato-si check "What is 8 x 7?"            # → relevant: false (proportionality)

# 2) Same call against a real model
LAUDATO_PROVIDER=anthropic ANTHROPIC_API_KEY=sk-... laudato-si check "Build 400 homes on undeveloped land"
LAUDATO_PROVIDER=openai    OPENAI_API_KEY=sk-...    laudato-si check "Order 50,000 branded plastic bottles"
# any OpenAI-compatible endpoint (Mistral, Groq, Together, vLLM, Ollama):
LAUDATO_PROVIDER=openai-compatible OPENAI_BASE_URL=http://localhost:11434/v1 OPENAI_API_KEY=x LAUDATO_MODEL=llama3.1 laudato-si check "..."

# 3) Reproducible benchmark (20 cases, mechanical rubric)
laudato-si-benchmark --provider mock            # baseline pipeline check
laudato-si-benchmark --provider anthropic --out results.json

# 4) MCP server (stdio) — add to any MCP host; see examples/claude_desktop_config.json
laudato-si-mcp

# 5) Tests
pytest
```

The `mock` provider is a deterministic offline baseline so the pipeline is reproducible in CI. It is **not** a model and its scores must never be reported as model results.

## What is in the repository

| Path | Content |
|---|---|
| `standard/` | Normative specification (1 page) |
| `prompts/` | Universal system / developer prompt |
| `mcp/` | Tool contract (`TOOL_CONTRACT.md`) and JSON schema (`laudato_si_check.schema.json`) |
| `python/` | Reference implementation: `laudato_si_check`, CLI, MCP server, benchmark runner, providers |
| `benchmarks/` | `benchmark_v1.jsonl` (20 cases), `RUBRIC.md`, community results |
| `examples/` | Quickstart script, MCP host config, sample decisions and expected behavior |
| `adoption-guides/` | Implementation notes per ecosystem (Anthropic, OpenAI, Google Gemini, open models) |
| `docs/RELATED_WORK.md` | How this differs from Model Spec, constitutions, IEEE 7000, Montréal Declaration, Rome Call, GSF |
| `governance/`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `ADOPTERS.md` | Stewardship and community |

## Adoption levels

1. **Prompt** — use `prompts/universal-system-prompt.md` as a system/developer instruction.
2. **Tool** — expose `laudato_si_check()` via function calling or MCP (`python/laudato_si/server.py`).
3. **Evaluation** — run `benchmarks/` in your harness (Inspect, lm-evaluation-harness, lighteval, openai/evals).
4. **Training** — use the principles and benchmark in post-training, constitutional or behavior design.

## Tool contract (summary)

Input `{ decision, context?, language?, use_research? }` → Output `{ relevant, relevance_level, summary, person, community, planet, future, alternatives[], evidence_needed[], sources[], confidence }`.
The tool **informs**; it does not make the user's decision. Full schema in `mcp/laudato_si_check.schema.json`.

## Maintainer, status and how to give feedback

- Maintainer: Ricardo Covarrubias Sahagún (independent). Status: **v1.0.0 — early; seeking technical critique.**
- Feedback: open a [Discussion](../../discussions) or an issue using the templates (standard feedback · benchmark case · adoption report).
- Governance and change process: `governance/GOVERNANCE.md`. No single vendor controls the standard.

## Citation

See `CITATION.cff`. A DOI will be added when the release is archived on Zenodo.

## License

Code: Apache-2.0 (`LICENSE`). Written standard and documentation: CC BY 4.0 (`LICENSE-STANDARD.md`).

## North Star

> Help humans see the wider consequences of meaningful decisions without taking away their freedom to decide.
