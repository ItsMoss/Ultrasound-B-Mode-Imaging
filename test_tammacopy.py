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

    assert c ==1540
    assert fs == 40000000
    assert axial_samples == 1556
    assert beam_spacing == 0.00011746274509803921
    assert num_beams == 256
    
