# Experiment 001 — Why Timing Constraints Exist

## Question

A combinational path takes 7 ns. Is that fast enough?

There is no correct answer until the design states **when the result is required**. Timing correctness is relational: an arrival time is compared with a required time.

For the minimal single-cycle model used here:

```text
arrival  = launch + path_delay
required = launch + clock_period
slack    = required - arrival
```

Positive or zero slack passes. Negative slack fails.

## Correct case

A 7 ns path under a 10 ns clock period:

```bash
python3 scripts/timing_model.py --period 10 --delay 7
```

Expected:

```text
arrival  = 7.000 ns
required = 10.000 ns
slack    = 3.000 ns
status   = PASS
```

## Intentionally broken case

Keep the exact same physical path but tighten the requirement to 5 ns:

```bash
python3 scripts/timing_model.py --period 5 --delay 7
```

Expected:

```text
arrival  = 7.000 ns
required = 5.000 ns
slack    = -2.000 ns
status   = FAIL
```

The implementation did not change. Only the constraint changed, yet the timing conclusion reversed.

## What this establishes

The first sanity-checking question is therefore not "does the report contain a violation?" It is "did we correctly express the timing intent that makes PASS or FAIL meaningful?"

Later experiments will replace this deliberately small arithmetic model with clock objects, SDC semantics, timing graphs, hierarchical object resolution, and tool-grounded verification.

## Verification

```bash
python3 -m unittest discover -s tests -v
```

The regression test proves that the same 7 ns path passes at 10 ns and fails at 5 ns, and rejects an invalid zero-period clock.

## Related article

The Day 1 article is published in the SDC/STA series on [Scott Yo-Ru Chen's technical site](https://rightson.github.io/).
