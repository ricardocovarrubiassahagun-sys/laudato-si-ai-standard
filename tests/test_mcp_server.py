import pytest

pytest.importorskip("mcp")


@pytest.mark.asyncio
async def test_tool_is_registered_and_callable(monkeypatch):
    monkeypatch.setenv("LAUDATO_PROVIDER", "mock")
    from laudato_si.server import build_server

    s = build_server()
    tools = await s.list_tools()
    names = [t.name for t in tools]
    assert "laudato_si_check" in names
    out = await s.call_tool("laudato_si_check", {"decision": "Design disposable packaging for a restaurant chain"})
    text = str(out)
    assert "relevant" in text
