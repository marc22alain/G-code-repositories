"""
A collection of G-code generating functions that support the wizards
accessed in the AXIS GUI.
"""
import Glib as G
import math


def bore_circle_ID(Z_safe, stock_thickness, cut_per_pass, target_depth,
              cutter_diameter, circle_diameter):
    '''use G2; from specified diameter and thickness;
       cutter compensation in function.
       Note that this method mixes ABSOLUTE with INCREMENTAL modes:
       all moves in XY are in INCR and all moves in Z are ABS.'''

    assert cutter_diameter <= circle_diameter, "bit is too large for desired hole"
    assert Z_safe > stock_thickness, "Z_safe is too short for stock thickness"

    # alternate path: do a straight drill
    if cutter_diameter == circle_diameter:
        file_text = G.set_ABS_mode()
        file_text += G.G0_Z(stock_thickness)
        file_text += G.G1_Z(target_depth)
        file_text += G.set_dwell(0.5)
        file_text += G.G0_Z(Z_safe)
        return file_text

    off_set = (circle_diameter  - cutter_diameter) / 2.0

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
              cutter_diameter, circle_diameter):
    ''' TODO: error check the off-set calculation.'''
    off_set_hole_diam = circle_diameter  + (2.0 * cutter_diameter)
    return bore_circle_ID(Z_safe, stock_thickness, cut_per_pass, target_depth,
              cutter_diameter, off_set_hole_diam)


def bore_tabbed_ID(Z_safe, stock_thickness, cut_per_pass, tab_thickness,
              cutter_diameter, circle_diameter, tab_width):
    ''' Cut three tabs.'''
    assert tab_thickness <= cut_per_pass, "script not set to handle cut_per_pass when it's less than tab thickness"

    off_set = (circle_diameter  - cutter_diameter) / 2.0
    path_length = math.pi * off_set * 2
    # NOTE: radius = off_set, path_length is circumference of the circle that the cutter will be tracing

    assert path_length > 6.0 * (tab_width + cutter_diameter), "tabs and/or bit are too large for the circle to cut"

    gap_radians = (cutter_diameter + tab_width) / off_set
    # file_text = "% cutting bore_tabbed_ID \n"
    file_text = G.set_ABS_mode()
    file_text += G.G0_Z(Z_safe)

    # XY-plane move to starting point, creating the first tab
    file_text += G.set_INCR_mode()
    x = -math.cos(gap_radians) * off_set;
    y = math.sin(gap_radians) * off_set;
    file_text += G.G0_XY( (x, y) )
    file_text += G.set_ABS_mode()

    # 1 G2 cut after the first tab
    file_text += G.G1_Z(0)
    x = ( math.cos(gap_radians) + math.cos(math.pi / 3.0) ) * off_set
    y = ( - math.sin(gap_radians) + math.sin((2 * math.pi) / 3.0) ) * off_set
    i = math.cos(gap_radians) * off_set
    j = - math.sin(gap_radians) * off_set
    file_text += G.G2XY_to_INCR_FULL( (x, y), (i, j) )

    # 2 G2 create the second tab
    file_text += G.G0_Z(tab_thickness)
    x = (math.cos((math.pi / 3.0) - gap_radians) - math.cos(math.pi / 3.0)) * off_set
    y = (math.sin((math.pi / 3.0) - gap_radians) - math.sin(math.pi / 3.0)) * off_set
    i = - math.cos(math.pi / 3.0) * off_set
    j = - math.sin(math.pi / 3.0) * off_set
    file_text += G.G2XY_to_INCR_FULL( (x, y), (i, j) )

    # 3 G2 cut after the second tab
    file_text += G.set_ABS_mode()
    file_text += G.G1_Z(0)
    x = 0
    y = - 2 * math.sin((math.pi / 3.0) - gap_radians) * off_set
    i = - math.cos((math.pi / 3.0) - gap_radians) * off_set
    j = - math.sin((math.pi / 3.0) - gap_radians) * off_set
    file_text += G.G2XY_to_INCR_FULL( (x, y), (i, j) )

    # 4 G2 create the third tab
    file_text += G.G0_Z(tab_thickness)
    x = - (math.cos((math.pi / 3.0) - gap_radians) - math.cos(math.pi / 3.0)) * off_set
    y = (math.sin((math.pi / 3.0) - gap_radians) - math.sin(math.pi / 3.0)) * off_set
    i = - math.cos((math.pi / 3.0) - gap_radians) * off_set
    j = math.sin((math.pi / 3.0) - gap_radians) * off_set
    file_text += G.G2XY_to_INCR_FULL( (x, y), (i, j) )

    # 5 G2 cut after the third tab
    file_text += G.set_ABS_mode()
    file_text += G.G1_Z(0)
    x = - (1 + math.cos(math.pi / 3.0)) * off_set
    y = math.sin(math.pi / 3.0) * off_set
    i = - math.cos(math.pi / 3.0) * off_set
    j = math.sin(math.pi / 3.0) * off_set
    file_text += G.G2XY_to_INCR_FULL( (x, y), (i, j))

    # return to Z_safe and origin
    file_text += G.set_ABS_mode()
    file_text += G.G0_Z(Z_safe)
    file_text += G.set_INCR_mode()
    file_text += G.G0_XY((off_set, 0))

    return file_text


def bore_tabbed_OD(Z_safe, stock_thickness, cut_per_pass, tab_thickness,
              cutter_diameter, circle_diameter, tab_width):
    off_set_hole_diam = circle_diameter  + (2.0 * cutter_diameter)
    # file_text = "% cutting bore_tabbed_OD \n"
    file_text = bore_tabbed_ID(Z_safe, stock_thickness, cut_per_pass, tab_thickness,
              cutter_diameter, off_set_hole_diam, tab_width)
    return file_text


def polar_holes(Z_safe, stock_thickness, cut_per_pass, target_depth,
              cutter_diameter, circle_diameter, num_holes, hole_circle_diameter):
    assert num_holes > 1, "too few holes to form a circle of holes; must be at least 2"
    file_text = G.set_ABS_mode()
    file_text += G.G0_Z(Z_safe)

    radians_increment = 2 * math.pi / num_holes;

    # drill first hole
    x = math.cos(0) * hole_circle_diameter
    y = math.sin(0) * hole_circle_diameter
    file_text += G.set_INCR_mode()
    file_text += G.G0_XY( (x, y) )
    file_text += bore_circle_ID(Z_safe, stock_thickness, cut_per_pass, target_depth,
              cutter_diameter, circle_diameter)

    # drill all other holes
    for i in xrange(1, int(num_holes)):
        x = - (math.cos((i - 1) * radians_increment) * hole_circle_diameter) + (math.cos(i * radians_increment) * hole_circle_diameter)
        y = - (math.sin((i - 1) * radians_increment) * hole_circle_diameter) + (math.sin(i * radians_increment) * hole_circle_diameter)
        file_text += G.set_INCR_mode()
        file_text += G.G0_XY( (x, y) )
        file_text += bore_circle_ID(Z_safe, stock_thickness, cut_per_pass, target_depth,
                  cutter_diameter, circle_diameter)

    # return to Z_safe and origin
    file_text += G.set_ABS_mode()
    file_text += G.G0_Z(Z_safe)
    file_text += G.set_INCR_mode()
    x = - (math.cos((num_holes - 1) * radians_increment) * hole_circle_diameter)
    y = - (math.sin((num_holes - 1) * radians_increment) * hole_circle_diameter)
    file_text += G.G0_XY( (x, y) )

    return file_text


def startProgram(feed_rate):
    return G.F_rate(feed_rate)


def endProgram():
    '''
    Ends the program with an M2
    '''
    return G.set_ABS_mode() + 'M2 \n'