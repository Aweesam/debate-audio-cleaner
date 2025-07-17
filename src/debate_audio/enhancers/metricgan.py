"""
metricgan.py
~~~~~~~~~~~~
MetricGAN+ model via *SpeechBrain* — fast crowd‑noise suppression.

Installation
------------
pip install speechbrain torch==2.2.2+cpu -f https://download.pytorch.org/whl/torch_stable.html
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Literal, final

from .base import BaseEnhancer

log = logging.getLogger(__name__)

__all__: list[str] = ["MetricGANEnhancer"]


@final
class MetricGANEnhancer(BaseEnhancer):
    """
    Parameters
    ----------
    device : Literal["cpu", "cuda"]
        Where to run inference. "cuda" requires an NVIDIA‑enabled torch build.
    """

    def __init__(self, device: Literal["cpu", "cuda"] = "cpu") -> None:
        try:
            from speechbrain.pretrained import SpectralMaskEnhancement
        except ModuleNotFoundError as e:  # pragma: no cover
            raise ImportError(
                "MetricGANEnhancer requires `speechbrain`.\n"
                "→ pip install speechbrain"
            ) from e

        self._enh = SpectralMaskEnhancement.from_hparams(
            source="speechbrain/metricgan-plus-voicebank",
            run_opts={"device": device},
        )

    # ------------------------------------------------------------------ #
    def enhance_file(self, in_wav: Path, out_wav: Path) -> None:  # noqa: D401
        log.debug("MetricGAN+ enhancing %s → %s", in_wav, out_wav)
        self._enh.enhance_file(str(in_wav), str(out_wav))
