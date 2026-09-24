module two_stage (
    input  wire clk,
    input  wire din,
    output wire qout
);
    reg q1;
    reg q2;

    always @(posedge clk) begin
        q1 <= din;
        q2 <= q1;
    end

    assign qout = q2;
endmodule
