# MCP Tool Contract

## Tool

`laudato_si_check`

## Purpose

Evaluate a decision through the Laudato Si AI Standard.

## Input

```json
{
  "decision": "string",
  "context": "string | optional",
  "language": "string | optional",
  "use_research": "boolean | optional"
}
```

## Output

```json
{
  "relevant": true,
  "person": {},
  "community": {},
  "planet": {},
  "future": {},
  "alternatives": [],
  "evidence_needed": [],
  "sources": [],
  "confidence": "low|medium|high"
}
```

## Behavioral requirement

The tool informs.
It does not make the user's decision.
