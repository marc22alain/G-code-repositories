from GCodeParser_class import GCodeParser
from Processor_class import Processor


class ErrorScanner(Processor):

    def setProgram(self, program):
        self.program_errors = {}
        self.program_ended = False
        self.program = program

    def getProgramData(self):
        return {
            'program_errors': self.program_errors,
            'program_ended': self.gcode_parser.program_ended
        }

    def parseProgram(self):
        current_line = 0
        for line in self.program:
            current_line += 1
            try:
                self.gcode_parser._parseLine(line)
            except Exception as e:
                print(e.args)
                self.program_errors[current_line] = {
                    'error': e,
                    'line': line
                }
