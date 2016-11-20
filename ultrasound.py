import helpers as helps
import logging as log


def read_jsonfile(infile):
    """
    Read data parameters from json file

    :param str infile: input json filename
    :returns: c, fs, axial_samples, beam_spacing, num_beams
    """
    from json import load
    log.debug("Reading input JSON file")

    with open(infile) as file:
        params = load(file)

    return params


def read_rf(rf_file, size, byte_it):
    """
    Reads a single axial beam of RF data from binary file.

    :param str rf_file: input binary file name
    :param int size: the amount samples that make up a single beam
    :param int byte_it: iterator that marks where bytes should be read from
    :return list beam: a single beam of RF data from shallow to deep
    :return int byte_it: updtated iterator based on number of bytes read (is \
    -1 if error occurs or EOF reached while reading in data)
    """
    import struct as struct
    log.debug("Reading input binary file of RF data")

    beam = [0 for x in range(size)]

    with open(rf_file, 'rb') as f:
        f.seek(byte_it)
        for i in range(size):
            try:
                beam[i] = struct.unpack('<h', f.read(2))[0]
                byte_it += 2
            except struct.error:
                errmsg = "Input RF file error! Reached EOF before amount of \
                data specified in input JSON file could be read in.\n"
                print(errmsg)
                log.error(errmsg)
                return beam, -1

    return helps.remove_nans(beam), byte_it


def init_matrix(x_len, y_len):
    """
    Initializes a 2-dimensional matrix with all values equal to 0

    :param int x_len: x-axis length (i.e. number of columns)
    :param int y_len: y-axis length (i.e. number of rows)
    :return ndarray: 2-D matrix with all values initialized to 0
    """
    from numpy import zeros
    log.debug("Initializing 2D image matrix")
    return zeros((y_len, x_len))


def parse_main():
    """
    This function sets default values or accepts user inputs for the variables
    in main function

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

    par.add_argument("--log_level",
                     dest="log_level",
                     help="Level of logging user wishes to be printed to ou\
                     tput file. Accepatable values are DEBUG, INFO, WARNING\
                     , ERROR, and CRITICAL. DEFAULT=DEBUG",
                     type=str,
                     default="DEBUG")

    par.add_argument("--display",
                     dest="display",
                     help="Display B-mode Image (default: False)",
                     type=bool,
                     default=False)

    par.add_argument("--save",
                     dest="save",
                     help="Save PNG image (default: True)",
                     type=bool,
                     default=True)

    par.add_argument("--save_filename",
                     dest="save_filename",
                     help="Filename to save a PNG file of B-mode Image "
                          "(default: bmode.png)",
                     type=str,
                     default='bmode.png')

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
    log.debug("Calculating lateral dimension for output image")

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
    log.debug("Calculating axial dimension for output image")

    try:
        delta_t = 1/fs
    except ZeroDivisionError:
        errmsg = "Input Parameter Error! Improbable sampling frequency"
        print(errmsg)
        log.error(errmsg)
        # raise ZeroDivisionError
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
    log.debug("Rectifying RF beam")

    if rtype == 'full':
        for i, v in enumerate(beam):
            if v < 0:
                beam[i] = -v
    elif rtype == 'half':
        for i, v in enumerate(beam):
            if v < 0:
                beam[i] = 0
    else:
        errmsg = "Invalid param rtype. Value must be 'full' or 'half'.\n"
        print(errmsg)
        log.error(errmsg)
        raise ValueError

    return beam


def find_envelope(beam):
    """
    Finds the envelope of a rectified beam of RF data

    :param list beam: a single beam of RF data
    :param float sf: smoothing factor for smoothing spline fit (0 =< sf <= 1)
    :return list envelope: an envelope of a beam of RF data
    """
    log.debug("Finding envelope of RF beam")

    if min(beam) < 0:
        wrnmsg = "Warning. The input signal is not rectified, so running a \
        full-wave rectifier on it.\n"
        print(wrnmsg)
        log.warning(wrnmsg)
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


def log_comp(env_line):
    """
    Perform logarithmic compression on envelope line

    :param env_line: envelope of rf line (list)
    :returns: comp_line (list)
    """
    log.debug("Performing logarithmic compresssion on RF envelope")

    data = [abs(x) for x in env_line]
    comp_line = [x**0.4 for x in data]

    return comp_line


def plot_bmode(x_axis, y_axis, data):
    """
    Generate figure for B-mode image

    :param x_axis: x axis (list)
    :param y_axis: y axis (list)
    :param data: data for b-mode display (2D matrix)
    :return: fig
    """
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm

    fig = plt.pcolormesh(x_axis, y_axis, data, cmap=cm.gray)
    plt.title('B-mode Image')
    plt.xlabel('Lateral Position (m)')
    plt.ylabel('Depth (m)')
    plt.axis([min(x_axis), max(x_axis), min(y_axis), max(y_axis)])
    plt.axis('image')

    return fig


def save_bmode(fig, save, filename):
    """
    Save B-mode image

    :param fig: figure for bmode
    :param save: save image (True/False)
    :param filename: filename (.png)
    :return:
    """

    import matplotlib
    matplotlib.use('Agg')
    import re
    import matplotlib.pyplot as plt

    if save is True:
        try:
            plt.savefig(filename, bbox_inches='tight')
        except ValueError:
            print('Warning: Unable to save as specified extension '
                  '- save as PNG file')
            regex = r"^(.*?)\..*"
            filename = re.findall(regex, filename)
            plt.savefig(filename[0], bbox_inches='tight')
    elif save is False:
        pass
    else:
        print('Warning: Unable to process save input '
              '- set to default (False)')
        pass


def display_bmode(fig, display):
    """
    Display B-mode image
    :param fig: figure for b-mode image
    :param display: display choice (True/False)
    :return:
    """

    import matplotlib.pyplot as plt

    if display is True:
        plt.show(fig)
    elif display is False:
        pass
    else:
        print('Warning: Unable to process display input '
              '- set to default (False)')
        pass


def reshape_matrix(matrix_in):
    """
    Reshape 2D B-mode matrix
    :param matrix_in: input 2D matrix
    :return: matrix_out
    """
    import numpy as np

    # Check matrix size and dimension
    matrix_size = np.shape(matrix_in)
    matrix_ndim = len(matrix_size)
    if matrix_ndim >2:
        matrix_in = np.squeeze(matrix_in)

    matrix_out = matrix_in.transpose()

    return matrix_out

