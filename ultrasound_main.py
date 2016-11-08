# This file is for main program

def main():
    pass

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

    args = par.parse_args()

    return args


if __name__ == "__main__":
    main()
