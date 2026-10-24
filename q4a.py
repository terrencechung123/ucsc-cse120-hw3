import pyrtl

def datapath(zero, lt, opcode):
    # opcode: 00=blt, 01=bge, 10=beq, 11=bne
    take_blt = (opcode == 0b00) & lt
    take_bge = (opcode == 0b01) & ~lt
    take_beq = (opcode == 0b10) & zero
    take_bne = (opcode == 0b11) & ~zero
    return take_blt | take_bge | take_beq | take_bne


if __name__ == "__main__":
    zero = pyrtl.Input(1, "zero")
    lt = pyrtl.Input(1, "lt")
    opcode = pyrtl.Input(2, "opcode")

    branch_out = datapath(zero, lt, opcode)
    branch = pyrtl.Output(1, "branch")
    branch <<= branch_out

    # Test all 16 combinations of opcode, zero, and lt.
    sim = pyrtl.Simulation()
    for op in range(4):
        for zero_value in range(2):
            for lt_value in range(2):
                sim.step({"zero": zero_value, "lt": lt_value, "opcode": op})
                if op == 0b00:
                    expected = lt_value
                elif op == 0b01:
                    expected = 1 - lt_value
                elif op == 0b10:
                    expected = zero_value
                else:
                    expected = 1 - zero_value
                assert sim.inspect("branch") == expected
    print("All 16 branch tests passed.")
