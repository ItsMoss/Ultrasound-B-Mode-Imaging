def test_log_comp():
    """
    Tests log_comp functionality
    """

    import tamma_copy as tc
    import numpy as np

    output1 = tc.log_comp([1, 10, 100, 1000, 10000])
    out1 = [1.0, 2.51188643150958, 6.309573444801933,
            15.848931924611136, 39.810717055349734]
    assert np.array_equal(output1, out1)

    output2 = tc.log_comp([-1, -10, -100, -1000, -10000])
    out2 = [1.0, 2.51188643150958, 6.309573444801933,
            15.848931924611136, 39.810717055349734]
    assert np.array_equal(output2, out2)

    output3 = tc.log_comp([0, 10, 100, 1000, 10000])
    out3 = [0.0, 2.51188643150958, 6.309573444801933,
            15.848931924611136, 39.810717055349734]
    assert np.array_equal(output3, out3)
