import ultrasound as us
import helpers as helps
from numpy import arange
from random import randrange


def test_read_jsonfile():
    """
    Tests read_jsonfile functionality from ultrasound.py
    """

    infile = 'bmode.json'
    params = us.read_jsonfile(infile)
    c = params['c']
    fs = params['fs']
    axial_samples = params['axial_samples']
    beam_spacing = params['beam_spacing']
    num_beams = params['num_beams']

    assert c == 1540
    assert fs == 40000000
    assert axial_samples == 1556
    assert beam_spacing == 0.00011746274509803921
    assert num_beams == 256


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
    assert output1.tolist() == []

    output2 = us.init_matrix(1, 0)
    assert output2.tolist() == []

    output3 = us.init_matrix(2, 2)
    assert output3.tolist() == [[0, 0], [0, 0]]

    output4 = us.init_matrix(2, 4)
    assert output4.tolist() == [[0, 0], [0, 0], [0, 0], [0, 0]]


def test_calc_lat_position():
    """
    Tests cal_lat_position functionality from ultrasound.py
    """

    [lat1, total_lat1] = us.calc_lat_position(1, 5)
    assert lat1 == [-2.0, -1.0, 0.0, 1.0, 2.0]
    assert total_lat1 == 5.0

    [lat2, total_lat2] = us.calc_lat_position(1, 6)
    assert lat2 == [-2.5, -1.5, -0.5, 0.5, 1.5, 2.5]
    assert total_lat2 == 6.0

    [lat3, total_lat3] = us.calc_lat_position(0.5, 5)
    assert lat3 == [-1.0, -0.5, 0.0, 0.5, 1.0]
    assert total_lat3 == 2.5


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
    assert ax3 == 0.0
    assert total_depth3 == 0.0


def test_rectify():
    """
    Tests rect functionality from ultrasound.py
    """
    full = 'full'
    half = 'half'

    # Test Case 1
    input1 = [-4, -15, -2, 4, 20]
    output1 = us.rectify(input1)
    assert output1 == [4, 15, 2, 4, 20]

    # Test Case 2
    input2 = [1, 14, 4, 10, 17]
    output2 = us.rectify(input2)
    assert output2 == input2

    # Test Case 3
    input3 = [-10, -15, -5, -10, -3]
    output3 = us.rectify(input3, full)
    assert output3 == [10, 15, 5, 10, 3]

    # Test Case 4
    input4 = [19, 0, -12, -7, 20]
    output4 = us.rectify(input4)
    assert output4 == [19, 0, 12, 7, 20]

    # Test Case 5
    input5 = [-3, -6, 8, 12, -5]
    output5 = us.rectify(input5, half)
    assert output5 == [0, 0, 8, 12, 0]


def test_find_env():
    """
    Tests find_envelope functionality from ultrasound.py
    """
    t = 5
    dt = 0.001
    t_axis = arange(0, t, dt)

    # Test Case 1 - Sine 1
    sine_curve1 = helps.makeSine(t, 5, 5, t_step=dt)
    # Rectify
    sine_rect1 = us.rectify(sine_curve1, 'half')
    # Find envelope
    sine_env1 = us.find_envelope(sine_rect1)

    assert min(sine_env1) >= 0
    assert max(sine_env1) == max(sine_curve1)
    assert helps.listAverage(sine_env1) >= helps.listAverage(sine_rect1)

    # Test Case 2 - Sine 2
    sine_curve2 = helps.makeCosine(t, 2, 3, t_step=dt)

    sine_env2 = us.find_envelope(sine_curve2)
    # figure(2)
    # plot(t_axis, sine_env2, 'g-*')
    # show()

    assert min(sine_env2) >= 0
    assert max(sine_env2) == max(sine_curve2)
    assert helps.listAverage(sine_env1) >= helps.listAverage(sine_curve2)

    # Test Case 3 - Sine 3
    sine_curve3 = helps.makeCosine(t, 1, 10, t_step=dt)

    sine_env3 = us.find_envelope(sine_curve3)
    # plot(t_axis, sine_env3, 'g-*')
    # show()

    assert min(sine_env3) >= 0
    assert max(sine_env3) == max(sine_curve3)
    assert helps.listAverage(sine_env3) >= helps.listAverage(sine_curve3)

    # Test Case 4 - Random 1
    rand_curve1 = [randrange(-10, 11, 1) for x in range(len(t_axis))]
    # figure(1)
    # plot(t_axis, rand_curve1, 'r')

    rand_rect1 = us.rectify(rand_curve1, 'half')
    # plot(t_axis, rand_rect1, 'b')

    rand_env1 = us.find_envelope(rand_rect1)
    # plot(t_axis, rand_env1, 'g-*')
    # show()

    assert min(rand_env1) >= 0
    assert max(rand_env1) == max(rand_rect1)
    assert helps.listAverage(rand_env1) >= helps.listAverage(rand_rect1)

    # Test Case 5 - Random 2
    rand_curve2 = [randrange(-25, 26, 1) for x in range(len(t_axis))]
    # figure(2)
    # plot(t_axis, rand_curve2, 'r')

    rand_rect2 = us.rectify(rand_curve2)
    # plot(t_axis, rand_rect2, 'b')

    rand_env2 = us.find_envelope(rand_rect2)
    # plot(t_axis, rand_env2, 'g-*')
    # show()

    assert min(rand_env2) >= 0
    assert max(rand_env2) == max(rand_rect2)
    assert helps.listAverage(rand_env2) >= helps.listAverage(rand_rect2)

    # Test Case 6 - Random 3
    rand_curve3 = [randrange(-15, 26, 1) for x in range(len(t_axis))]
    # figure(3)
    # plot(t_axis, rand_curve3, 'r')

    rand_rect3 = us.rectify(rand_curve3)
    # plot(t_axis, rand_rect3, 'b')

    rand_env3 = us.find_envelope(rand_rect3)
    # plot(t_axis, rand_env3, 'g-*')
    # show()

    assert min(rand_env3) >= 0
    assert max(rand_env3) == max(rand_rect3)
    assert helps.listAverage(rand_env3) >= helps.listAverage(rand_rect3)

    # Test Case 7 - PWM 1
    pwm1 = helps.makePWM(t, 3, 0.63, 5)

    pwm_env1 = us.find_envelope(pwm1)
    # plot(t_axis, pwm_env1, 'g-*')
    # show()

    assert min(pwm_env1) >= 0
    assert max(pwm_env1) == max(pwm1)

    # Test Case 8 - PWM 2
    pwm2 = helps.makePWM(t, 1, 0.15, 1)

    pwm_env2 = us.find_envelope(pwm2)
    # plot(t_axis, pwm_env2, 'g-*')
    # show()

    assert min(pwm_env2) >= 0
    assert max(pwm_env2) == max(pwm2)

    # Test Case 9 - PWM 3
    pwm3 = helps.makePWM(t, 4, 2.0, 3)

    pwm_env3 = us.find_envelope(pwm3)
    # plot(t_axis, pwm_env3, 'g-*')
    # show()

    assert min(pwm_env3) >= 0
    assert max(pwm_env3) == max(pwm3)


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
