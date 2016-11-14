# This file is for main program
import ultrasound as us


def main():
    # 1. Parse Command Line arguments
    main_args = us.parse_main()
    json_file = main_args.json_filename
    rf_file = main_args.rf_filename

    # 2. Read JSON metadata
    c, Fs, axial_samples, beam_spacing, n_beams = us.read_jsonfile(json_file)

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
        image_matrix[line] = rf_beam

    # 9. Output
    # A. Reshape Matrix
    # B. Axes Calculations
    x_axis, x_len = us.calc_lat_position(beam_spacing, n_beams)
    y_axis, y_len = us.calc_axial_position(c, Fs, axial_samples)
    print("Output would be produced here.\n")


if __name__ == "__main__":
    main()
