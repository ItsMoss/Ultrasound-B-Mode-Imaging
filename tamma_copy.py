# File for all function definitions used in ultrasound_main.py


def read_jsonfile(infile):
    """ Read data parameters from json file

    :param infile: input json filename (str)
    :returns: params
    """

    import json

    with open(infile) as file:
        params = json.load(file)

    return params


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
    :returns: comp_line (list)
    """

    data = [abs(x) for x in env_line]
    comp_line = [x**0.4 for x in data]

    return comp_line


def display_bmode(x_axis, y_axis, data):
    """
    Display B-mode image
    :param x_axis: x axis (list)
    :param y_axis: y axis (list)
    :param data: data for b-mode display (2D matrix)
    :return:
    """

    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    plt.pcolormesh(x_axis, y_axis, bmode_data, cmap=cm.gray)
    plt.title('B-mode Image')
    plt.show()


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

    par.add_argument("--display",
                     dest="display",
                     help="Display B-mode Image (default: False)",
                     type=bool,
                     default=False)

    par.add_argument("--save",
                     dest="save",
                     help="Filename to save a PNG file of B-mode Image "
                          "(default: bmode.png)",
                     type=str,
                     default='bmode.png')

    args = par.parse_args()

    return args


def plot_bmode(x_axis, y_axis, data):
    """
    Generate figure for B-mode image

    :param x_axis: x axis (list)
    :param y_axis: y axis (list)
    :param data: data for b-mode display (2D matrix)
    :return: fig
    """

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

    import matplotlib.pyplot as plt
    import re

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
