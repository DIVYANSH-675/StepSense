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


def align(expected, observed):
    """Minimum edit alignment, retaining repeated actions and deterministic ties."""
    if any(type(x) is not int or x < 0 for x in expected + observed):
        raise ValueError("Action IDs must be nonnegative integers")
    n, m = len(expected), len(observed)
    cost = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        cost[i][0] = i
    for j in range(m + 1):
        cost[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost[i][j] = min(cost[i-1][j] + 1, cost[i][j-1] + 1,
                             cost[i-1][j-1] + (expected[i-1] != observed[j-1]))
    edits = []
    i, j = n, m
    while i or j:
        if i and j and cost[i][j] == cost[i-1][j-1] + (expected[i-1] != observed[j-1]):
            if expected[i-1] != observed[j-1]:
                edits.append({"kind": "substitution", "step": i-1, "segment": j-1,
                              "expected": expected[i-1], "observed": observed[j-1]})
            i, j = i-1, j-1
        elif i and cost[i][j] == cost[i-1][j] + 1:
            edits.append({"kind": "missing", "step": i-1, "expected": expected[i-1]})
            i -= 1
        else:
            edits.append({"kind": "extra", "segment": j-1, "observed": observed[j-1]})
            j -= 1
    return {"edit_distance": cost[n][m], "issues": list(reversed(edits))}


def review(predictions, expected, min_frames=1):
    runs = segments(predictions, min_frames)
    result = align(expected, [run["action"] for run in runs])
    for issue in result["issues"]:
        if "segment" in issue:
            run = runs[issue["segment"]]
            issue["frame_range"] = [run["start"], run["end"]]
    return {**result, "segments": runs}


