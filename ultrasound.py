# File for all function definitions used in ultrasound_main.py

def read_jsonfile(infile):
    """ Read data parameters from json file

    :param infile: input json filename (str)
    :returns: c, fs, axial_samples, beam_spacing, num_beams
    """

    import json

    with open(infile) as file:
        params = json.load(file)

    c = params['c']
    fs = params['fs']
    axial_samples = params['axial_samples']
    beam_spacing = params['beam_spacing']
    num_beams = params['num_beams']

    return c, fs, axial_samples, beam_spacing, num_beams
