"""
downloader.py
~~~~~~~~~~~~~
Lightweight wrapper around *yt-dlp* that extracts a YouTube video's audio
stream and converts it to 16‑bit PCM WAV—ready for enhancement models.
"""

from __future__ import annotations

import logging
import shutil
import subprocess
from pathlib import Path
from typing import List

log = logging.getLogger(__name__)


def _run(cmd: List[str]) -> None:
    """Run a shell command, raising if the exit code is non‑zero."""
    log.debug("Running shell command: %s", " ".join(cmd))
    subprocess.run(cmd, check=True)


class AudioDownloader:
    """
    Parameters
    ----------
    out_dir : Path | str
        Directory where the extracted WAV file will be saved.
    """

    def __init__(self, out_dir: Path | str = Path("./data")) -> None:
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)
        if shutil.which("ffmpeg") is None:  # yt‑dlp relies on ffmpeg for re‑mux
            raise EnvironmentError("ffmpeg not found on PATH. Please install it.")

    # --------------------------------------------------------------------- #
    def fetch(self, youtube_url: str) -> Path:
        """
        Download *only* the audio track, convert it to WAV, and return the path.

        Notes
        -----
        - Requires `yt-dlp` to be installed in the current environment.
        - Audio is re‑encoded to 16‑bit PCM, 48 kHz by ffmpeg behind the scenes.
        """
        wav_target = self.out_dir / "raw_audio.wav"
        cmd = [
            "yt-dlp",
            "-x",                   # extract audio only
            "--audio-format", "wav",
            "--output", str(wav_target),
            youtube_url,
        ]
        _run(cmd)
        log.info("Downloaded audio → %s", wav_target)
        return wav_target
