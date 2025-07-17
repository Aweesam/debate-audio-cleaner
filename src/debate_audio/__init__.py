"""
debate_audio
============

High‑level public API for the Debate‑Audio‑Cleaner project.

Typical usage:
    >>> from debate_audio import DebateAudioPipeline, MetricGANEnhancer
    >>> pipe = DebateAudioPipeline(MetricGANEnhancer())
    >>> pipe.clean("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
"""

from __future__ import annotations

import importlib.metadata as _ilm

# Re‑export library‑facing classes for convenience
from .downloader import AudioDownloader
from .pipeline import DebateAudioPipeline
try:
    from .enhancers.metricgan import MetricGANEnhancer
except ModuleNotFoundError:  # enhancers package might not be populated yet
    MetricGANEnhancer = None  # type: ignore

__all__ = [
    "AudioDownloader",
    "DebateAudioPipeline",
    "MetricGANEnhancer",
]

# Package version (falls back to "0.0.0" in editable installs)
try:
    __version__: str = _ilm.version(__name__)
except _ilm.PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0"
