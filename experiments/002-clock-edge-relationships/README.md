# Experiment 002 — A Clock Defines Edge Relationships

## Question

For two positive-edge-triggered flip-flops on the same 10 ns clock, why does STA use a 10 ns relationship for setup but a 0 ns relationship for hold?

The key is that setup and hold are not the same check with opposite signs. They select different launch/capture edge relationships:

```text
same rising-edge clock, period = 10 ns

rising edges:  0 -------- 10 -------- 20 ns

setup:          L -------- C          => 10 ns
hold:           L/C                    =>  0 ns
```

OpenSTA documents `report_checks -path_delay max` as setup/max analysis and `-path_delay min` as hold/min analysis. Intel's Timing Analyzer documentation likewise shows a same-clock 10 ns example with a default 10 ns setup relationship and 0 ns hold relationship.

## Design

`rtl/002_two_stage.v` is a two-register pipeline. `netlist/002_two_stage.v` is the equivalent structural netlist using one synthetic `DFF` cell from `lib/sdc_lab_min.lib`.

The tiny Liberty model intentionally uses simple scalar timing numbers:

- CK→Q: 0.20 ns
- setup: 0.50 ns
- hold: 0.10 ns

These values are synthetic and exist only to make the timing relationship observable.

## Good constraint

`sdc/002_clock_good.sdc`:

```tcl
create_clock -name clk -period 10.0 -waveform {0.0 5.0} [get_ports clk]
```

First run the deterministic sanity check:

```bash
python3 checker/check_clock_constraint.py sdc/002_clock_good.sdc
```

Expected key lines:

```text
setup edges  : 10.000 ns apart
hold edges   : 0.000 ns apart
```

With OpenSTA installed:

```bash
sta scripts/002_sta_good.tcl
```

Inspect the `max` report for the setup relationship and the `min` report for the hold relationship. Do not compare only final slack; look at the launch clock edge, capture clock edge, library setup/hold term, and data arrival time.

## Intentional failure

`sdc/002_clock_bad_target.sdc` targets `clkk`, which does not exist in the design.

```bash
python3 checker/check_clock_constraint.py sdc/002_clock_bad_target.sdc
```

The checker must fail because the intended clock does not resolve to the real top-level `clk` port. With OpenSTA:

```bash
sta scripts/002_sta_bad.tcl
```

The expected outcome is an error/diagnostic for the bad object reference or, if execution continues, unconstrained timing evidence. This is a useful sanity-checker rule: a syntactically plausible `create_clock` line is not enough; the target collection must resolve to the intended design object.

## Optional Yosys synthesis

The structural netlist is checked in so OpenSTA can run without synthesis. To also exercise the RTL→netlist step:

```bash
mkdir -p build
yosys -s scripts/002_synth.ys
```

The generated `build/002_two_stage_yosys.v` should contain mapped `DFF` instances. Compare it with the hand-written structural netlist before using it for timing analysis.

## What to record

For each run, capture these facts rather than only PASS/FAIL:

1. Which SDC line created the clock?
2. Which design object did `[get_ports ...]` actually resolve to?
3. What period and waveform did the tool create?
4. Which launch and capture edges were selected for `max` and `min` analysis?
5. Which Liberty setup/hold arc constrained the endpoint?
6. Was the path constrained at all?

Those six facts are the beginning of an evidence package that a future issue-solving agent can reason over without guessing.

## Sources

- OpenSTA command reference: https://opensta.readthedocs.io/en/latest/Commands/
- OpenSTA examples: https://opensta.readthedocs.io/en/latest/Examples/
- OpenSTA debugging guide: https://opensta.readthedocs.io/en/latest/Debugging/
- Intel Quartus Timing Analyzer User Guide: https://www.intel.com/programmable/technical-pdfs/683068.pdf
- Liberty Reference Manual example for setup/hold timing arcs: https://people.eecs.berkeley.edu/~alanmi/publications/other/liberty13_03.pdf

## Related article

https://rightson.github.io/eda/2026/09/24/clock-edges-define-setup-hold.html
