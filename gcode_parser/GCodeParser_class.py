import re

"""
Note the assumptions made here:
- the low-level G-Code tokens are mostly correct:
   . number types are not checked
- capital letters ONLY for all commands and arguments
- offsets words that might be omitted are still supplied
- axis words that might be omitted are still supplied

REF: http://www.linuxcnc.org/docs/html/gcode/g-code.html
"""

class GCodeParser(object):
    int_p = re.compile(r'(-*\d+)')
    float_p = re.compile(r'(-*\d+\.\d+)')

    def __init__(self, processors=[]):
        # self._setProps()
        self.processors = processors

    def resetProgram(self, program):
        self._setProps()
        self.program = program
        for processor in self.processors:
            processor.resetProgram(program)

    def _setProps(self):
        self.program = None
        self.program_errors = {}
        self.program_ended = False
        # Default might be 'XY', but I don't want to count on it
        self.selected_plane = None

    def getProgramData(self):
        data = {
            'parser': {
                'program_errors': self.program_errors,
                'program_ended': self.program_ended
            }
        }
        for processor in self.processors:
            data.update(processor.getProgramData())

        return data

    def parseProgram(self):
        current_line = 0
        for line in self.program:
            current_line += 1
            try:
                self.sendProcessMessage('trackLine', [{ 'current_line': current_line, 'line': line }])
                self._parseLine(line)
            except Exception as e:
                print e.args
                self.program_errors[current_line] = {
                    'error': e,
                    'line': line
                }

    def _parseLine(self, line):
        # go into FSM mode
        tokens = line.split(' ')
        while len(tokens) > 0:
            token = tokens.pop(0)
            # print 'processing: %s' % (token)
            if token == '':
                break
            if token in ['G90', 'G91']:
                self.sendProcessMessage('changeMode', token)
                continue
            if token in ['M2']:
                self.endProgram(token)
                continue
            if token[0] == 'F':
                self.sendProcessMessage('setFeedRate', token)
                continue
            if token in ['G0', 'G1']:
                linear = [token]
                while len(tokens) > 0 and tokens[0] != '' and tokens[0][0] in ['X', 'Y', 'Z']:
                    linear.append(tokens.pop(0))
                # TODO: raise an error if there are tokens left
                # self.processLinear(linear)
                self.sendProcessMessage('processLinear', linear)
                continue
            if token in ['G2', 'G3']:
                circular = [token]
                # TODO: update to handle radius words 'R', and offset words for other planes
                while len(tokens) > 0 and tokens[0] != '' and tokens[0][0] in ['X', 'Y', 'Z', 'I', 'J', 'P']:
                    circular.append(tokens.pop(0))
                # TODO: raise an error if there are tokens left
                self.processCircular(circular)
                continue
            if token == 'G4':
                next_token = tokens.pop(0)
                if not next_token[0] == 'P':
                    raise ValueError('dwell command must have "P" word parameter')
                continue
            if token in ['G17', 'G18', 'G19']:
                self.selectPlane(token)
                continue
            if token[0] in ['#', '(']:
                # this is a comment
                break
            raise ValueError('token "%s" has no parser defined yet' % token)

    def processCircular(self, tokens):
        self._validateOffsetWords(tokens)
        for processor in self.processors:
            processor.processCircular(tokens)

    def _validateOffsetWords(self, tokens):
        if not self.selected_plane:
            raise ValueError('No plane selected for arc')
        valid_offset_words = {
            'XY': 'IJ',
            'ZX': 'IK',
            'YZ': 'JK'
        }
        offset = valid_offset_words[self.selected_plane]
        pattern_string = offset[0] + '.*' + offset[1] + '|' + offset[1] + '.*' + offset[0]
        pattern = re.compile(pattern_string)
        if not pattern.search(''.join(tokens)):
            raise ValueError('Invalid offset words for selected plane')

    def endProgram(self, token):
        # not doing anything with the token at the moment ... may never ?
        self.program_ended = True
        for processor in self.processors:
            processor.endProgram(token)

    def sendProcessMessage(self, method, tokens):
        """Only two arguments will ever get passed.
            the first is a string, the second may or may not be a list."""
        for processor in self.processors:
            processor.process(method, tokens)
