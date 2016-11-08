def test_read_jsonfile():

    import ultrasound

    infile = 'bmode.json'
    [c, fs, axial_samples, beam_spacing, num_beams] = ultrasound.read_jsonfile(infile)
    param = [c, fs, axial_samples, beam_spacing, num_beams]
    assert param == [1540, 40000000, 1556, 0.00011746274509803921, 256]