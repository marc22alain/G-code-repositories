from GCodeParser_class import GCodeParser
from SimMachine_class import SimMachine


class PostProcessor(object):
    def __init__(self):
        self.sim_machine = SimMachine()
        self.parser = GCodeParser(self.sim_machine)

    def setProgram(self, program):
        self.parser.setProgram(program)
        self.sim_machine.reset()

    def parseProgram(self):
        self.parser.parseProgram()

    def getProgramData(self):
        results = {}
        results.update(self.sim_machine.getMachineState())
        results.update(self.parser.getProgramData())
        return results

    def process(self, gcode):
        return gcode
