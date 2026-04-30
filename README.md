# StepSense

Explain sequence differences in PREGO prediction exports.

An extension maintained by Divyansh Gupta, based on [https://github.com/aleflabo/PREGO](https://github.com/aleflabo/PREGO) at `3078571f6a827c763a4220e919c4d9b5b8adea07`. Upstream source, licenses, citations and commit history are preserved. See [upstream documentation](UPSTREAM_README.md).

## Added functionality

Collapses consecutive frame labels, optionally filters short runs with --min-frames, and computes a minimum-edit alignment. Reports missing, extra and substituted actions with zero-based step indices and half-open frame ranges where available.

## Quick start

The new utility uses Python 3.10+ and the standard library. The examples are synthetic. GPU packages are not required for the new utility or its tests.

```bash
python3 stepsense.py examples/predictions.json --expected 1,2,3 --output report.json
python3 -m unittest discover -s tests -v
```

## Scope and limitations

Offline review against a user-supplied expected sequence; not a live camera coach. Input must be frame-level predictions, not already-aggregated steps. Filtering can remove real short actions. Multiple alignments can be equally valid; findings are hypotheses, not proof of physical mistakes.

## Licensing

The new `stepsense.py`, its tests, synthetic examples, CI workflow and this README are MIT licensed in ADDITIONS_LICENSE. Upstream files retain their existing notices and terms; the new license does not relicense them.
