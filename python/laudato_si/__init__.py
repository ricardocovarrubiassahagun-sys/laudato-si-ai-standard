"""Laudato Si AI Standard 1.0 — reference implementation.

Model-agnostic helper that evaluates a decision through five lenses
(PERSON · COMMUNITY · PLANET · FUTURE · ALTERNATIVES) and returns structured,
non-coercive information so the *human* decides.

Independent initiative. Not an official project of the Holy See.
"""

from .check import (
    SYSTEM_PROMPT,
    CheckResult,
    laudato_si_check,
    laudato_si_check_sync,
)

__version__ = "1.0.0"
__all__ = ["laudato_si_check", "laudato_si_check_sync", "CheckResult", "SYSTEM_PROMPT", "__version__"]
