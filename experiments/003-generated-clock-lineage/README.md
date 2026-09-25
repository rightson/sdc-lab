# Experiment 003 — Generated Clock Lineage

## Question

A divider output runs at 50 MHz, so its period is 20 ns. Why is that number still insufficient?

Because two clock definitions can have the same numeric period while representing different timing models. An internal divider output is physically and temporally derived from the 10 ns root clock. The STA model should preserve that provenance.

The good constraint is:

```tcl
create_clock -name root_clk -period 10.0 -waveform {0.0 5.0} [get_ports clk]
create_generated_clock -name div2_clk -source [get_ports clk] -divide_by 2 [get_pins u_div/Q]
```

For a divide-by-two generated clock, the equivalent source-edge selection is `{1 3 5}`: source rising edge 1 becomes the generated rising edge, source rising edge 3 becomes the generated falling edge, and source rising edge 5 starts the next cycle. The generated period is therefore 20 ns.

## Design

`generated_clock_demo` contains a toggle divider, a root-clock launch register, and a register captured by the divided clock:

```text
                      +---------------------+
root clk ------------>| u_div (toggle DFF) |---- div2 ----+
   |                  +---------------------+              |
   |                                                       v
   +----> u_launch DFF ---- data_q -----------------> u_capture DFF
```

The divider output is a real clock node in the timing graph, not a second external oscillator.

The checked-in structural netlist uses a synthetic DFF and inverter Liberty model so the experiment can run without a proprietary PDK.

## Intentional comparison case

`sdc/003_generated_clock_independent.sdc` uses:

```tcl
create_clock -name div2_clk -period 20.0 -waveform {0.0 10.0} [get_pins u_div/Q]
```

The 20 ns period is numerically correct. That is why this bug is more interesting than a typo.

The problem is provenance: this command creates another primary clock at the divider output instead of a clock derived from `root_clk`. In an ideal zero-latency toy example, some edge times can look identical, which can hide the modeling error. Once source latency, insertion delay, jitter/uncertainty, phase transformation, or multiple possible master clocks matter, the distinction is no longer cosmetic.

AMD's Vivado constraint documentation warns that using `create_clock` instead of `create_generated_clock` for a derived clock prevents the child clock from inheriting source-clock properties such as insertion delay and jitter. Intel likewise documents generated clocks as transformations of a source waveform and explains that generated-clock source latency follows the generated clock network plus the master clock context.

## Run the deterministic checker

Good case:

```bash
python3 checker/check_generated_clock.py sdc/003_generated_clock_good.sdc
```

Expected evidence includes:

```text
root period     : 10.000 ns
definition mode : generated
derived period  : 20.000 ns
lineage kept    : True
source edges    : 1 3 5  (rise/fall/rise)
```

Comparison case:

```bash
python3 checker/check_generated_clock.py sdc/003_generated_clock_independent.sdc
```

It must exit non-zero even though it prints a 20 ns derived period.

Run all deterministic regressions:

```bash
python3 -m unittest discover -s tests -v
```

## Run OpenSTA

With OpenSTA installed:

```bash
sta scripts/003_sta_good.tcl
sta scripts/003_sta_independent.tcl
```

Compare more than the final slack. Record:

1. how `report_clocks` describes `root_clk` and `div2_clk`;
2. the launch/capture edge relationship on the `u_launch/Q -> u_capture/D` path;
3. the clock arrival at `u_capture/CK`;
4. whether the derived clock reports a master/source relationship;
5. which differences remain invisible in this idealized pre-CTS model.

That last point matters. The comparison case does not have to show different slack in every idealized setup. The purpose is to prove that the constraint model retains the evidence needed to stay correct when physical clock-path effects are introduced later.

## Optional Yosys synthesis

```bash
mkdir -p build
yosys -s scripts/003_synth.ys
```

Compare the mapped divider structure with `netlist/003_generated_clock.v`. The checked-in netlist remains the reference for OpenSTA so synthesis and timing-model debugging stay separable.

## Sanity rule introduced today

For every clock created on an internal node, ask:

> Is this node truly a new independent clock source, or is it derived from an already-defined clock?

If it is derived, the checker should require evidence for:

- master/source clock;
- resolved source object;
- resolved generated-clock target;
- waveform transformation;
- expected period, phase, and duty cycle;
- propagation to intended sequential sinks.

## Sources

- OpenSTA command reference — `create_generated_clock`: https://opensta.readthedocs.io/en/latest/Commands/
- Intel Timing Analyzer — `create_generated_clock`: https://www.intel.com/content/www/us/en/programmable/quartushelp/24.2/tafs/tafs/tcl_pkg_sdc_ver_1.5_cmd_create_generated_clock.htm
- AMD Vivado Tcl — `create_generated_clock`: https://docs.amd.com/r/2020.2-English/ug835-vivado-tcl-commands/create_generated_clock
- AMD Vivado Tcl — `create_clock`: https://docs.amd.com/r/2023.2-English/ug835-vivado-tcl-commands/create_clock

## Related article

https://rightson.github.io/timing/2026/09/25/generated-clock-edge-lineage.html
