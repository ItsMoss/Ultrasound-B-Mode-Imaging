import ultrasound as us

def test_calc_axial():
    """
    Tests cal_axial_position functionality from ultrasound.py
    """

    [ax1, total_depth1] = us.calc_axial_position(1, 100, 10)
    assert ax1 == [0.00, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]
    assert total_depth1 == 0.09

    [ax2, total_depth2] = us.calc_axial_position(0.5, 50, 10)
    assert ax2 == [0.00, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]
    assert total_depth2 == 0.09

    [ax3, total_depth3] = us.calc_axial_position(1, 0, 10)
    assert ax1 == 0.0
    assert total_depth1 == 0.0