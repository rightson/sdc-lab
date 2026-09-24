read_liberty lib/sdc_lab_min.lib
read_verilog netlist/002_two_stage.v
link_design two_stage
read_sdc sdc/002_clock_good.sdc

puts "=== CLOCKS ==="
report_clocks
puts "=== SETUP / MAX PATH ==="
report_checks -path_delay max -format full_clock
puts "=== HOLD / MIN PATH ==="
report_checks -path_delay min -format full_clock
