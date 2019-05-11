import re

'''
Note the assumptions made here:
- the low-level G-Code tokens are mostly correct:
   . number types are not checked
- capital letters ONLY for all commands and arguments
- offsets words that might be omitted are still supplied
- axis words that might be omitted are still supplied

REF: http://www.linuxcnc.org/docs/html/gcode/g-code.html
'''

class GCodeParser(object):
    int_p = re.compile(r'(-*\d+)')
    float_p = re.compile(r'(-*\d+\.\d+)')

    def __init__(self):
        self._setProps()

    def resetProgram(self, program):
        self._setProps()
        self.program = program

    def _setProps(self):
        self.x_pos = 0
        self.y_pos = 0
        self.z_pos = 0
        self.feed_rate = None
        self.program = None
        self.program_errors = {}
        self.abs_incr_mode = None
        self.program_ended = False
        self.negative_Z = False
        # Default might be 'XY', but I don't want to count on it
        self.selected_plane = None

    def getProgramData(self):
        return {
            'program_errors': self.program_errors,
            'ending_x_pos': self.x_pos,
            'ending_y_pos': self.y_pos,
            'ending_z_pos': self.z_pos,
            'feed_rate': self.feed_rate,
            'ending_mode': self.abs_incr_mode,
            'program_ended': self.program_ended,
            'negative_Z': self.negative_Z
        }

    def parseProgram(self):
        current_line = 0
        for line in self.program:
            current_line += 1
            try:
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
                self.changeMode(token)
                continue
            if token in ['M2']:
                self.endProgram(token)
                continue
            if token[0] == 'F':
                self.setFeedRate(token)
                continue
            if token in ['G0', 'G1']:
                linear = [token]
                while len(tokens) > 0 and tokens[0] != '' and tokens[0][0] in ['X', 'Y', 'Z']:
                    linear.append(tokens.pop(0))
                # TODO: raise an error if there are tokens left
                self.processLinear(linear)
                continue
            if token in ['G2', 'G3']:
                circular = [token]
                # TODO: update to handle radius words 'R', and offset words for other planes
                while len(tokens) > 0 and tokens[0] != '' and tokens[0][0] in ['X', 'Y', 'Z', 'I', 'J', 'P']:
                    circular.append(tokens.pop(0))
                # TODO: raise an error if there are tokens left
                self.processCircular(circular)
                continue
            if token in ['G17', 'G18', 'G19']:
                self.selectPlane(token)
                continue
            if token[0] == '#':
                # this is a comment
                break
            raise ValueError('token "%s" has no parser defined yet' % token)

    def setFeedRate(self, token):
        result = re.search(self.int_p, token)
        if (result == None or result.group(0) == ''):
            raise ValueError('token "%s" is not a valid feed rate' % token)
        self.feed_rate = int(result.group(0))

    def changeMode(self, token):
        modes = {
            'G90': 'abs',
            'G91': 'incr'
        }
        self.abs_incr_mode = modes[token]

    def processLinear(self, tokens):
        # doing nothing with this for the moment
        move_token = tokens.pop(0)
        while len(tokens) > 0:
            next_num = tokens.pop(0)
            if next_num[0] == 'P':
                continue
            result = re.search(self.float_p, next_num)
            if (result == None or result.group(0) == ''):
                raise ValueError('token "%s" is not a valid move' % next_num)
            num = float(result.group(0))
            if next_num[0] == 'X':
                if self.abs_incr_mode == 'incr':
                    self.x_pos += num
                else:
                    self.x_pos = num
            elif next_num[0] == 'Y':
                if self.abs_incr_mode == 'incr':
                    self.y_pos += num
                else:
                    self.y_pos = num
            elif next_num[0] == 'Z':
                if self.abs_incr_mode == 'incr':
                    self.z_pos += num
                else:
                    self.z_pos = num
                if self.z_pos < 0:
                    self.negative_Z = True
                    raise ValueError('move to negative Z')

    def processCircular(self, tokens):
        self._validateOffsetWords(tokens)
        # for center format arcs, can simply submit the tokens to `processLinear()`
        self.processLinear(tokens)
        # radius format arcs will have an 'R' word

    def selectPlane(self, token):
        planes = {
            'G17': 'XY',
            'G18': 'ZX',
            'G19': 'YZ',
            'G17.1': 'UV',
            'G18.1': 'WU',
            'G19.1': 'VW'
        }
        self.selected_plane = planes[token]

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
