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
- `netlist/` — checked-in structural netlists when an experiment should run without synthesis
- `lib/` — synthetic/public Liberty models used only for reproducible labs
- `sdc/` — SDC examples
- `scripts/` — Yosys/OpenSTA and helper scripts
- `checker/` — deterministic sanity-checking logic as it develops
- `tests/` — deterministic regression tests
- `experiments/` — one directory per learning experiment

## Experiments

### Day 1 — Why Timing Constraints Exist

[Experiment 001](experiments/001-why-timing-constraints/README.md) builds the smallest useful timing model: arrival time, required time, and slack. It demonstrates why a path delay alone cannot tell us whether a design meets timing.

### Day 2 — A Clock Defines Edge Relationships

[Experiment 002](experiments/002-clock-edge-relationships/README.md) moves from arithmetic to a real STA-shaped flow. A two-register design, synthetic Liberty model, SDC, and OpenSTA scripts expose why a same-clock 10 ns path uses a 10 ns setup relationship but a 0 ns hold relationship. The broken case targets a nonexistent clock port so the checker must reject it.

## Quick verification

Requires Python 3.10+:

```bash
python3 -m unittest discover -s tests -v
python3 checker/check_clock_constraint.py sdc/002_clock_good.sdc
```

Expected failure case:

```bash
python3 checker/check_clock_constraint.py sdc/002_clock_bad_target.sdc
```

The second command should exit non-zero.

## Open-source EDA flow

With OpenSTA installed:

```bash
sta scripts/002_sta_good.tcl
```

With Yosys installed, the Day 2 RTL can also be mapped to the synthetic DFF library:

```bash
mkdir -p build
yosys -s scripts/002_synth.ys
```

The checked-in structural netlist keeps the STA experiment independent of synthesis so each layer can be debugged separately.

## Day 1 model

```bash
python3 scripts/timing_model.py --period 10 --delay 7
python3 scripts/timing_model.py --period 5 --delay 7
```

## Roadmap

Timing model → clocks → generated clocks → I/O constraints → uncertainty/latency → environment constraints → clock groups → timing exceptions → hierarchical SDC → constraint coverage/consistency → sanity checker → issue solver → deterministic verification → agent evaluation/regression.
