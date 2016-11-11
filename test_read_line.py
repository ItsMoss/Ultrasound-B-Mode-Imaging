from moss_copy import read_rf


def test_read_rf():
    # import numpy as np
    # from scipy.io import loadmat

    test_file = 'test.bin'
    sz = 5

    # Test Case 1
    output1, b_it1 = read_rf(test_file, sz, 0)

    assert len(output1) == sz
    assert output1 == [19982, -6128, -340, -15342, -14867]
    assert b_it1 == sz * 2

    # Test Case 2
    output2, b_it2 = read_rf(test_file, sz, b_it1)

    assert len(output2) == sz
    assert output2 == [23354, -25445, 24448, 14301, -26437]
    assert b_it2 == b_it1 + sz * 2

    # file = loadmat('rf.mat')
    # f = file['rfdata']
    # f = np.array(f).flatten()
    # rf = f.tolist()

    # assert np.array_equal(rfdata, rf)
