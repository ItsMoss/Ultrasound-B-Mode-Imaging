import moss_copy as us


def test_init_matrix():
    """
    This function tests the functionality of init_matrix from ultrasound.py
    """
    output1 = us.init_matrix(0, 0)
    assert output1 == []

    output2 = us.init_matrix(1, 0)
    assert output2 == []

    output3 = us.init_matrix(2, 2)
    assert output3 == [[0, 0], [0, 0]]

    output4 = us.init_matrix(2, 4)
    assert output4 == [[0, 0], [0, 0], [0, 0], [0, 0]]
