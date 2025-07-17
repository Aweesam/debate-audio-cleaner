
"""
debate_audio.enhancers
======================

Collection of pluggable speech‑enhancement back‑ends.

Typical usage:
    >>> from debate_audio.enhancers.metricgan import MetricGANEnhancer
"""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING

from .base import BaseEnhancer

__all__: list[str] = ["BaseEnhancer"]

# Lazy‑load heavy sub‑modules so `pip install debate-audio-cleaner`
# doesn't *require* GPU libs until the user actually selects them.
for _name in ("metricgan", "voicefixer"):
    try:
        _mod = import_module(f"{__name__}.{_name}")
        __all__.extend(_mod.__all__)  # type: ignore[attr-defined]
    except ModuleNotFoundError:
        if TYPE_CHECKING:
            raise  # keep mypy happy; at runtime we swallow the error
