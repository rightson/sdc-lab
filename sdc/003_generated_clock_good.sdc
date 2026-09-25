create_clock -name root_clk -period 10.0 -waveform {0.0 5.0} [get_ports clk]
create_generated_clock -name div2_clk -source [get_ports clk] -divide_by 2 [get_pins u_div/Q]
