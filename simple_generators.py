"""
A collection of G-code generating functions that support the wizards
accessed in the AXIS GUI.

BONUS!
Can also call these from the command line to save programs, like so:
:$ python -c 'from simple_generators import *; print rectArea((200,220),19.05)' >> plane_200x220x19.05.ngc
... but this does leave out important lines such as feed rate and program end.

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

    # gap_radians is the gap (in radians) between the start and stop of each pair of cuts
    gap_radians = (cutter_diameter + tab_width) / off_set
    # file_text = "% cutting bore_tabbed_ID \n"
    file_text = G.set_ABS_mode()
    file_text += G.G0_Z(Z_safe)

    # XY-plane move to starting point, creating the first tab
    # at approximately 180 degrees
    file_text += G.set_INCR_mode()
    x = -math.cos(gap_radians) * off_set
    y = math.sin(gap_radians) * off_set
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
    # at approximately 60 degrees
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

    hole_circle_radius = hole_circle_diameter / 2.0

    file_text = G.set_ABS_mode()
    file_text += G.G0_Z(Z_safe)

    radians_increment = 2 * math.pi / num_holes;

    # drill first hole
    x = math.cos(0) * hole_circle_radius
    y = math.sin(0) * hole_circle_radius
    file_text += G.set_INCR_mode()
    file_text += G.G0_XY( (x, y) )
    file_text += bore_circle_ID(Z_safe, stock_thickness, cut_per_pass, target_depth,
              cutter_diameter, circle_diameter)

    # drill all other holes
    for i in xrange(1, int(num_holes)):
        x = - (math.cos((i - 1) * radians_increment) * hole_circle_radius) + (math.cos(i * radians_increment) * hole_circle_radius)
        y = - (math.sin((i - 1) * radians_increment) * hole_circle_radius) + (math.sin(i * radians_increment) * hole_circle_radius)
        file_text += G.set_INCR_mode()
        file_text += G.G0_XY( (x, y) )
        file_text += bore_circle_ID(Z_safe, stock_thickness, cut_per_pass, target_depth,
                  cutter_diameter, circle_diameter)

    # return to Z_safe and origin
    file_text += G.set_ABS_mode()
    file_text += G.G0_Z(Z_safe)
    file_text += G.set_INCR_mode()
    x = - (math.cos((num_holes - 1) * radians_increment) * hole_circle_radius)
    y = - (math.sin((num_holes - 1) * radians_increment) * hole_circle_radius)
    file_text += G.G0_XY( (x, y) )

    return file_text


def rectArea(area, bit_diameter):
    """ Required arguments: area (as (x=length, y=width), bit_diameter.
    Assumes that the bit is already in the origin corner at required depth of cut.
    """
    length, width = area
    if bit_diameter > length or bit_diameter > width:
        raise ValueError("Bit is too large to cut specified area")
    file_text = G.set_INCR_mode()
    # magic number 0.5 is the pass-to-pass overlap
    pass_width = bit_diameter - 0.5
    current_x = 0

    # first pass
    file_text += G.G1_Y(width - bit_diameter)

    # sentinel to track the pass direction; out is opposite to back, and the
    # bit is now ready to come back
    out = False
    while current_x < (length - bit_diameter):
        # prepare for the next pass
        # current_x = min(current_x + pass_width, length - bit_diameter)
        # file_text += G.G1_X(current_x)

        if current_x + pass_width <= length - bit_diameter:
            file_text += G.G1_X(pass_width)
            current_x = current_x + pass_width
        else:
            file_text += G.G1_X( length - bit_diameter - current_x)
            current_x = length - bit_diameter

        if out == True:
            file_text += G.G1_Y(width - bit_diameter)
        else:
            file_text += G.G1_Y( - (width - bit_diameter) )

        out = not out

    # last move is a return to relative origin
    if out == True:
        # Moves straight back along original side wall
        # file_text += G.G1_XY(( -(length - bit_diameter), 0))
        # Change to: move across to other side, move straight back, then back to origin
        file_text += G.G1_Y(( 0, (width - bit_diameter)))
        file_text += G.G1_X(( -(length - bit_diameter), 0))
        file_text += G.G0_Y(( 0, -(width - bit_diameter)))
    else:
        # Moves diagonally across the cut area
        # file_text += G.G1_XY(( -(length - bit_diameter), -(width - bit_diameter)))
        # Change to: move straight back, then back to origin
        file_text += G.G1_X(( -(length - bit_diameter), 0))
        file_text += G.G0_Y(( 0, -(width - bit_diameter)))

    file_text += G.set_ABS_mode()
    return file_text


def rectAreaByOutline(area, bit_diameter, debug=False):
    """ Required arguments: area (as (x=length, y=width), bit_diameter.
    Assumes that the bit is already in the origin corner at required depth of cut.
    This version just cuts progressively smaller rectangles.
    For fastest progress, orient the largest area dimension with the fastest machine axis.
    """
    length, width = area
    if bit_diameter > length or bit_diameter > width:
        raise ValueError("Bit is too large to cut specified area")
    # magic number 0.5 is the pass-to-pass overlap... not sure that I'll enforce it
    min_overlap = 0.5
    min_passes = min(math.ceil(length / bit_diameter), math.ceil(width / bit_diameter))
    min_passes += min_passes % 2

    x_overlap = max(min_overlap, (((min_passes * bit_diameter) - length) / (min_passes - 1)))
    y_overlap = max(min_overlap, (((min_passes * bit_diameter) - width) / (min_passes - 1)))

    x_step = bit_diameter - x_overlap
    y_step = bit_diameter - y_overlap

    file_text = G.set_INCR_mode()
    current_x = 0
    current_y = 0

    if debug:
        file_text += "; length: " + str(length) + "\n"
        file_text += "; width: " + str(width) + "\n"
        file_text += "; bit_diameter: " + str(bit_diameter) + "\n"
        file_text += "; min_passes: " + str(min_passes) + "\n"
        file_text += "; x_overlap: " + str(x_overlap) + "\n"
        file_text += "; y_overlap: " + str(y_overlap) + "\n"
        file_text += "; x_step: " + str(x_step) + "\n"
        file_text += "; y_step: " + str(y_step) + "\n"

    file_text += _rectOutline(length, width, bit_diameter)
    min_passes -= 2
    while min_passes > 0:
        file_text += G.G1_XY((x_step, y_step))
        current_x += x_step
        current_y += y_step
        length -= (2 * x_step)
        width -= (2 * y_step)
        file_text += _rectOutline(length, width, bit_diameter)
        min_passes -= 2
    file_text += G.G0_XY((- current_x, - current_y))
    file_text += G.set_ABS_mode()
    return file_text


def _rectOutline(length, width, bit_diameter):
    """ Assumes it's in INCREMENTAL MODE.
    Since length and width arguments are not related to any position.
    The length and width define the outer boundaries of the cut.
    """
    # TODO: consider whether to climb-cut or not.
    # Cut the whole outline of the area, returning to the origin.
    file_text = G.G1_X(length - bit_diameter)
    file_text += G.G1_Y(width - bit_diameter)
    file_text += G.G1_X(-(length - bit_diameter))
    file_text += G.G1_Y(-(width - bit_diameter))
    return file_text

def rectangularPocket(area, target_depth, stock_thickness, safe_Z, cut_per_pass, bit_diameter, debug=False):
    """
    area argument requires tuple (length, width).
    target_depth is an absolute Z coordinate.
    Assumes that the bit is already in the origin corner.
    Origin is (minCornerX + bit_radius, minCornerY + bit_radius)
    """
    file_text = G.set_ABS_mode()
    if debug:
        file_text += "; target_depth: " + str(target_depth) + "\n"
        file_text += "; stock_thickness: " + str(stock_thickness) + "\n"
        file_text += "; cut_per_pass: " + str(cut_per_pass) + "\n"
        file_text += "; bit_diameter: " + str(bit_diameter) + "\n"
    file_text += G.G0_Z(stock_thickness)
    while stock_thickness > target_depth:
        stock_thickness -= cut_per_pass
        if stock_thickness < target_depth:
            stock_thickness = target_depth
        # Z-axis move by ABSOLUTE coords
        file_text += G.set_ABS_mode()
        file_text += G.G1_Z(stock_thickness)
        file_text += rectAreaByOutline(area, bit_diameter)
    file_text += G.G0_Z(safe_Z)
    return file_text

def roundedRectangle(length, width, corner_radius, bit_diameter, path_ref='outside'):
    """ Assumes it's in INCREMENTAL MODE.
    Since length and width arguments are not related to any position.
    With path_ref='outside', the length and width define the outer boundary of the cut.
    With path_ref='center', the length and width define the cut path (centerline of cut) boundary.
    With path_ref='inside', the length and width define the inner boundary of the cut.
    Assumes that the bit is already in a starting position, at least X of least Y edge;
    path_ref is not a consideration.
    """
    bit_radius = bit_diameter / 2.0
    corner_diameter = 2 * corner_radius
    if corner_radius <= 0:
        raise ValueError('corner_radius %d must be greater than 0.' % corner_radius)
    if path_ref is 'outside':
        # TODO: check that corner_radius > bit_radius
        if corner_radius <= bit_radius:
            raise ValueError('corner_radius %d must be greater than bit radius %d.' % (corner_radius, bit_radius))
        center_offset = corner_radius - bit_radius
        file_text = G.G1_X(length - corner_diameter)
        file_text += G.G3XY_to_INCR_FULL((center_offset, center_offset), (0, center_offset))
        file_text += G.G1_Y(width - corner_diameter)
        file_text += G.G3XY_to_INCR_FULL((- center_offset, center_offset), (- center_offset, 0))
        file_text += G.G1_X(- length + corner_diameter)
        file_text += G.G3XY_to_INCR_FULL((- center_offset, - center_offset), (0, - center_offset))
        file_text += G.G1_Y(- width + corner_diameter)
        file_text += G.G3XY_to_INCR_FULL((center_offset, - center_offset), (center_offset, 0))
    elif path_ref is 'center':
        file_text = G.G1_X(length - corner_diameter)
        file_text += G.G3XY_to_INCR_FULL((corner_radius, corner_radius), (0, corner_radius))
        file_text += G.G1_Y(width - corner_diameter)
        file_text += G.G3XY_to_INCR_FULL((- corner_radius, corner_radius), (- corner_radius, 0))
        file_text += G.G1_X(- length + corner_diameter)
        file_text += G.G3XY_to_INCR_FULL((- corner_radius, - corner_radius), (0, - corner_radius))
        file_text += G.G1_Y(- width + corner_diameter)
        file_text += G.G3XY_to_INCR_FULL((corner_radius, - corner_radius), (corner_radius, 0))
    elif path_ref is 'inside':
        center_offset = corner_radius + bit_radius
        file_text = G.G1_X(length - corner_diameter)
        file_text += G.G3XY_to_INCR_FULL((center_offset, center_offset), (0, center_offset))
        file_text += G.G1_Y(width - corner_diameter)
        file_text += G.G3XY_to_INCR_FULL((- center_offset, center_offset), (- center_offset, 0))
        file_text += G.G1_X(- length + corner_diameter)
        file_text += G.G3XY_to_INCR_FULL((- center_offset, - center_offset), (0, - center_offset))
        file_text += G.G1_Y(- width + corner_diameter)
        file_text += G.G3XY_to_INCR_FULL((center_offset, - center_offset), (center_offset, 0))
    else:
        raise ValueError('Invalid path reference specified: %s.' % path_ref)
    return file_text

def tenon(rail, stile, offsets, tenon, mortise_bit_diameter, bit_diameter, safe_Z, cut_per_pass):
    """
    Assumed bit location (center) is at refs origin, at safe_Z, and machine is assumed in ABS mode.
    It is usual that mortise_bit_diameter == bit_diameter.
    Requires:
        rail = (rail_face_width, rail_thickness)
        stile = (stile_face_width, stile_thickness)
        offsets = (offset_from_face, offset_from_end)
        tenon = (length, width, depth)
    """
    # Unpacking the tuples
    rail_face_width, rail_thickness = rail
    stile_face_width, stile_thickness = stile
    offset_from_face, offset_from_end = offsets
    length, width, depth = tenon

    bit_radius = bit_diameter / 2.0
    corner_radius = mortise_bit_diameter / 2.0

    file_text = ''

    # if debug:
    #     file_text += "; target_depth: " + str(target_depth) + "\n"
    #     file_text += "; stock_thickness: " + str(stock_thickness) + "\n"
    #     file_text += "; cut_per_pass: " + str(cut_per_pass) + "\n"
    #     file_text += "; bit_diameter: " + str(bit_diameter) + "\n"

    if (offset_from_face <= bit_diameter) and (offset_from_end <= bit_diameter) and \
        (rail_face_width - offset_from_end - length <= bit_diameter) and \
        (rail_thickness - offset_from_face - width <= bit_diameter):
        file_text += G.set_ABS_mode()
        file_text += G.G0_Z(safe_Z)
        file_text += G.set_INCR_mode()
        file_text += G.G0_X(offset_from_end + corner_radius)
        file_text += G.set_ABS_mode()
        file_text += G.G0_Z(stile_face_width)
        # Making target_depth a reference from machine's Z = 0.
        target_depth = stile_face_width - depth
        while stile_face_width > target_depth:
            stile_face_width -= cut_per_pass
            if stile_face_width < target_depth:
                stile_face_width = target_depth
            # Z-axis move by ABSOLUTE coords
            file_text += G.set_ABS_mode()
            file_text += G.G1_Z(stile_face_width)

            file_text += G.set_INCR_mode()
            file_text += roundedRectangle(length, width, mortise_bit_diameter, bit_diameter, 'inside')
    else:
        file_text = 'Not implemented yet'

    file_text += G.set_ABS_mode()
    file_text += G.G0_Z(safe_Z)
    return file_text

def mortise():
    pass

def startProgram(feed_rate):
    return G.F_rate(feed_rate)


def endProgram():
    '''
    Ends the program with an M2
    '''
    return G.set_ABS_mode() + 'M2 \n'
