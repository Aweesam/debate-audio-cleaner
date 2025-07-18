#!/usr/bin/env python3
"""
clean_debate_audio.py ──────────────────────────────────────────────
One‑shot CLI wrapper around the DebateAudioPipeline.

Usage examples
--------------
# CPU‑only, skip diarisation
python scripts/clean_debate_audio.py "https://youtu.be/VIDEO_ID" --no-diar

# Use GPU and keep top‑2 speakers
python scripts/clean_debate_audio.py "https://youtu.be/VIDEO_ID" --gpu

# Show all flags
python scripts/clean_debate_audio.py -h
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from debate_audio import DebateAudioPipeline
from debate_audio.enhancers.metricgan import MetricGANEnhancer
from debate_audio.enhancers.demucs import DemucsEnhancer

# ─── optional import (only if diarisation is installed) ────────────
try:
    from debate_audio.diarization.pyannote import PyannoteDiarizer
except ModuleNotFoundError:
    PyannoteDiarizer = None  # type: ignore

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(name)s: %(message)s",
)

parser = argparse.ArgumentParser(description="Clean debate audio from YouTube.")
parser.add_argument("url", help="YouTube video URL")
parser.add_argument(
    "--out",
    type=Path,
    default=Path("./output"),
    help="Directory for cleaned WAV",
)
parser.add_argument(
    "--gpu",
    action="store_true",
    help="Run models on CUDA (requires GPU‑enabled torch build)",
)
parser.add_argument(
    "--no-diar",
    action="store_true",
    help="Skip speaker diarisation even if pyannote is installed",
)
parser.add_argument(
    "--keep-intermediates",
    action="store_true",
    help="Save raw and enhanced WAV files alongside the final output",
)

def main() -> None:
    # run --> python src\clean_debate_audio.py "https://www.youtube.com/watch?v=OTp8ImYnM6U" --gpu

    args = parser.parse_args()

    device = "cuda" if args.gpu else "cpu"
    enhancer = MetricGANEnhancer(device=device)

    diarizer = None
    if not args.no_diar and PyannoteDiarizer is not None:
        diarizer = PyannoteDiarizer(num_speakers=2, device=device)

    # pipe = DebateAudioPipeline(
    #     enhancer=enhancer,
    #     diarizer=diarizer,
    #     work_dir=args.out,
    # )
    pipe = DebateAudioPipeline(
    enhancer=DemucsEnhancer(device="cuda"),
    diarizer=None        # try without first
)
    try:
        #pipe.clean(args.url, keep_intermediates=args.keep_intermediates)
        pipe.clean(args.url, keep_intermediates=True)
    except Exception as exc:  # noqa: BLE001
        logging.error("Processing failed: %s", exc)
        sys.exit(1)


if __name__ == "__main__":  # pragma: no cover
    main()
