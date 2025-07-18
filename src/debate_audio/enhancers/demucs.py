from __future__ import annotations
import logging, subprocess, tempfile
from pathlib import Path
from .base import BaseEnhancer

log = logging.getLogger(__name__)

class DemucsEnhancer(BaseEnhancer):
    """Multi‑speaker crowd‑noise suppression with Demucs v4."""
    def __init__(self, device: str = "cuda") -> None:
        self.device = device

    def enhance_file(self, in_wav: Path, out_wav: Path) -> None:
        with tempfile.TemporaryDirectory() as d:
            cmd = [
                "python", "-m", "demucs", "-n", "htdemucs_ft",
                "--two-stems=vocals", "--device", self.device, "-o", d, str(in_wav)
            ]
            subprocess.run(cmd, check=True)
            # Demucs writes .../htdemucs_ft/<filename>/vocals.wav
            stem = Path(d) / "htdemucs_ft" / in_wav.stem / "vocals.wav"
            stem.rename(out_wav)
            log.info("Demucs output → %s", out_wav)
