create_clock -name root_clk -period 10.0 -waveform {0.0 5.0} [get_ports clk]
create_clock -name div2_clk -period 20.0 -waveform {0.0 10.0} [get_pins u_div/Q]
