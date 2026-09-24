# Intentional failure: the design has no port named clkk.
create_clock -name clk -period 10.0 -waveform {0.0 5.0} [get_ports clkk]
