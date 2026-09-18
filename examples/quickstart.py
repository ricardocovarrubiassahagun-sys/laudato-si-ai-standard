"""10-minute quickstart. Run: python examples/quickstart.py  (offline mock unless an API key is set)."""
from laudato_si import laudato_si_check_sync

for decision in ["What is 8 x 7?", "Replace 30,000 working laptops this year"]:
    r = laudato_si_check_sync(decision)
    print(f"\n{decision}\n  relevant={r.relevant} level={r.relevance_level} provider={r.provider}")
    if r.relevant:
        print("  alternatives:", "; ".join(r.alternatives[:3]))
        print("  evidence needed:", "; ".join(r.evidence_needed[:2]))
