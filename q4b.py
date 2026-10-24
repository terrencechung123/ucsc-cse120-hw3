import pyrtl

if __name__ == "__main__":
    enable = pyrtl.Input(1, "enable")
    reset = pyrtl.Input(1, "reset")
    y = pyrtl.Register(2, "y")

    # Reset takes priority; otherwise increment when enabled or hold.
    incremented = pyrtl.truncate(y + pyrtl.Const(1, bitwidth=2), 2)
    y.next <<= pyrtl.select(
        reset,
        pyrtl.Const(0, bitwidth=2),
        pyrtl.select(enable, incremented, y),
    )

    trace = pyrtl.SimulationTrace()
    sim = pyrtl.Simulation(tracer=trace)

    # Each tuple is (reset, enable, expected y after the clock edge).
    test_steps = [
        (1, 0, 0),  # reset
        (0, 0, 0),  # hold at zero
        (0, 1, 1),  # increment to one
        (0, 0, 1),  # hold at one
        (0, 1, 2),  # increment to two
        (0, 1, 3),  # increment to three
        (0, 1, 0),  # two-bit wraparound
        (1, 1, 0),  # reset wins over enable
    ]

    for reset_value, enable_value, expected_y in test_steps:
        sim.step({"reset": reset_value, "enable": enable_value})
        assert sim.inspect("y") == expected_y

    print("All counter tests passed.")
    trace.render_trace()
