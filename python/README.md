# laudato-si (Python reference implementation)

```bash
pip install -e ".[dev]"          # from python/ — offline mock provider, tests
laudato-si check "Replace 30,000 working laptops this year"          # uses mock unless an API key is set
LAUDATO_PROVIDER=anthropic ANTHROPIC_API_KEY=... laudato-si check "Build 400 homes on undeveloped land"
laudato-si-benchmark --provider mock                                  # reproducible, no keys
laudato-si-mcp                                                        # MCP server over stdio
pytest
```
See the repository root README for the standard, the tool contract and the rubric.
