read_liberty lib/sdc_lab_generated.lib
read_verilog netlist/003_generated_clock.v
link_design generated_clock_demo
read_sdc sdc/003_generated_clock_good.sdc

puts "=== CLOCKS ==="
report_clocks
puts "=== ROOT -> DIV2 SETUP PATH ==="
report_checks -from [get_pins u_launch/Q] -to [get_pins u_capture/D] -path_delay max -format full_clock
puts "=== DIV2 CLOCK ARRIVAL ==="
report_arrival [get_pins u_capture/CK]
