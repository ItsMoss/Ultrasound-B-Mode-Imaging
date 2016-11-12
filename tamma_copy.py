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


def read_rffile(rffile):
    """ Read RF data from binary file

    :param rffile: input rf binary filename (str)
    :returns: rfdata
    """

    rfdata = []

    with open(rffile, 'rb') as file:
        data = file.read(2)
        while data:
            rf = int.from_bytes(data, byteorder='little', signed=True)
            rfdata.append(rf)
            data = file.read(2)

    return rfdata


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


def log_comp(env_line):
    """
    Perform logarithmic compression on envelope line

    :param env_line: envelope of rf line (list)
    :returns: log_line (list)
    """

    import numpy as np

    data = [abs(x) for x in env_line]

    for i, j in enumerate(data):
        if j == 0:
            print('Warning! Might encounter incorrect data from '
                  'taking logarithmic calculation of zero')
            data[i] = 1

    log_line = np.log10(data)

    return log_line
