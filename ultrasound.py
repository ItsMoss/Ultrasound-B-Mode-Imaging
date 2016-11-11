import helpers as helps


def read_jsonfile(infile):
    """
    Read data parameters from json file

    :param str infile: input json filename
    :returns: c, fs, axial_samples, beam_spacing, num_beams
    """
    from json import load

    with open(infile) as file:
        params = load(file)

    c = params['c']
    fs = params['fs']
    axial_samples = params['axial_samples']
    beam_spacing = params['beam_spacing']
    num_beams = params['num_beams']

    return c, fs, axial_samples, beam_spacing, num_beams


def read_rf(rf_file, size, byte_it):
    """
    Reads a single axial beam of RF data from binary file.

    :param str rf_file: input binary file name
    :param int size: the amount samples that make up a single beam
    :param int byte_it: iterator that marks where bytes should be read from
    :return array beam: a single beam of RF data from shallow to deep
    :return int byte_it: updtated iterator based on number of bytes read (is \
    -1 if error occurs or EOF reached while reading in data)
    """
    import struct as struct

    beam = [0 for x in range(size)]

    with open(rf_file, 'rb') as f:
        f.seek(byte_it)
        for i in range(size):
            try:
                beam[i] = struct.unpack('<h', f.read(2))[0]
                byte_it += 2
            except struct.error:
                print("Input RF file error! Reached EOF before amount of data \
                specified in input JSON file could be read in.\n")
                return beam, -1

    return helps.remove_nans(beam), byte_it