"""
debate_audio.diarization
========================
Speaker‑diarisation helpers that can trim the debate audio down
to the loudest N debaters and discard most audience noise.
"""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING

__all__: list[str] = []

try:
    _mod = import_module(f"{__name__}.pyannote")
    __all__.extend(_mod.__all__)  # type: ignore[attr-defined]
except ModuleNotFoundError:
    if TYPE_CHECKING:
        raise
