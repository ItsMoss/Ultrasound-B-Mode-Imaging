import moss_copy as us


def test_rect():
    """
    Tests rect functionality from ultrasound.py
    """
    full = 'full'
    half = 'half'

    # Test Case 1
    input1 = [-4, -15, -2, 4, 20]
    output1 = us.rect(input1)
    assert output1 == [4, 15, 2, 4, 20]

    # Test Case 2
    input2 = [1, 14, 4, 10, 17]
    output2 = us.rect(input2)
    assert output2 == input2

    # Test Case 3
    input3 = [-10, -15, -5, -10, -3]
    output3 = us.rect(input3, full)
    assert output3 == [10, 15, 5, 10, 3]

    # Test Case 4
    input4 = [19, 0, -12, -7, 20]
    output4 = us.rect(input4)
    assert output4 == [19, 0, 12, 7, 20]

    # Test Case 5
    input5 = [-3, -6, 8, 12, -5]
    output5 = us.rect(input5, half)
    assert output5 == [0, 0, 8, 12, 0]
