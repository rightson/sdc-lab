read_liberty lib/sdc_lab_min.lib
read_verilog netlist/002_two_stage.v
link_design two_stage
read_sdc sdc/002_clock_bad_target.sdc

# If the bad constraint does not abort first, this exposes unconstrained paths.
report_checks -unconstrained -path_delay min_max
