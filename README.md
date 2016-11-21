# Assignment 05
## B-Mode Ultrasound Imaging
Authors: Moseph Jackson-Atogi, Tamma Ketsiri

### File Descriptions:
+ `ultrasound_main.py` - **main** file that runs B-Mode imaging program
+ `ultrasound.py` - file containing all function definitions used in main program
+ `helpers.py` - file containing various helper functions used in main program
+ `test_ultrasound.py` - file containing all unit tests for main program
+ `createTest.sh` - bash shell script for generating `test.bin` binary file
+ `test.bin` - a test binary file used to test reading in binary data properly
+ `rfdat.bin` - test binary file containing RF data used to debug main program
+ `bmode.json` - JSON file containing image parameters used for testing and debugging main program
+ `rf.mat` - a MATLAB file equivalent `rfdat.bin` for testing various input types
+ `requirements.txt` - file outlining dependencies needed for CI
+ `baseline/` - folder containing a test image used in unit testing image plotting
+ `docs/` - folder containing all Sphinx documentation

### Running Program
To run this program simply run `ultrasound_main.py` from the terminal. Use -h option to see what command line arguments are taken and what default values are. Note that a log file named `b_mode_us.log` will be auto-generated with information regarding the status of the program, as well as values of important variables. A command line argument can be passed to determine the level of logging desired.

### Happy Thanksgiving
