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
    # Z-axis move
    file_text += G.set_ABS_mode()
    file_text += G.G0_Z(Z_safe)
    file_text += 'M2 \n'
    print 'cutter_diameter is ', str(cutter_diameter)
    return file_text

def route_line(Z_safe, stock_thickness, max_cut, cutter_diameter,
              start_coords, end_coords, feed_rate):
    file_text = G.F_rate(feed_rate)
    file_text += G.set_ABS_mode()
    file_text += G.G0_Z(Z_safe)
    file_text += G.G0_XY(start_coords)
    file_text += G.G0_Z(stock_thickness)
    odd = True
    while stock_thickness > 0:
        stock_thickness -= max_cut
        if stock_thickness < 0:
            stock_thickness = 0
        # Z-axis move 
        file_text += G.G1_Z(stock_thickness)
        # XY-plane straight move
        if odd is True:
            file_text += G.G1_XY(end_coords)
            odd = False
        else:
            file_text += G.G1_XY(start_coords)
            odd = True

    # Z-axis move
    file_text += G.G0_Z(Z_safe)
    file_text += 'M2 \n'
    print 'cutter_diameter is ', str(cutter_diameter)
    return file_text