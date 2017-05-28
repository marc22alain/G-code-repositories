"""
Glib for python 2, for LinuxCNC
The purpose of this library is simple: provide G-code functions.
"""

def sane(number):
    '''
    Also prevents engineering notation, which LinuxCNC doesn't recognize.
    '''
    return str(round(number, 5))


def G0_XY(point):
    '''
    Takes a tuple, returns a string;
    goes to (X,Y), not Z
    '''
    return 'G0 X' + sane(point[0]) + ' Y' + sane(point[1]) + ' \n'


def G1_XY(point):
    '''
    Takes a tuple, returns a string;
    almost same as above
    '''
    return 'G1 X' + sane(point[0]) + ' Y' + sane(point[1]) + ' \n'


def G1_to_XZ(point):
    '''
    Takes a tuple, returns a string;
    pulls coords from a 3-value tuple...threeple as it were'''
    return 'G1 X' + sane(point[0]) + ' Z' + sane(point[2]) + ' \n'


def G0_X(plane):
    """
    Takes an int, returns a string;
    """
    return 'G0 X' + sane(plane) + ' \n'


def G0_Y(plane):
    """
    Takes an int, returns a string;
    """
    return 'G0 Y' + sane(plane) + ' \n'


def G0_Z(height):
    """
    Takes an int, returns a string;
    """
    return 'G0 Z' + sane(height) + ' \n'


def G1_X(pos):
    """
    Takes an int, returns a string;
    """
    return 'G1 X' + sane(pos) + ' \n'


def G1_Y(pos):
    """
    Takes an int, returns a string;
    """
    return 'G1 Y' + sane(pos) + ' \n'


def G1_Z(height):
    '''
    Takes an int, returns a string;
    '''
    return 'G1 Z' + sane(height) + ' \n'


def G2XY_to_ABS(point, center):
    '''
    Takes two tuples, returns a string.
    Runs in ABSOLUTE IJ mode G2 == CW.
    '''
    return 'G90.1 G17 G2 X' + sane(point[0]) + ' Y' + sane(point[1]) + ' I' + \
           sane(center[0]) + ' J' + sane(center[1]) + ' \n'


def G2XY_to_INCR_FULL(point, center_offset):
    '''
    Takes two tuples, returns a string.
    Assumes INCREMENTAL IJ mode G2 == CW.
    ***Consider taking out the P1 and making the method more general;
        P1 seems to be optional (p.114 of LinuxCNC User Guide).
    '''
    return 'G91 G17 G2 X' + sane(point[0]) + ' Y' + sane(point[1]) + ' I' + \
           sane(center_offset[0]) + ' J' + sane(center_offset[1]) + ' P1 \n'


def G3XY_to(point, center):
    '''
    Takes two tuples, returns a string.
    Runs in ABSOLUTE IJ mode G3 == CWW.
    '''
    return 'G90.1 G17 G3 X' + sane(point[0]) + ' Y' + sane(point[1]) + ' I' + \
           sane(center[0]) + ' J' + sane(center[1]) + ' \n'


def F_rate(rate):
    '''
    Takes an int, returns a string.
    Sets the feed rate.
    '''
    return 'F' + sane(rate) + ' \n'


def set_INCR_mode():
    '''
    Returns a string to set the program to Incremental (IJ) mode. G91.
    '''
    return 'G91 \n'


def set_ABS_mode():
    '''
    Returns a string to set the program to ABSOLUTE (IJ) mode. G90.
    '''
    return 'G90 \n'


def end_program():
    '''
    Returns a string to end the program with M2.
    '''
    return 'M2 \n'


def set_dwell(time):
    '''
    Takes a float representing seconds, returns a string.
    Sets the dwell time. G4.
    '''
    return 'G4 P' + sane(time) + ' \n'
