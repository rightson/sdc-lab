module two_stage (
    input  wire clk,
    input  wire din,
    output wire qout
);
    wire q1;

    DFF ff1 (.D(din), .CK(clk), .Q(q1));
    DFF ff2 (.D(q1),  .CK(clk), .Q(qout));
endmodule
