"""
voicefixer.py
~~~~~~~~~~~~~
Wrapper for VoiceFixer 2.

Install notes
-------------
pip install voicefixer
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Literal, final

from .base import BaseEnhancer

log = logging.getLogger(__name__)

__all__: list[str] = ["VoiceFixerEnhancer"]


@final
class VoiceFixerEnhancer(BaseEnhancer):
    """High‑quality restoration for distorted / clipped recordings."""

    def __init__(self, device: Literal["cpu", "cuda"] = "cpu") -> None:
        try:
            from voicefixer import VoiceFixer  # type: ignore
        except ModuleNotFoundError as e:  # pragma: no cover
            raise ImportError(
                "VoiceFixerEnhancer requires the `voicefixer` package.\n"
                "→ pip install voicefixer"
            ) from e

        self._vf = VoiceFixer(device=device)

    # ------------------------------------------------------------------ #
    def enhance_file(self, in_wav: Path, out_wav: Path) -> None:  # noqa: D401
        log.debug("VoiceFixer enhancing %s → %s", in_wav, out_wav)
        self._vf.restore(input=in_wav, output=out_wav)
