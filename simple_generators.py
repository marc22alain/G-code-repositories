"""
A collection of G-code generating functions that support the wizards
accessed in the AXIS GUI.
"""
import Glib as G
import math


def bore_hole(Z_safe, stock_thickness, cut_per_pass, target_depth,
              cutter_diameter, circle_diameter, feed_rate):
# =======
# def bore_hole(Z_safe, stock_thickness, max_cut, cutter_diameter,
#               hole_diameter):
# >>>>>>> master
    '''use G2; from specified diameter and thickness;
       cutter compensation in function.
       Note that this method mixes ABSOLUTE with INCREMENTAL modes:
       all moves in XY are in INCR and all moves in Z are ABS.'''

    assert cutter_diameter <= hole_diameter, "bit is too large for desired hole"
    assert Z_safe > stock_thickness, "Z_safe is too short for stock thickness"

    off_set = (hole_diameter  - cutter_diameter) / 2.0

    file_text = G.set_ABS_mode()
    file_text += G.G0_Z(Z_safe)
    # XY-plane move to starting point
    file_text += G.set_INCR_mode()
    file_text += G.G0_XY((-off_set, 0))
    # Z-axis move to starting point
    file_text += G.set_ABS_mode()
    file_text += G.G0_Z(stock_thickness)
    while stock_thickness > target_depth:
        stock_thickness -= cut_per_pass
        if stock_thickness < target_depth:
            stock_thickness = target_depth
        # Z-axis move 
        file_text += G.set_ABS_mode()
        file_text += G.G1_Z(stock_thickness)
        # XY-plane arc move
        file_text += G.G2XY_to_INCR_FULL((0,0),(off_set, 0))
    # At end of cut, ensures that the program reaches the very bottom
    file_text += G.set_dwell(0.5)
    # Z-axis move
    # TODO: move this to before the return to origin
    file_text += G.set_ABS_mode()
    file_text += G.G0_Z(Z_safe)
    # Then put the bit back to (0,0)
    file_text += G.set_INCR_mode()
    file_text += G.G0_XY((off_set, 0))
    return file_text


def bore_circle_OD(Z_safe, stock_thickness, cut_per_pass, target_depth,
              cutter_diameter, circle_diameter, feed_rate):
    ''' TODO: error check the off-set calculation.'''
    off_set_hole_diam = circle_diameter  + (2 * cutter_diameter)
    return bore_hole(Z_safe, stock_thickness, cut_per_pass, target_depth,
              cutter_diameter,off_set_hole_diam, feed_rate)


def bore_tabbed_ID(Z_safe, stock_thickness, cut_per_pass, target_depth,
              cutter_diameter, circle_diameter, feed_rate, tab_width):
    ''' Cut three tabs.'''
    assert target_depth <= cut_per_pass, "script not set to handle cut_per_pass when it's less than tab thickness"

    off_set = (circle_diameter  - cutter_diameter) / 2
    # NOTE: radius = off_set
    # circumference = math.pi * off_set * 2
    gap_radians = (cutter_diameter + tab_width) / off_set
    file_text = "% cutting bore_tabbed_ID \n"
    file_text += G.G0_Z(Z_safe)

    # XY-plane move to starting point, creating the first tab
    file_text += G.set_INCR_mode()
    file_text += G.G0_XY((-math.cos(gap_radians), \
        math.sin(gap_radians)))
    file_text += G.set_ABS_mode()

    # cut after the first tab
    file_text += G.G1_Z(0)
    file_text += G.G2XY_to_INCR_FULL((math.cos(math.pi / 3), math.sin(math.pi / 3)), \
        (math.cos(gap_radians), -math.sin(gap_radians)))

    # create the second tab
    file_text += G.G0_Z(target_depth)
    file_text += G.G2XY_to_INCR_FULL((math.cos((math.pi / 3) - gap_radians), math.sin((math.pi / 3) - gap_radians)), \
        (- math.cos(math.pi / 3), - math.sin(math.pi / 3)))

    # cut after the second tab
    file_text += G.set_ABS_mode()
    file_text += G.G1_Z(0)
    file_text += G.G2XY_to_INCR_FULL((math.cos((math.pi / 3) - gap_radians), - math.sin((math.pi / 3) - gap_radians), \
        (- math.cos((math.pi / 3) - gap_radians), - math.sin((math.pi / 3) - gap_radians)))

    # create the third tab
    file_text += G.G0_Z(target_depth)
    file_text += G.G2XY_to_INCR_FULL((math.cos(math.pi / 3), - math.sin(math.pi / 3), \
        (- math.cos((math.pi / 3) - gap_radians), math.sin((math.pi / 3) - gap_radians)))

    # cut after the third tab
    file_text += G.set_ABS_mode()
    file_text += G.G1_Z(0)
    file_text += G.G2XY_to_INCR_FULL((math.cos(math.pi - gap_radians), - math.sin(math.pi - gap_radians), \
        (- math.cos(math.pi / 3), math.sin(math.pi / 3)))



    # OPTIONS:
    # - get radius, get sin & cos (of target point ?) to get radians and quadrant
    # for three tabs, need to make 5 point calculations

    file_text += G.set_ABS_mode()
    file_text += G.G0_Z(Z_safe)
    file_text += G.set_INCR_mode()
    file_text += G0_XY((math.cos(gap_radians), math.sin(gap_radians)))
    file_text += G.set_ABS_mode()

    return file_text


def bore_tabbed_OD(Z_safe, stock_thickness, cut_per_pass, target_depth,
              cutter_diameter, circle_diameter, feed_rate, tab_width):
    ''' TODO: leverage the bore_tabbed_ID.'''
    off_set_hole_diam = circle_diameter  + (2 * cutter_diameter)
    file_text = "% cutting bore_tabbed_ID \n"
    return bore_tabbed_OD(Z_safe, stock_thickness, cut_per_pass, target_depth,
              cutter_diameter, off_set_hole_diam, feed_rate, tab_width)


def startProgram(feed_rate):
    return G.F_rate(feed_rate)


def endProgram():
    '''
    Ends the program with an M2
    '''
    return G.set_ABS_mode() + 'M2 \n'