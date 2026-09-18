"""MCP server exposing `laudato_si_check` (stdio transport).

Run:  laudato-si-mcp            (after `pip install laudato-si[mcp]`)
      python -m laudato_si.server

Claude Desktop / any MCP host config example:
{
  "mcpServers": {
    "laudato-si": {
      "command": "laudato-si-mcp",
      "env": { "LAUDATO_PROVIDER": "mock" }
    }
  }
}
Set LAUDATO_PROVIDER=anthropic|openai|openai-compatible with the matching API key for real models.
"""

from __future__ import annotations

from typing import Any

from .check import laudato_si_check


def build_server():
    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP(
        "laudato-si",
        instructions=(
            "Call laudato_si_check only when a decision has material consequences for people, "
            "communities, resources, ecosystems, waste, energy, water or future generations. "
            "The tool informs; it does not decide for the user."
        ),
    )

    @mcp.tool(name="laudato_si_check")
    async def laudato_si_check_tool(
        decision: str,
        context: str | None = None,
        language: str | None = None,
        use_research: bool = False,
    ) -> dict[str, Any]:
        """Evaluate a decision through the Laudato Si AI Standard (PERSON · COMMUNITY · PLANET · FUTURE · ALTERNATIVES).

        Returns structured, non-coercive information: relevance, five lens summaries, alternatives,
        evidence needed, sources and confidence. Never a verdict.
        """
        r = await laudato_si_check(decision, context, language, use_research)
        return r.to_dict()

    return mcp


def main() -> None:
    build_server().run()


if __name__ == "__main__":
    main()
