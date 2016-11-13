import moss_copy as us
import helpers as helps
from matplotlib.pyplot import figure, plot, show
from numpy import arange
from random import randrange


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
    sine_rect1 = us.rect(sine_curve1, 'half')
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

    rand_rect1 = us.rect(rand_curve1, 'half')
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

    rand_rect2 = us.rect(rand_curve2)
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

    rand_rect3 = us.rect(rand_curve3)
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
