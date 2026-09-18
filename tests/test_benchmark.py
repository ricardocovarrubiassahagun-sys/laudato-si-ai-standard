from pathlib import Path

from laudato_si.benchmark import run, to_markdown

ROOT = Path(__file__).resolve().parents[1]


def test_benchmark_runs_offline_and_mock_scores_high():
    rep = run(ROOT / "benchmarks" / "benchmark_v1.jsonl", "mock")
    assert rep["cases"] == 20
    assert rep["overall"] >= 0.9  # mock follows proportionality by construction
    md = to_markdown(rep)
    assert "| LS001 |" in md
