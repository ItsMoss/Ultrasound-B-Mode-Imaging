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


def init_matrix(x_len, y_len):
    """
    Initializes a 2-dimensional matrix with all values equal to 0

    :param int x_len: x-axis length (i.e. number of columns)
    :param int y_len: y-axis length (i.e. number of rows)
    :return list: 2-D matrix with all values initialized to 0
    """
    return [[0 for x in range(x_len)] for y in range(y_len)]


def parse_main():
    """This function sets default values or accepts
    user inputs for the variables in main function

    :returns: args
    """
    import argparse as ap

    par = ap.ArgumentParser(description="Accept user input argument",
                            formatter_class=ap.ArgumentDefaultsHelpFormatter)

    par.add_argument("--json_filename",
                     dest="json_filename",
                     help="Data acquisition metadata in json file",
                     type=str,
                     default="bmode.json")

    par.add_argument("--rf_filename",
                     dest="rf_filename",
                     help="RF binary filename",
                     type=str,
                     default="rfdat.bin")

    args = par.parse_args()

    return args


def calc_lat_position(beam_spacing, num_beams):
    """
    Calculate lateral position and length

    :param beam_spacing: spacing between lateral beams (m)
    :param num_beams: number of lateral beams
    :returns: lateral (list), total_lateral (float)
    """

    import numpy as np

    start_position = -((num_beams-1)/2)*beam_spacing
    end_position = ((num_beams)/2)*beam_spacing
    lat = np.arange(start_position, end_position, beam_spacing)
    lateral = list(lat)

    total_lateral = float(beam_spacing*num_beams)

    return lateral, total_lateral


def calc_axial_position(c, fs, axial_samples):
    """
    Calculate axial position and length

    :param c: souns speed (m/s)
    :param fs: sampling frequency (Hz)
    :param axial_samples: number of samples in depth
    :returns: axial (list), total_depth (float)
    """

    import numpy as np

    try:
        delta_t = 1/fs
    except ZeroDivisionError:
        print('Input Parameter Error! Improbable sampling frequency')
        return 0.0, 0.0

    distance_btw_sample = c*delta_t

    start_position = 0
    end_position = distance_btw_sample*(axial_samples)
    ax = np.arange(start_position, end_position, distance_btw_sample)
    axial = ax.tolist()

    total_depth = float((axial_samples-1)*distance_btw_sample)

    return axial, total_depth


def rectify(beam, rtype='full'):
    """
    Rectifies a beam of RF data

    :param list beam: a single beam of RF data
    :param str rtype: type of rectification to be done (full or half)
    :return list beam: rectified beam of RF data
    """
    if rtype == 'full':
        for i, v in enumerate(beam):
            if v < 0:
                beam[i] = -v
    elif rtype == 'half':
        for i, v in enumerate(beam):
            if v < 0:
                beam[i] = 0
    else:
        print("Invalid param rtype. Value must be 'full' or 'half'.\n")
        raise ValueError

    return beam


def find_envelope(beam):
    """
    Finds the envelope of a rectified beam of RF data

    :param list beam: a single beam of RF data
    :param float sf: smoothing factor for smoothing spline fit (0 =< sf <= 1)
    :return list envelope: an envelope of a beam of RF data
    """
    if min(beam) < 0:
        print("Error. The input signal is not rectified, so running a full-wav\
        e rectifier on it.\n")
        beam = rectify(beam)

    from numpy import int16, ones, convolve

    beam_max = max(beam)
    np_beam = helps.list2numpy(beam)

    window = len(beam) // 5
    beam_env = convolve(np_beam, ones(window, dtype=int16)/window, mode='same')

    envelope = helps.numpy2list(beam_env)
    env_max = max(envelope)
    offset = beam_max - env_max
    envelope = helps.listAdd(envelope, offset)

    return envelope
