# Changelog

All notable changes to this project are documented here. Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning: [SemVer](https://semver.org/).

## [1.0.0] — 2026-09-18
### Added
- Normative specification `standard/LAUDATO_SI_AI_STANDARD_1.0.md` (five lenses, human autonomy, proportionality, evidence, social justice, consumption, long-term responsibility, positive action, transparency).
- Universal system prompt, MCP tool contract (`mcp/TOOL_CONTRACT.md`) and JSON schema (`mcp/laudato_si_check.schema.json`).
- Python reference implementation `laudato-si`: `laudato_si_check`, CLI, MCP server (stdio), benchmark runner, offline mock provider, tests, CI.
- Benchmark v1: 20 cases (low / medium / high relevance) with rubric `benchmarks/RUBRIC.md`.
- Adoption guides (Anthropic, OpenAI, Google Gemini, open models), governance, contributing, code of conduct.
- Real licenses: Apache-2.0 (code) and CC BY 4.0 (standard text); `CITATION.cff`.

### Notes
- Independent initiative; not affiliated with the Holy See or any AI laboratory.
- The mock provider is a deterministic baseline for reproducibility, not a model result.
