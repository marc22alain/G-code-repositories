from utilities import addDebugFrame, log, Glib as G
import math

class FingerJointedSplice(object):
    A_order = 1
    B_order = 0

    """docstring for FingerJointedSplice"""
    def __init__(self, m, w, c):
        self.machine_params = m
        self.workpiece_params = w
        self.cutting_params = c

    def getAGCode(self):
        """
        Starts from the corner of the workpiece ... relative 0,0.
        """
        bit_diameter = self.machine_params['bit_diameter']
        bit_radius = bit_diameter / 2
        x_straight_cut = self.getDistribution()['x_straight_cut']
        # This is magic for A: special refs.
        x_starting_ref = x_straight_cut + bit_radius
        y_starting_ref = - bit_radius
        self.startRefs = {
            'x_starting_ref': x_starting_ref,
            'y_starting_ref': y_starting_ref
        }
        # Of course, other magic is the A finger pattern.
        return self._getGCode(self.A_order)

    def cutFingers(self, order_int):
        """
        One full pass.
        Assumes it's already at its starting position in XYZ.
        """
        bit_diameter = self.machine_params['bit_diameter']
        bit_radius = bit_diameter / 2
        distribution = self.getDistribution()
        path_num = 1

        file_text = G.set_INCR_mode()
        file_text += G.G1_XY((0, bit_radius))
        # Start _remCut with bit center at edge of stock.
        file_text += self._remCut()

        while path_num <= distribution['num_fingers']:
            if path_num % 2 == order_int:
                file_text += self._leftwardsPath()
            else:
                file_text += self._rightwardsPath()
            path_num += 1

        file_text += self._remCut()
        file_text += G.G1_XY((0, bit_radius))
        return file_text

    def _remCut(self):
        distribution = self.getDistribution()
        file_text = G.comment(' => _remCut')
        file_text += G.G1_XY((0, distribution['remainder'] / 2))
        return file_text

    def _leftwardsPath(self):
        """
        Each of these paths is the full width of one finger.
        """
        distribution = self.getDistribution()
        finger_width = distribution['finger_width']
        x_straight_cut = distribution['x_straight_cut']
        file_text = G.comment(' => _leftwardsPath')
        file_text += G.G1_XY(( - x_straight_cut, 0))
        file_text += G.G2XY(( - finger_width, finger_width), (0, finger_width))
        return file_text

    def _rightwardsPath(self):
        """
        Each of these paths is the full width of one finger.
        """
        distribution = self.getDistribution()
        finger_width = distribution['finger_width']
        x_straight_cut = distribution['x_straight_cut']
        file_text = G.comment(' => _rightwardsPath')
        file_text += G.G2XY((finger_width, finger_width), (finger_width, 0))
        file_text += G.G1_XY((x_straight_cut, 0))
        return file_text

    def _getGCode(self, order_int):
        file_text = self._startProgram()
        # move to start, at safe-Z, in INCR mode
        file_text += G.set_INCR_mode()
        file_text += G.G0_XY(( \
            self.startRefs['x_starting_ref'], \
            self.startRefs['y_starting_ref'] \
        ))

        height_to_cut = self.workpiece_params['stock_height']

        while height_to_cut > 0:
            # move down to top of stock
            file_text += G.set_ABS_mode()
            file_text += G.G0_Z(height_to_cut)
            # get to cutting height
            height_to_cut = max(height_to_cut - self.cutting_params['cut_per_pass'], 0)
            file_text += G.set_ABS_mode()
            file_text += G.G1_Z(height_to_cut) # could be G0 here, but it's good practice

            # This is other magic for A/B: special order of paths.
            file_text += self.cutFingers(order_int)
            file_text += self.returnToStart(order_int)

        file_text += self.returnToHome()
        file_text += self._endProgram()
        return file_text

    def returnToStart(self, order_int):
        distribution = self.getDistribution()
        stock_span = self.workpiece_params['stock_width'] + self.machine_params['bit_diameter']
        file_text = self.machine.moveToSafeZ()
        file_text += G.set_INCR_mode()
        if distribution['num_fingers'] % 2 == 0:
            file_text += G.G0_XY(( \
                0, \
                - stock_span \
            ))
        else:
            if order_int == 1:
                file_text += G.G0_XY((\
                    - self.cutting_params['finger_depth'], \
                    - stock_span \
                ))
            else:
                file_text += G.G0_XY((\
                    self.cutting_params['finger_depth'], \
                    - stock_span \
                ))
        return file_text

    def returnToHome(self):
        file_text = self.machine.moveToSafeZ()
        file_text += G.set_INCR_mode()
        file_text += G.G0_XY(( \
            - self.startRefs['x_starting_ref'], \
            - self.startRefs['y_starting_ref'], \
        ))
        return file_text

    def getBGCode(self):
        """
        Only required when there is an odd number of finger widths in the stock.
        """
        """
        Starts from the corner of the workpiece ... relative 0,0.
        """
        bit_diameter = self.machine_params['bit_diameter']
        bit_radius = bit_diameter / 2
        x_straight_cut = self.getDistribution()['x_straight_cut']
        # This is magic for B: special refs.
        x_starting_ref = - bit_radius
        y_starting_ref = - bit_radius
        self.startRefs = {
            'x_starting_ref': x_starting_ref,
            'y_starting_ref': y_starting_ref
        }
        # Of course, other magic is the A finger pattern.
        return self._getGCode(self.B_order)

    def getDistribution(self):
        """
        Each path cutting the side of a finger is the more representative proxy
        for the finger width.
        """
        finger_width = self.machine_params['bit_diameter'] - self.cutting_params['fit_factor']
        x_straight_cut = self.cutting_params['finger_depth'] - finger_width
        num_fingers = math.floor(self.workpiece_params['stock_width'] / \
            finger_width)
        remainder = self.workpiece_params['stock_width'] - \
            (num_fingers * finger_width)
        return {
            'num_fingers': num_fingers,
            'remainder': remainder,
            'finger_width': finger_width,
            'x_straight_cut': x_straight_cut
        }


    def _startProgram(self):
        file_text = G.F_rate(self.machine_params['feed_rate'])
        file_text += self.machine.moveToSafeZ()
        return file_text

    def _endProgram(self):
        file_text = self.machine.moveToSafeZ()
        file_text += G.end_program()
        return file_text
