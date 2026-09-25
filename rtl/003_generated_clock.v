module generated_clock_demo (
    input  wire clk,
    input  wire din,
    output wire qout,
    output wire div2_out
);
    reg div2;
    reg data_q;
    reg qout_r;

    always @(posedge clk) begin
        div2   <= ~div2;
        data_q <= din;
    end

    always @(posedge div2)
        qout_r <= data_q;

    assign qout = qout_r;
    assign div2_out = div2;
endmodule
