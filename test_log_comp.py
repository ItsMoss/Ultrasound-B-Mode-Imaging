def test_log_comp():
    """
    Tests log_comp functionality
    """

    import tamma_copy as tc
    import numpy as np

    output1 = tc.log_comp([1, 10, 100, 1000, 10000])
    assert np.array_equal(output1, [0.0, 1.0, 2.0, 3.0, 4.0])

    output2 = tc.log_comp([-1, -10, -100, -1000, -10000])
    assert np.array_equal(output2, [0.0, 1.0, 2.0, 3.0, 4.0])

    output3 = tc.log_comp([0, 10, 100, 1000, 10000])
    assert np.array_equal(output3, [0.0, 1.0, 2.0, 3.0, 4.0])
