import tamma_copy as tc


def test_read_jsonfile():
    """
    Tests read_jsonfile functionality from ultrasound.py
    """

    infile = 'bmode.json'
    params = tc.read_jsonfile(infile)

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


def test_save_img():

    import numpy as np
    import os

    data = np.zeros((100, 100))
    line = np.array(range(1, 101))
    for i in range(0, 100):
        data[i] = line

    xaxis = np.linspace(1, 10, 100)
    yaxis = np.linspace(1, 10, 100)

    fig = tc.plot_bmode(xaxis, yaxis, data)

    # Case 1
    checkfile = os.path.isfile('test1.png')
    if checkfile is True:
        os.remove('test1.png')
    tc.save_bmode(fig, True, 'test1.png')
    output = os.path.isfile('test1.png')
    assert output is True

    # Case 2
    checkfile = os.path.isfile('test2.png')
    if checkfile is True:
        os.remove('test2.png')
    tc.save_bmode(fig, True, 'test2')
    output = os.path.isfile('test2.png')
    assert output is True

    # Case 3
    checkfile = os.path.isfile('test3.png')
    if checkfile is True:
        os.remove('test3.png')
    tc.save_bmode(fig, True, 'test3.jpeg')
    output = os.path.isfile('test3.png')
    assert output is True

    # Case4
    checkfile = os.path.isfile('test4.png')
    if checkfile is True:
        os.remove('test4.png')
    tc.save_bmode(fig, False, 'test4.png')
    output = os.path.isfile('test4.png')
    assert output is False

    # Case5
    checkfile = os.path.isfile('test5.png')
    if checkfile is True:
        os.remove('test5.png')
    tc.save_bmode(fig, 'F', 'test5.png')
    output = os.path.isfile('test5.png')
    assert output is False
