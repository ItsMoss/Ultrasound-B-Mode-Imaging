import ultrasound as us


def test_read_jsonfile():
    """
    Tests read_jsonfile functionality from ultrasound.py
    """

    infile = 'bmode.json'
    [c, fs, axial_samples, beam_spacing, num_beams] = us.read_jsonfile(infile)
    param = [c, fs, axial_samples, beam_spacing, num_beams]

    assert param == [1540, 40000000, 1556, 0.00011746274509803921, 256]


def test_read_rf():
    """
    Tests read_rf functionality from ultrasound.py
    """
    # import numpy as np
    # from scipy.io import loadmat

    test_file = 'test.bin'
    sz = 5

    # Test Case 1
    output1, b_it1 = us.read_rf(test_file, sz, 0)

    assert len(output1) == sz
    assert output1 == [19982, -6128, -340, -15342, -14867]
    assert b_it1 == sz * 2

    # Test Case 2
    output2, b_it2 = us.read_rf(test_file, sz, b_it1)

    assert len(output2) == sz
    assert output2 == [23354, -25445, 24448, 14301, -26437]
    assert b_it2 == b_it1 + sz * 2

    # file = loadmat('rf.mat')
    # f = file['rfdata']
    # f = np.array(f).flatten()
    # rf = f.tolist()

    # assert np.array_equal(rfdata, rf)


def test_init_matrix():
    """
    Tests init_matrix functionality from ultrasound.py
    """
    output1 = us.init_matrix(0, 0)
    assert output1 == []

    output2 = us.init_matrix(1, 0)
    assert output2 == []

    output3 = us.init_matrix(2, 2)
    assert output3 == [[0, 0], [0, 0]]

    output4 = us.init_matrix(2, 4)
    assert output4 == [[0, 0], [0, 0], [0, 0], [0, 0]]
