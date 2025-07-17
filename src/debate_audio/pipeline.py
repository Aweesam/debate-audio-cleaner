"""
pipeline.py
~~~~~~~~~~~
End‑to‑end orchestration:

YouTube URL ─▶ download WAV ─▶ enhance ─▶ (optional) diarise ─▶ save cleaned WAV
"""

from __future__ import annotations

import logging
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from .downloader import AudioDownloader

# Type stubs—actual implementations live under `enhancers/` and `diarization/`
class BaseEnhancer:  # pragma: no cover
    """Interface every enhancer must implement."""

    def enhance_file(self, in_wav: Path, out_wav: Path) -> None:  # noqa: D401
        """Transform `in_wav` into a denoised `out_wav`."""
        raise NotImplementedError


class BaseDiarizer:  # pragma: no cover
    """Interface every diarizer must implement."""

    def filter_top_speakers(self, in_wav: Path, out_wav: Path) -> None:
        """Keep only the desired speakers and write a new WAV."""
        raise NotImplementedError


log = logging.getLogger(__name__)


class DebateAudioPipeline:
    """
    Orchestrates all steps needed to clean debate audio.

    Parameters
    ----------
    enhancer : BaseEnhancer
        The speech‑enhancement model to apply.
    diarizer : BaseDiarizer | None
        Optional speaker‑diarisation component.
    work_dir : Path | str
        Directory to store intermediate and final artefacts.
    """

    def __init__(
        self,
        enhancer: BaseEnhancer,
        diarizer: Optional[BaseDiarizer] = None,
        work_dir: Path | str = Path("./output"),
    ) -> None:
        self.enhancer = enhancer
        self.diarizer = diarizer
        self.work_dir = Path(work_dir)
        self.work_dir.mkdir(parents=True, exist_ok=True)
        self.downloader = AudioDownloader(self.work_dir)

    # ------------------------------------------------------------------ #
    def clean(self, youtube_url: str, *, keep_intermediates: bool = False) -> Path:
        """
        Execute the download ➜ enhance ➜ diarise pipeline.

        Returns
        -------
        Path
            Filesystem location of the final cleaned WAV.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_p = Path(tmpdir)
            raw = self.downloader.fetch(youtube_url)

            enhanced = tmpdir_p / "enhanced.wav"
            log.info("Enhancing …")
            self.enhancer.enhance_file(raw, enhanced)

            if self.diarizer:
                log.info("Applying diarisation …")
                final = self.work_dir / "debate_clean.wav"
                self.diarizer.filter_top_speakers(enhanced, final)
            else:
                final = self.work_dir / "debate_clean.wav"
                shutil.move(enhanced, final)

            if keep_intermediates:
                shutil.copy(raw, self.work_dir / raw.name)

            log.info("✓ All done! Cleaned file saved → %s", final)
            return final

    # ------------------------------------------------------------------ #
    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"<DebateAudioPipeline enhancer={self.enhancer.__class__.__name__} "
            f"diarizer={self.diarizer and self.diarizer.__class__.__name__}>"
        )
