def test_read_jsonfile():

    import ultrasound

    infile = 'bmode.json'
    [c, fs, axial_samples, beam_spacing, num_beams] = ultrasound.read_jsonfile(infile)
    param = [c, fs, axial_samples, beam_spacing, num_beams]
    assert param == [1540, 40000000, 1556, 0.00011746274509803921, 256]

def test_read_rffile():

    import ultrasound
    import numpy as np
    from scipy.io import loadmat
    import time

    rffile = 'rfdat.bin'
    rfdata = ultrasound.read_rffile(rffile)
    file = loadmat('rf.mat')
    f = file['rfdata']
    f = np.array(f).flatten()
    rf = f.tolist()
    assert np.array_equal(rfdata, rf)