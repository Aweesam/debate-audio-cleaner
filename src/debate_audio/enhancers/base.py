"""
base.py
~~~~~~~
Abstract interface that all enhancer classes must follow.
"""

from __future__ import annotations

import abc
from pathlib import Path


class BaseEnhancer(abc.ABC):
    """Blueprint for a speech‑enhancement component."""

    @abc.abstractmethod
    def enhance_file(self, in_wav: Path, out_wav: Path) -> None:  # noqa: D401
        """
        Transform `in_wav` → `out_wav`.

        Implementations SHOULD:
        - leave sample‑rate and bit‑depth unchanged, unless documented otherwise
        - be deterministic (same input → same output)
        - raise an Exception if processing fails
        """
