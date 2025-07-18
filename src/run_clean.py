#!/usr/bin/env python3
"""
run_clean.py  ───────────────────────────────────────────────────────
Fire‑and‑forget driver that:

  1.  Downloads the YouTube audio track
  2.  Runs Demucs‑Denoiser on GPU (multi‑speaker friendly)
  3.  (Optional) runs diarisation if Hugging Face token is set
  4.  Saves output/debate_clean.wav

Edit the constants at the top, then:

    python run_clean.py
"""

from __future__ import annotations
import logging
from pathlib import Path

from debate_audio import DebateAudioPipeline
from debate_audio.enhancers.demucs import DemucsEnhancer  # ← NEW

# Optional diarisation (needs HF token + pyannote.audio)
# from debate_audio.diarization.pyannote import PyannoteDiarizer

# ─── CONFIG – EDIT AS NEEDED ───────────────────────────────────────
YOUTUBE_URL: str = "https://www.youtube.com/watch?v=OTp8ImYnM6U"
USE_GPU: bool = True                 # False → CPU
ENABLE_DIAR: bool = False            # True → run speaker diarisation
OUTPUT_DIR: Path = Path("output")
KEEP_INTERMEDIATES: bool = False     # True = keep raw/enhanced WAVs
# ────────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(name)s: %(message)s",
)

device = "cuda" if USE_GPU else "cpu"
enhancer = DemucsEnhancer(device=device)      # ← Use Demucs

diarizer = None
if ENABLE_DIAR:
    try:
        from debate_audio.diarization.pyannote import PyannoteDiarizer
        diarizer = PyannoteDiarizer(num_speakers=2, device=device)
    except Exception as exc:  # noqa: BLE001
        logging.warning("Diarisation disabled (%s)", exc)

pipeline = DebateAudioPipeline(
    enhancer=enhancer,
    diarizer=diarizer,
    work_dir=OUTPUT_DIR,
)

if __name__ == "__main__":
    pipeline.clean(YOUTUBE_URL, keep_intermediates=KEEP_INTERMEDIATES)
