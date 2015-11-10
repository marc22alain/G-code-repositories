"""
A collection of G-code generating functions that support the wizards
accessed in the AXIS GUI.
"""
import Glib as G

def bore_hole(Z_safe, stock_thickness, max_cut, cutter_diameter,
              hole_diameter, feed_rate):
    '''use G2; from specified diameter and thickness;
       cutter compensation in function.
       Note that this method mixes ABSOLUTE with INCREMENTAL modes:
       all moves in XY are in INCR and all moves in Z are ABS.'''
    off_set = (hole_diameter  - cutter_diameter) / 2

##    G.set_Z_safe(Z_safe)

    file_text = G.F_rate(feed_rate)
    file_text += G.G0_Z(Z_safe)
    # XY-plane move to starting point
    file_text += G.set_INCR_mode()
    file_text += G.G0_XY((-off_set, 0))
    # Z-axis move to starting point
    file_text += G.set_ABS_mode()
    file_text += G.G0_Z(stock_thickness)
    while stock_thickness > 0:
        stock_thickness -= max_cut
        if stock_thickness < 0:
            stock_thickness = 0
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

def endProgram():
    '''
    Ends the program with an M2
    '''
    return 'M2 \n'