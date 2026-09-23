# SDC Lab

A public, reproducible lab for learning Static Timing Analysis (STA), Synopsys Design Constraints (SDC), constraint sanity checking, and eventually agent-assisted issue solving.

The repository grows one experiment at a time. Each experiment starts from a timing question, provides a deterministic executable model, includes both correct and intentionally broken cases, and defines observable expected results.

## Principles

- Correctness before agents.
- Minimal reproducible experiments before framework complexity.
- Every broken case must have an explicit expected failure.
- Public/synthetic examples only. No proprietary design data, rules, logs, skills, PDK content, or internal implementation details.
- Agent reasoning, when introduced later, must be grounded by deterministic evidence and verification.

## Layout

- `rtl/` — minimal RTL used by experiments
- `sdc/` — SDC examples
- `scripts/` — executable helpers
- `checker/` — sanity-checking logic as it develops
- `tests/` — deterministic regression tests
- `experiments/` — one directory per learning experiment

## Day 1

[Why Timing Constraints Exist](experiments/001-why-timing-constraints/README.md) builds the smallest useful timing model: arrival time, required time, and slack. It demonstrates why a path delay alone cannot tell us whether a design meets timing.

## Run

Requires Python 3.10+.

```bash
python3 scripts/timing_model.py --period 10 --delay 7
python3 scripts/timing_model.py --period 5 --delay 7
python3 -m unittest discover -s tests -v
```

## Roadmap

Timing model → clocks → generated clocks → I/O constraints → uncertainty/latency → environment constraints → clock groups → timing exceptions → hierarchical SDC → constraint coverage/consistency → sanity checker → issue solver → deterministic verification → agent evaluation/regression.
