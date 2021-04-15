from GCodeParser_class import GCodeParser
from SimMachine_class import SimMachine
from utilities import MC

default_machine_params = {
    'bit_diameter': MC.default_bit,
    'feed_rate': MC.default_feed_rate,
    'safe_z': MC.default_safe_Z
}

class PostProcessor(object):
    def __init__(self, machine_params=default_machine_params):
        self.sim_machine = SimMachine(machine_params)
        self.parser = GCodeParser(self.sim_machine)

    def setProgram(self, program):
        self.parser.setProgram(program.split('\n'))
        self.sim_machine.reset()

    def parseProgram(self):
        self.parser.parseProgram()

    def getProgramData(self):
        results = {}
        results.update(self.sim_machine.getMachineState())
        results.update(self.parser.getProgramData())
        return results

    def process(self, gcode):
        self.setProgram(gcode)
        self.parseProgram()
        return gcode
