# Compatibility

The standard is model-agnostic. Compatibility is described by interface and behavior rather than by endorsement of a vendor or model.

| Integration path | Status | Notes |
|---|---|---|
| Universal system / developer prompt | Supported | Works wherever equivalent system/developer instructions are available. |
| Python reference implementation | Supported | Python 3.10+; CI tests multiple Python versions. |
| MCP server (stdio) | Supported | Reference implementation currently targets MCP 1.x compatibility. |
| OpenAI-compatible chat endpoints | Supported by adapter | Requires a compatible endpoint and model configuration. |
| Anthropic adapter | Supported by adapter | Requires provider credentials and a compatible SDK. |
| Evaluation / benchmark runner | Supported | Mechanical v1 rubric; exact model id/date/prompt version should be reported. |
| Training / post-training use | Conceptually supported | Implementers are responsible for their own training stack and validation. |

## Versioning

- Standard version: 1.0
- Reference implementation package: 1.0.0
- MCP compatibility in the current reference implementation: `mcp>=1.2,<2`

## Compatibility claims

A project should describe the exact adoption level it implements and should not imply certification, endorsement, or conformance beyond what it has actually tested.
