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


def test_reshape_matrix():
    import numpy as np

    # Case 1
    data = np.zeros((5, 10))
    data_size = np.shape(data)
    nrow_in = data_size[0]
    ncolumn_in = data_size[1]

    output = tc.reshape_matrix(data)
    output_size = np.shape(output)
    nrow_out = output_size[0]
    ncolumn_out = output_size[1]

    assert nrow_in == ncolumn_out
    assert nrow_out == ncolumn_in

    # Case 2
    data = np.zeros((1, 10))
    data_size = np.shape(data)
    nrow_in = data_size[0]
    ncolumn_in = data_size[1]

    output = tc.reshape_matrix(data)
    output_size = np.shape(output)
    nrow_out = output_size[0]
    ncolumn_out = output_size[1]

    assert nrow_in == ncolumn_out
    assert nrow_out == ncolumn_in

    # Case 3
    data = np.zeros((5, 1))
    data_size = np.shape(data)
    nrow_in = data_size[0]
    ncolumn_in = data_size[1]

    output = tc.reshape_matrix(data)
    output_size = np.shape(output)
    nrow_out = output_size[0]
    ncolumn_out = output_size[1]

    assert nrow_in == ncolumn_out
    assert nrow_out == ncolumn_in

    # Case 4
    data = np.zeros((5, 10))
    line = np.array(range(1, 11))
    for i in range(0, 5):
        data[i] = line
    data_row1 = data[0]

    output = tc.reshape_matrix(data)
    output_row1 = output[...,0]

    assert np.array_equal(data_row1, output_row1)

    # Case 5
    data = np.zeros((5, 1, 10))
    data_size = np.shape(data)
    nrow_in = data_size[0]
    ncolumn_in = data_size[2]

    output = tc.reshape_matrix(data)
    output_size = np.shape(output)
    nrow_out = output_size[0]
    ncolumn_out = output_size[1]

    assert nrow_in == ncolumn_out
    assert nrow_out == ncolumn_in
