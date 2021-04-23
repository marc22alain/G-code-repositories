from observeder import AutoObserver
from ErrorScanner_class import ErrorScanner
from GCodeParser_class import GCodeParser
from Processor_class import Processor
from utilities import Glib as G


class SafeZOptimizer(Processor):

    def onStateTransition(self, state_name, states):
        ending_state = states['ending_state']
        self.ending_state = ending_state
        if state_name == 'to-safe-Z':
            # assuming that this always occurs in ABS mode, and there is always
            # an instance of this immediately preceding any reference point moves
            # at safe-z
            self.at_safe_Z_start_state = ending_state
        elif state_name == 'at-safe-Z':
            self.at_safe_Z_interim_state = ending_state
            # annulling movement instructions
            self.next_line = ''
        elif state_name == 'to-ABS-mode-at-safe-Z':
            cached_line = self.next_line
            self.next_line = '(optimized move)\n'
            self.next_line += G.G0_XY((
                self.at_safe_Z_interim_state['ending_x_pos'] - self.at_safe_Z_start_state['ending_x_pos'],
                self.at_safe_Z_interim_state['ending_y_pos'] - self.at_safe_Z_start_state['ending_y_pos']
            ))
            self.next_line += cached_line
            self.at_safe_Z_start_state = None
            self.at_safe_Z_interim_state = None


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
        errors = self.testOptimizedProgram()
        if len(errors) == 0:
            return self.optimized_program + '(with safe-Z optimizations)\n'
        else:
            return errors

    def testOptimizedProgram(self):
        error_scanner = ErrorScanner(self.machine_params)
        error_scanner.setProgram(self.optimized_program.split('\n'))
        error_scanner.parseProgram()
        errors = error_scanner.getProgramData()['program_errors']
        return errors
