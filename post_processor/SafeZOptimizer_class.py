from observeder import AutoObserver
from GCodeParser_class import GCodeParser
from Processor_class import Processor


class SafeZOptimizer(Processor):

    def onStateTransition(self, state_name, states):
        if state_name == 'to-safe-Z':
            # set the starting point, setting (self.total_x = 0,self.total_y = 0)
            pass
        elif state_name == 'at-safe-Z':
            # do what ? ... ignore
            # keep track of additional transit, updating (self.total_x,self.total_y)
            # self.next_line = ''
            pass
        elif state_name == 'off-safe-Z':
            # end the accounting and write the stuff
            # self.next_line = G.G0_XY((self.total_x,self.total_y)) + self.next_line
            pass
        elif state_name == 'not-safe-Z':
            #
            pass
        else:
            raise ValueError('state_name "%s" not handled' % state_name)
        self.next_line = ('(STATE: %s)\n' % state_name) + self.next_line

    def setProgram(self, program):
        self.program_errors = {}
        self.program_ended = False
        self.program = program
        self.optimized_program = ''

    def getProgramData(self):
        return {
            'program_errors': self.program_errors,
            'program_ended': self.gcode_parser.program_ended
        }

    def parseProgram(self):
        current_line = 0
        self.next_line = ''
        for line in self.program:
            self.optimized_program += self.next_line
            self.next_line = line + '\n'
            current_line += 1
            self.gcode_parser._parseLine(line)

    def getOptimizedGCode(self):
        return self.optimized_program + '(optimized)\n'
