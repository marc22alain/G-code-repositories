from observeder import AutoObserver

# TODO: turn this into a metaclass
# TODO: subclass for safe-z movements optimization
# TODO: subclass for program error discovery

class Optimizer(AutoObserver):
    def __init__(self, sim_machine, gcode_parser):
        self.observable = sim_machine
        self.gcode_parser = gcode_parser
        AutoObserver.__init__(self)

    def onStateTransition(self, state_name, states):
        print('STATE: %s' % state_name)
        if state_name == 'to-safe-Z':
            # set the starting point
            pass
        elif state_name == 'at-safe-Z':
            # do what ? ... ignore
            pass
        elif state_name == 'off-safe-Z':
            # end the
            pass
        elif state_name == 'not-safe-Z':
            #
            pass
        else:
            raise ValueError('state_name "%s" not handled' % state_name)
