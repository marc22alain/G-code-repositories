import abc
from observeder import AutoObserver
from GCodeParser_class import GCodeParser
from SimMachine_class import SimMachine


class Processor(AutoObserver):
    __metaclass__ = abc.ABCMeta

    def __init__(self, machine_params):
        self.machine_params = machine_params
        sim_machine = SimMachine(machine_params)
        self.observable = sim_machine
        self.gcode_parser = GCodeParser(sim_machine)
        AutoObserver.__init__(self)

    def onStateTransition(self, state_name, states):
        pass

    @abc.abstractmethod
    def setProgram(self, program):
        pass

    @abc.abstractmethod
    def getProgramData(self):
        pass

    @abc.abstractmethod
    def parseProgram(self):
        pass
