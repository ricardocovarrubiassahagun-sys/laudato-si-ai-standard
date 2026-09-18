"""CLI: `laudato-si check "Replace 30,000 working laptops this year"`"""

from __future__ import annotations

import argparse
import json

from .check import laudato_si_check_sync


def main() -> None:
    ap = argparse.ArgumentParser(prog="laudato-si", description="Laudato Si AI Standard 1.0 — consequence check")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="evaluate a decision through the five lenses")
    c.add_argument("decision")
    c.add_argument("--context", default=None)
    c.add_argument("--language", default=None)
    c.add_argument("--provider", default=None, help="anthropic | openai | openai-compatible | mock")
    c.add_argument("--research", action="store_true")
    a = ap.parse_args()
    r = laudato_si_check_sync(a.decision, a.context, a.language, a.research, a.provider)
    print(json.dumps(r.to_dict(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
