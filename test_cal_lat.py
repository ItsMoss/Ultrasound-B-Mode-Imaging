def test_calc_lat_position():
    """
    Tests cal_lat_position functionality from ultrasound.py
    """

    import ultrasound as us

    [lat1, total_lat1] = us.calc_lat_position(1, 5)
    assert lat1 == [-2.0, -1.0, 0.0, 1.0, 2.0]
    assert total_lat1 == 5.0

    [lat2, total_lat2] = us.calc_lat_position(1, 6)
    assert lat2 == [-2.5, -1.5, -0.5, 0.5, 1.5, 2.5]
    assert total_lat2 == 6.0

    [lat3, total_lat3] = us.calc_lat_position(0.5, 5)
    assert lat3 == [-1.0, -0.5, 0.0, 0.5, 1.0]
    assert total_lat3 == 2.5