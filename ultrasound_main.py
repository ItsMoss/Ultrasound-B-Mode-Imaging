# This file is for main program
import ultrasound as us
import helpers as helps
from numpy import array
import logging as log


def main():
    # 1. Parse Command Line arguments
    main_args = us.parse_main()
    json_file = main_args.json_filename
    rf_file = main_args.rf_filename
    log_level = main_args.log_level
    display = main_args.display
    save = main_args.save

    # Start Logging
    helps.init_log_file("b_mode_us", "BME590 Assignment 05", log_level)

    # 2. Read JSON metadata
    params = us.read_jsonfile(json_file)

    c = params['c']
    Fs = params['fs']
    axial_samples = params['axial_samples']
    beam_spacing = params['beam_spacing']
    n_beams = params['num_beams']
    log.info("C = %d m/s\nFs = %d Hz\nAxial samples=%d\nBeam spacing = %.8f m\
             \nNumber of beams = %d", c, Fs, axial_samples, beam_spacing,
             n_beams)

    # 3. Initialize 2-D Matrix
    image_matrix = us.init_matrix(axial_samples, n_beams)

    # 4. Read in a Single Beam of RF data while matrix not full
    byte_n = 0  # read-in byte counter
    for line, _ in enumerate(range(n_beams)):

        rf_beam, byte_n = us.read_rf(rf_file, axial_samples, byte_n)

        # Error handling
        if byte_n == -1:
            return

        # 5. Rectify Beam
        rf_beam = us.rectify(rf_beam)

        # 6. Create Envelope of Beam
        rf_beam = us.find_envelope(rf_beam)

        # 7. Logarithmic Compression
        rf_beam = us.log_comp(rf_beam)

        # 8. Place Beam in 2-D Matrix
        image_matrix[line] = array(rf_beam)

    # 9. Output
    # A. Reshape Matrix
    bmode_data = us.reshape_matrix(image_matrix)

    # B. Axes Calculations
    x_axis, x_len = us.calc_lat_position(beam_spacing, n_beams)
    log.info("X Length = %.5f m", x_len)
    y_axis, y_len = us.calc_axial_position(c, Fs, axial_samples)
    log.info("Y Length = %.5f m", y_len)

    # C. Plot/Save/Display Image
    fig = us.plot_bmode(x_axis, y_axis, bmode_data)
    us.save_bmode(fig, save)
    us.display_bmode(fig, display)

    log.info("EXIT SUCCESS")


if __name__ == "__main__":
    main()
