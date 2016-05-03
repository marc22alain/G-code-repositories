"""
A collection of G-code generating functions that support the wizards
accessed in the AXIS GUI.
"""
import Glib as G

def bore_hole(Z_safe, stock_thickness, cut_per_pass, target_depth,
              cutter_diameter, circle_diameter, feed_rate):
    '''use G2; from specified diameter and thickness;
       cutter compensation in function.
       Note that this method mixes ABSOLUTE with INCREMENTAL modes:
       all moves in XY are in INCR and all moves in Z are ABS.'''
    off_set = (circle_diameter  - cutter_diameter) / 2

##    G.set_Z_safe(Z_safe)

    file_text = G.F_rate(feed_rate)
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
    # Then put the bit back to (0,0)
    file_text += G.G0_XY((off_set, 0))
    # Z-axis move
    file_text += G.set_ABS_mode()
    file_text += G.G0_Z(Z_safe)
    return file_text


def bore_circle_OD(Z_safe, stock_thickness, cut_per_pass, target_depth,
              cutter_diameter, circle_diameter, feed_rate):
    ''' TODO: error check the off-set calculation.'''
    off_set_hole_diam = circle_diameter  + (2 * cutter_diameter)
    return bore_hole(Z_safe, stock_thickness, cut_per_pass, target_depth,
              cutter_diameter,off_set_hole_diam, feed_rate)


def bore_tabbed_ID(Z_safe, stock_thickness, cut_per_pass, target_depth,
              cutter_diameter, circle_diameter, feed_rate):
    ''' Cut three tabs.'''
    off_set = (circle_diameter  - cutter_diameter) / 2
    file_text = "% cutting bore_tabbed_ID \n"
    file_text += G.G0_Z(Z_safe)
    return file_text


def bore_tabbed_OD(Z_safe, stock_thickness, cut_per_pass, target_depth,
              cutter_diameter, circle_diameter, feed_rate):
    ''' TODO: leverage the bore_tabbed_ID.'''
    off_set_hole_diam = circle_diameter  + cutter_diameter
    file_text = "% cutting bore_tabbed_ID \n"
    file_text += G.G0_Z(Z_safe)
    return file_text


def endProgram():
    '''
    Ends the program with an M2
    '''
    return 'M2 \n'