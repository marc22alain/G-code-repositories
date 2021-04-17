from observeder import Observable

class SimMachine(Observable):
    def __init__(self, machine_params):
        self.safe_z = machine_params['safe_z']
        self._setProps()
        Observable.__init__(self)

    def reset(self):
        self._setProps()

    def _setProps(self):
        self.x_pos = 0
        self.y_pos = 0
        self.z_pos = 0
        self.feed_rate = None
        self.abs_incr_mode = None
        self.negative_Z = False
        self.at_safe_z = False
        # Default might be 'XY', but I don't want to count on it
        self.selected_plane = None

    def getMachineState(self):
        return {
            'ending_x_pos': self.x_pos,
            'ending_y_pos': self.y_pos,
            'ending_z_pos': self.z_pos,
            'feed_rate': self.feed_rate,
            'ending_mode': self.abs_incr_mode,
            'negative_Z': self.negative_Z,
            'at_safe_z': self.at_safe_z
        }

    def changeMode(self, mode):
        self.abs_incr_mode = mode

    def makeMove(self, move_coords):
        initial_state = {}
        initial_state.update(self.getMachineState())
        state_name = ''
        if self.abs_incr_mode == 'incr':
            if 'X' in move_coords:
                self.x_pos += move_coords['X']
            if 'Y' in move_coords:
                self.y_pos += move_coords['Y']
            if 'Z' in move_coords:
                self.z_pos += move_coords['Z']
        else:
            if 'X' in move_coords:
                self.x_pos = move_coords['X']
            if 'Y' in move_coords:
                self.y_pos = move_coords['Y']
            if 'Z' in move_coords:
                self.z_pos = move_coords['Z']
        #     if self.z_pos < 0:
        #         self.negative_Z = True
        #         raise ValueError('move to negative Z')
        if self.z_pos == self.safe_z and self.at_safe_z == False:
            self.at_safe_z = True
            state_name = 'to-safe-Z'
        elif self.z_pos == self.safe_z and self.at_safe_z == True:
            state_name = 'at-safe-Z'
        elif self.z_pos != self.safe_z and self.at_safe_z == True:
            self.at_safe_z = False
            state_name = 'off-safe-Z'
        else:
            state_name = 'not-safe-Z'

        ending_state = {}
        ending_state.update(self.getMachineState())

        self.notifyObservers('onStateTransition', state_name, { 'initial_state': initial_state, 'ending_state': ending_state,})


    def setFeedRate(self, feed_rate):
        self.feed_rate = feed_rate
