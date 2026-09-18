import json
import pytest

from laudato_si import laudato_si_check_sync
from laudato_si.check import _extract_json, _validate
from laudato_si.providers import MockProvider


def test_low_relevance_returns_no_lecture():
    r = laudato_si_check_sync("What is 8 x 7?", provider="mock")
    assert r.relevant is False
    assert r.person == {} and r.alternatives == []


def test_high_relevance_covers_all_lenses():
    r = laudato_si_check_sync("Replace 30000 working laptops this year", provider="mock")
    assert r.relevant is True and r.relevance_level == "high"
    for k in ("person", "community", "planet", "future"):
        assert getattr(r, k)
    assert len(r.alternatives) >= 2 and r.evidence_needed


def test_empty_decision_rejected():
    with pytest.raises(ValueError):
        laudato_si_check_sync("   ", provider="mock")


def test_validate_enforces_proportionality_guard():
    d = _validate({"relevant": False, "person": {"summary": "x"}, "alternatives": ["a"]})
    assert d["person"] == {} and d["alternatives"] == []


def test_extract_json_from_fenced_block():
    d = _extract_json('Here you go:\n```json\n{"relevant": true}\n```')
    assert d["relevant"] is True


def test_to_dict_matches_contract_keys():
    r = laudato_si_check_sync("Build 400 homes on undeveloped land", provider=MockProvider())
    keys = set(r.to_dict())
    for k in ("relevant", "relevance_level", "summary", "person", "community", "planet", "future", "alternatives", "evidence_needed", "sources", "confidence"):
        assert k in keys
    json.dumps(r.to_dict())
