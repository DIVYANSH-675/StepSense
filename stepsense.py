"""Compare a PREGO prediction sequence to an expected procedure."""
import argparse
import json
from pathlib import Path


def segments(predictions, min_frames=1):
    if type(min_frames) is not int or min_frames < 1:
        raise ValueError("min_frames must be a positive integer")
    if not isinstance(predictions, list) or any(type(x) is not int or x < 0 for x in predictions):
        raise ValueError("predictions must be a list of nonnegative integer action IDs")
    runs = []
    for frame, action in enumerate(predictions):
        if runs and runs[-1]["action"] == action:
            runs[-1]["end"] = frame + 1
        else:
            runs.append({"action": action, "start": frame, "end": frame + 1})
    return [run for run in runs if run["end"] - run["start"] >= min_frames]


