module generated_clock_demo (
    input  wire clk,
    input  wire din,
    output wire qout,
    output wire div2_out
);
    wire div2;
    wire div2_d;
    wire data_q;

    INV u_inv     (.A(div2),   .Y(div2_d));
    DFF u_div     (.D(div2_d), .CK(clk),  .Q(div2));
    DFF u_launch  (.D(din),    .CK(clk),  .Q(data_q));
    DFF u_capture (.D(data_q), .CK(div2), .Q(qout));

    assign div2_out = div2;
endmodule
