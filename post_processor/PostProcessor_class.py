from ErrorScanner_class import ErrorScanner
from SafeZOptimizer_class import SafeZOptimizer
from utilities import MC

default_machine_params = {
    'bit_diameter': MC.default_bit,
    'feed_rate': MC.default_feed_rate,
    'safe_z': MC.default_safe_Z
}

class PostProcessor(object):
    def __init__(self, machine_params=default_machine_params):
        self.error_scanner = ErrorScanner(machine_params)
        self.safe_z_optimizer = SafeZOptimizer(machine_params)

    def setProgram(self, program):
        self.error_scanner.setProgram(program.split('\n'))
        self.safe_z_optimizer.setProgram(program.split('\n'))

    def parseProgram(self):
        self.error_scanner.parseProgram()
        error_checks = self.getProgramData()['program_errors']
        if len(error_checks):
            print('GOT ERRORS')
            # TODO: some behaviour to warn consuming applications from returning gcode
        else:
            self.safe_z_optimizer.parseProgram()

    def getProgramData(self):
        """
        Collates machine state, errors.
        """
        results = {}
        results.update(self.error_scanner.observable.getMachineState())
        results.update(self.error_scanner.getProgramData())
        results.update({ 'processed_gcode': self.safe_z_optimizer.getOptimizedGCode() })
        return results

    def process(self, gcode):
        self.setProgram(gcode)
        self.parseProgram()
        processed_gcode = self.safe_z_optimizer.getOptimizedGCode()
        return processed_gcode
