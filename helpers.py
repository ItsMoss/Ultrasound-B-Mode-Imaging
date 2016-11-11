def myAverage(n1, n2):
    """
    This function calculates the average of two integers
    If one of the input numbers is not an integer a zero is returned

    :param int n1: number one
    :param int n2: number two
    :return int a: calculated average
    """
    if type(n1) != int or type(n2) != int:
        return 0

    a = myRound((n1 + n2) / 2)
    return a


def myRound(n):
    """
    This function rounds a number up if it has decimal >= 0.5

    :param float n: input number
    :return int r: rounded number
    """
    if n % 1 >= 0.5:
        r = int(n) + 1
    else:
        r = int(n)

    return r


def listAverage(input_list):
    """
    This function finds the average value in a list

    :param list input_list: a list of all integer values
    :return float average: calculated list average
    """
    if len(input_list) < 1:
        print("\nCannot take average. List has length=0\n")
        # raise IndexError

    denominator = len(input_list)

    numerator = 0
    for i in range(denominator):
        # if type(input_list[i]) != int:
            # print("\nList must only consist of integer values\n")
            # raise TypeError
        numerator += input_list[i]

    average = numerator / denominator

    return round(average, 2)


def listInts(input_list):
    """
    This function takes a list of ints and/or floats and converts all values to
    type int

    :param list input_list: list of ints and/or floats
    :return list int_list: list of only ints
    """
    for i in range(len(input_list)):
        try:
            input_list[i] = int(input_list[i])
        except (TypeError, ValueError):
            print("\nValues in input list must be types int or float\n")
            # raise TypeError

    int_list = input_list

    return int_list


def list2numpy(input_list):
    """
    This function converts a list into a numpy array of int16 values

    :param list input_list: list of presumably ints
    :return array np_array: numpy array of int16 values
    """
    from numpy import array, int16

    np_array = array(input_list, dtype=int16)

    return np_array


def numpy2list(input_numpy):
    """
    This function converts a numpy array of int16 values to a list

    :param array input_array: numpy array of int16 values
    :return list output_list: list of ints
    """
    from numpy import ndarray

    if type(input_numpy) != ndarray:
        print("\nYour input must be a numpy array\n")
        # raise TypeError

    output_list = listInts(list(input_numpy))

    return output_list


def makeSine(time, amplitude, frequency, phase=0):
    """
    This function is for creating sine waves of varying time, amplitude, freq,
    and phase for simulating input signals

    :param int time: time in seconds for sine curve
    :param int amplitude: amplitude of sine curve
    :param int frequency: frequency of sine curve in Hz
    :param int phase: phase of sine curve in radians
    :return array curve: calculated sine curve
    """
    from numpy import sin, pi, arange
    t = arange(0, time, 0.01)
    a = amplitude
    f = frequency
    p = phase

    curve = a * sin(2 * pi * f * t + p)
    for p in range(len(curve)):
        curve[p] = round(curve[p], 2)

#    from matplotlib.pyplot import figure, plot, show
#    figure(1)
#    plot(t, curve)
#    show()

    return curve


def makeCosine(time, amplitude, frequency, phase=0):
    """
    This function is for creating cosine wave of varying time, amplitude, freq,
    and phase for simulating input signals

    :param int time: time in seconds for cosine curve
    :param int amplitude: amplitude of cosine curve
    :param int frequency: frequency of cosine curve in Hz
    :param int phase: phase of cosine curve in radians
    :return array curve: calculated cosine curve
    """
    from numpy import cos, pi, arange
    t = arange(0, time, 0.01)
    a = amplitude
    f = frequency
    p = phase

    curve = a * cos(2 * pi * f * t + p)
    for p in range(len(curve)):
        curve[p] = round(curve[p], 2)
    return curve


def dotProduct(list1, list2):
    """
    This function determines the dot product of two lists

    :param list list1: input list 1
    :param list list2: input list 2
    :return int dp: calculated dot product (could also be type float)
    """
    # Exit function if lengths are not the same
    if len(list1) != len(list2):
        print("\nBoth input lists must have the same length\n")
        raise IndexError

    # NOTE. This function does not check that both lists only contain numbers
    # but it is expected to work properly

    L = len(list1)
    dp = 0

    for i in range(L):
        dp += list1[i] * list2[i]

    return dp


def multiplex(Fs, signal1, signal2):
    """
    This function multiplexes data from two input signals into one single \
    list, where the first value is sampling frequency and the following \
    values contain the multiplexed values from each signal

    :param int Fs: sampling frequency (in Hz)
    :param list signal1: an input signal
    :param list signal2: an input signal
    :return list mplex: multiplexed signal
    """
    # 1. The length of mplex should be determined first
    # NOTE. It is possible (though not ideal) that one signal is longer than
    # the other...in such a case only values with overlapping indices will be
    # copied to mplex (i.e. shorter length will be used)
    length1 = len(signal1)
    length2 = len(signal2)
    if length1 < length2:
        mplexLen = length1
    else:
        mplexLen = length2

    mplex = [0 for x in range(2 * mplexLen + 1)]  # add one for Fs

    # 2. Set Fs
    mplex[0] = Fs

    # 3. Multiplexing Time!
    i = 1  # mplex index counter
    for m in range(mplexLen):
        mplex[i] = signal1[m]
        i += 1
        mplex[i] = signal2[m]
        i += 1

    return mplex


logDict = {"DEBUG": 10,
           "INFO": 20,
           "WARNING": 30,
           "ERROR": 40,
           "CRITICAL": 50}
