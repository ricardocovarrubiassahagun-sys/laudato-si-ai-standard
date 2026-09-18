# Related work — and how this standard differs

This standard is small on purpose and is meant to be **complementary** to existing behavior specifications, ethics frameworks and evaluation suites. It claims no affiliation with any of them.

| Framework | What it is | Relationship to Laudato Si AI Standard 1.0 |
|---|---|---|
| OpenAI Model Spec | Vendor behavior specification for OpenAI models, with an open compliance-eval harness (`openai/model_spec_evals`). | Compatible: the standard is a *decision-scoped* behavior layer (five lenses + proportionality) that can be expressed as developer instructions and checked with the same eval approach. It does not replace vendor specs. |
| Anthropic's constitution for Claude | Vendor document weighing helpfulness, safety and ethics, including interests of third parties. | Complementary: this standard operationalizes one narrow slice — consequence visibility for material decisions — as a tool contract usable by any model. |
| IEEE 7000 series / Ethically Aligned Design | Engineering process standards for addressing ethical concerns in system design. | Different level: IEEE 7000 governs *design processes* of organizations; this standard governs *runtime assistant behavior* for a decision. Could be referenced as a runtime control within a 7000-style process. |
| Montréal Declaration for Responsible AI | Ten principles (well-being, autonomy, sustainable development…). | Shared values (autonomy, sustainability); this standard adds an executable contract, a benchmark and proportionality rules. |
| Rome Call for AI Ethics | Principles (transparency, inclusion, responsibility, impartiality, reliability, security/privacy) promoted by the Pontifical Academy for Life and signatories. | Shared inspiration in human dignity; **no affiliation or endorsement**. This standard is independent and secular-usable. |
| Green Software Foundation standards (e.g. SCI) | Measuring and reducing the carbon footprint of software. | Orthogonal: GSF measures the *system's* footprint; this standard concerns what the assistant *says* about the user's decision. Both can apply at once. |
| MCP (Model Context Protocol) | Open protocol for tools/context between hosts and servers. | This standard ships an MCP tool contract and a reference server; it is a *consumer* of MCP, not a modification of it. |
| Evaluation harnesses (Inspect, lm-evaluation-harness, lighteval, openai/evals) | Frameworks to run model evaluations. | The benchmark is designed to be packaged as a task in these harnesses; v1 uses mechanical rules for reproducibility. |

Corrections welcome — open a Discussion if any characterization above is inaccurate.
