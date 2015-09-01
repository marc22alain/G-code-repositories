def cutter_comment(cutter):
    return '% cutter diameter is ' + str(cutter) + 'mm \n'


def cut_closed_lines(points):
    '''function that assumes the coords are already offset for cutter R'''
    file_text = Z_safe
    file_text += G0_to(points[0])
    Z_now = stock_thick
    file_text += G0_Z(Z_now)
    while Z_now > 0:
        Z_now -= max_cut
        if Z_now < 0:
            Z_now = 0
        file_text += G1_Z(Z_now)
        for i in range(1, len(points)):
            file_text += G1_to(points[i])
        file_text += G1_to(points[0])
    file_text += Z_safe
    return file_text


def cut_circle(center, diam):
    '''cuts in XY, moves safely and retrieves bit; cutting in steps to bottom'''
    file_text = Z_safe
    file_text += G0_to((center[0] + diam - cutter_rad, center[1]))
    Z_now = stock_thick
    file_text += G0_Z(Z_now)
    while Z_now > 0:
        Z_now -= max_cut
        if Z_now < 0:
            Z_now = 0
        file_text += G1_Z(Z_now)
        file_text += 'G17 G2 X' + str(center[0] + diam - cutter_rad) + ' Y' + \
                    str(center[1]) + ' I' + str(center[0]) + ' J' + \
                    str(center[1]) + ' \n'
    file_text += Z_safe
    return file_text

def drill(point):
    '''drills a hole the size of the bit; safe moves''' 
    file_text = Z_safe
    file_text += G0_to(point)
    file_text += G0_Z(stock_thick)
    file_text += G1_Z(0)
    file_text += Z_safe
    return file_text


def feed_rate(rate):
    '''this exists to modify the feed rate in mid-program'''
    return 'F' + str(rate) + ' \n'

def drill_down():
    '''this leaves the bit at the bottom of the through hole'''
    file_text = G0_Z(stock_thick)
    file_text += G1_Z(0)
    return file_text

def bore_hole(center, diam):
    '''use G12; from specified center diameter::cutter compensation in function
    uses default stock thickness and default cutter'''
    off_set = (diam / 2) - cutter_rad
    file_text = Z_safe
    file_text += G0_to(center)
    Z_now = stock_thick
    file_text += G0_Z(Z_now)
    while Z_now > 0:
        Z_now -= max_cut
        if Z_now < 0:
            Z_now = 0
        file_text += G1_Z(Z_now)
        file_text += 'G12 I' + str(off_set) + ' \n'
    file_text += 'G4 P0.5\n'
    file_text += Z_safe
    return file_text


def round_pocket(diam, cutter, stock_thick, depth):
    '''use G12; from specified diameter, stock height, and depth of cut;
       cutter compensation in function'''
    off_set = (diam - cutter) / 2
    file_text = cutter_comment(cutter)
    file_text += G0_Z(stock_thick)
    cut_pos = stock_thick
    while cut_pos > stock_thick - depth:
        cut_pos -= max_cut
        if cut_pos < stock_thick - depth:
            cut_pos = stock_thick - depth
        file_text += G1_Z(cut_pos)
        file_text += 'G12 I' + str(off_set) + ' \n' 
    file_text += Z_safe
    return file_text
    


def arc_path(arc_ends, arc_center, way, side):
    '''TO DO: cuts an arc path using G2/G3; assumes cutter on inside'''
    if side == 'in':
        of_st = -1 * cutter_rad
    else:
        of_st = cutter_rad
    file_text = ''
    file_text = Z_safe
    file_text = G0_to((arc_ends[0][0] + of_st),(arc_ends[0][1] + of_st))
    Z_now = stock_thick
    file_text += G0_Z(Z_now)
    while Z_now > 0:
        Z_now -= max_cut
        if Z_now < 0:
            Z_now = 0
        file_text += G1_Z(Z_now)
        file_text += 'G1 X' + str(in_X) + ' Y' + str(arc_ends[0][1]) \
                 + ' Z' + str(arc_ends[0][2]) + ' \n'
    return file_text


def off_set(off_set, point):
    '''returns an off set point (X,Y tuple) by a vector (X,Y tuple)'''
    return (point[0] + off_set[0], point[1] + off_set[1])


def rect_hole(start, size, cutter, stock_thick):
    '''
    takes... start: tuple, size: tuple, cutter: float, stock_thick: float;
    cuts a rectangular THRU hole at starting corner point (X,Y) with + size
    (X,Y), compensates for cutter diameter, from reference point of stock
    thickness; depth-of-cut step is default'''
    cut_R = cutter / 2
    path_strt = off_set(start, (cut_R, cut_R))
    corners = (off_set((size[0]-cutter, 0), path_strt), \
               off_set((size[0]-cutter, size[1]-cutter), path_strt), \
               off_set((0, size[1]-cutter), path_strt), \
               off_set((0, 0), path_strt),)
    file_text = Z_safe  # move to SAFE
    file_text += G0_to(path_strt)  # move to SAFE
    file_text += G0_Z(stock_thick)  # move to SAFE
    while stock_thick > 0:
        stock_thick -= max_cut
        if stock_thick < 0:
            stock_thick = 0
        file_text += G1_Z(stock_thick)
        for c in corners:
            file_text += G1_to(c)
    file_text += Z_safe  # move to SAFE
    return file_text


def rect_hole_safe(start, size, cutter, stock_thick):
        '''
    takes... start: tuple, size: tuple, cutter: float, stock_thick: float;
    cuts a rectangular THRU hole at starting corner point (X,Y) with + size
    (X,Y), compensates for cutter diameter, from reference point of stock
    thickness; depth-of-cut step is default'''
    cut_R = cutter / 2
    # off set the path start !!! assuming that start is the left-bottom corner
    path_strt = off_set(start, (cut_R, cut_R))
    file_text = Z_safe  # move to SAFE
    file_text += G0_to(path_strt)  # move to SAFE
    file_text += G0_Z(stock_thick)  # move to SAFE
    file_text += Set_XY_zero  # set temporary coordinate system

    # routine for cuttng THRU
    while stock_thick > 0:
        stock_thick -= max_cut
        if stock_thick < 0:
            stock_thick = 0
        # adjust one more step down
        file_text += G1_Z(stock_thick)
        # core function call
        file_text += _rect_hole_basic(size, cutter)
    
    file_text += Set_XY_abs  # return to absolute coordinate system
    file_text += Z_safe  # move to SAFE
    return file_text


def _rect_hole_basic(size, cutter):
    '''
    takes a tuple and a float, returns a string;
    cuts a rectangular profile with size (X,Y); compensates for cutter
    diameter'''
    cut_R = cutter / 2
    corners = ((size[0]-cutter, 0), \
               (size[0]-cutter, size[1]-cutter), \
               (0, size[1]-cutter), \
               (0, 0))
    file_text = ''
    for c in corners:
        file_text += G1_to(c)
    return file_text

        
def rect_pocket(start, size, cutter, stock_thick):
    '''
    takes... start: tuple, size: tuple, cutter: float, stock_thick: float;
    cuts a BLIND rectangular pocket from starting corner point (X,Y) with
    size (X,Y,Z), compensates for cutter diameter, (? from reference
    point of stock thickness ?); depth-of-cut step is default'''
    # OPTIONS: spiral; zig-zag in X; zig-zag in Y (fastest)
    
    # set envelope parameter
    cut_R = cutter / 2
    file_text = cutter_comment(cutter)
    # off set the path start !!! assuming that start is the left-bottom corner
    path_strt = off_set(start, (cut_R, cut_R))
    file_text += Z_safe  # move to SAFE
    file_text += G0_to(path_strt)  # move to corner
    file_text += G0_Z(stock_thick)  # move to stock
    file_text += Set_XY_zero  # set temporary coordinate system
    Z_pos = stock_thick

    # within routine for repeating to full depth of cut:
    while Z_pos > stock_thick - size[2]:
        Z_pos -= max_cut
        if Z_pos < stock_thick - size[2]:
            Z_pos = stock_thick - size[2]
        # adjust one more step down
        file_text += G1_Z(Z_pos)
        # call the outline cutting function
        file_text += _rect_hole_basic(size, cutter)
        
        # TO DO: now call the ZIG-ZAG routine
        X_pos = cutter
        dir_Y = 1
        while X_pos < size[0] - cutter:
            if X_pos > size[0] - cutter:
                X_pos = size[0] - cutter  # will overlap by definition; more ?
            file_text += G1_X(X_pos - def_overlap)  # added some overlap
            # TO DO: last bit for Y
            if dir_Y == 1:
                file_text += G1_Y(size[1] - 3 * cut_R)  # avoids burning side
            else:
                file_text += G1_Y(2 * cut_R - def_overlap)  # added some overlap
            dir_Y *= -1
            X_pos += cutter
        file_text += G0_to((0,0)) 
    
    file_text += Set_XY_abs  # return to absolute coordinate system
    file_text += Z_safe  # move to SAFE
    return file_text


def rect_from_center(start, size, cutter, stock_thick):
    '''
    takes... start: tuple, size: tuple, cutter: float, stock_thick: float;
    start is the center point'''
    corner = off_set((-size[0] / 2, -size[1] / 2), start)
    return rect_pocket(corner, size, cutter, stock_thick)
"""
PLACEHOLDER file ONLY
"""

def plane_X(start, area_Z, cutter):
    '''
    takes... start: tuple, area_Z: tuple, cutter: float;
    point control; (X,Y,Z) tuples; grain along X; no overlap
    as you'll be sanding anyway'''
    file_text = Z_safe
    file_text += G0_to(start)
    dir_X = 1
    Y_pos = start[1]
    Z_pos = start[2]
    # routine for shifting depth in steps
    while Z_pos > area_Z[2]:
        Z_pos -= max_cut
        if Z_pos < area_Z[2]:
            Z_pos = area_Z[2]
        file_text += G1_Z(Z_pos)
        # routine for shifting across the planed surface
        while True:
##        while Y_pos + cutter / 2 < area_Z[1]:
            if dir_X == 1:
                file_text += G1_X(start[0] + area_Z[0])
            else:
                file_text += G1_X(start[0])
            dir_X *= -1
            if Y_pos + cutter / 2 > area_Z[1]:
                break
            Y_pos += cutter
            file_text += G1_Y(Y_pos)
    file_text += Z_safe
    return file_text

    
def angle_plane(start, area_Z, angle, cutter):
    '''
    takes... start: tuple, area_Z: tuple, angle: float, cutter: float;
    more general planing function'''
    pass
