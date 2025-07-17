"""
pyannote.py
~~~~~~~~~~~
Speaker trimming using *pyannote.audio*'s pretrained pipelines.

Install
-------
pip install pyannote.audio
# and set HF_TOKEN env‑var if the model is gated.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Literal, final
import os
#from huggingface_hub import HfHubHTTPError


from ..enhancers.base import BaseEnhancer  # import just for type hints

log = logging.getLogger(__name__)

__all__: list[str] = ["PyannoteDiarizer"]


@final
class PyannoteDiarizer:
    """
    Keep only the `num_speakers` loudest speakers in the waveform.

    Parameters
    ----------
    num_speakers : int
        How many distinct voices to preserve.
    device : Literal["cpu", "cuda"]
        Compute device.
    """

    def __init__(
        self,
        num_speakers: int = 2,
        device: Literal["cpu", "cuda"] = "cpu",
    ) -> None:
        try:
            from pyannote.audio import Pipeline
        except ModuleNotFoundError as e:  # pragma: no cover
            raise ImportError(
                "PyannoteDiarizer requires `pyannote.audio`.\n"
                "→ pip install pyannote.audio"
            ) from e

        # model card: https://huggingface.co/pyannote/speaker-diarization
        try:
            self._pl = Pipeline.from_pretrained(
                "pyannote/speaker-diarization@2.1",
                use_auth_token=os.getenv("HUGGING_FACE_HUB_TOKEN"),
            )
        except (HfHubHTTPError, ValueError):
            log.warning("pyannote model gated or token missing -> diarisation disabled.")
            self._pl = None

        if self._pl is not None:
            self._pl.to(device)
        self._num = num_speakers

        # torchaudio is a pyannote dep, but we check explicitly for clarity
        try:
            import torchaudio  # noqa: F401
        except ModuleNotFoundError as e:  # pragma: no cover
            raise ImportError("`torchaudio` is required for PyannoteDiarizer.") from e

    # ------------------------------------------------------------------ #
    def filter_top_speakers(self, in_wav: Path, out_wav: Path) -> None:
        """
        Analyse `in_wav`, keep top‑N loudest speakers, write to `out_wav`.
        """
        import torch
        import torchaudio  # type: ignore

        diar = self._pl(in_wav)
        speaker_energy: dict[str, float] = {}

        # Aggregate energy per speaker
        for segment, track, label in diar.itertracks(yield_label=True):
            samples = track.data  # (n_frames,) torch Tensor
            speaker_energy[label] = speaker_energy.get(label, 0.0) + samples.pow(2).sum().item()

        top_labels = {
            lbl for lbl, _ in sorted(speaker_energy.items(), key=lambda kv: kv[1], reverse=True)[: self._num]
        }
        log.debug("Retaining speakers: %s", ", ".join(sorted(top_labels)))

        waveform, sr = torchaudio.load(in_wav)  # (channels, n_samples)
        mask = torch.zeros_like(waveform)

        # Build a binary mask of desired segments
        for segment, _, label in diar.itertracks(yield_label=True):
            if label in top_labels:
                start = int(segment.start * sr)
                end = int(segment.end * sr)
                mask[:, start:end] = 1.0

        torchaudio.save(out_wav, waveform * mask, sr)
        log.info("Diarised output written → %s", out_wav)
