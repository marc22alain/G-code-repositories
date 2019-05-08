class GCodeParser(object):
    def __init__(self):
        self.x_pos = 0
        self.y_pos = 0
        self.z_pos = 0
        self.program = None
        self.program_errors = {}
        self.abs_incr_mode = 'abs'  # choosing a default value

    def resetProgram(self, program):
        self.program = program
        self.program_errors = {}
        self.abs_incr_mode = 'abs'

    def getProgramData(self):
        return {
            'program_errors': self.program_errors,
            'ending_x_pos': self.x_pos,
            'ending_y_pos': self.y_pos,
            'ending_z_pos': self.z_pos,
        }

    def parseProgram(self):
        current_line = 0
        for line in self.program:
            current_line += 1
            try:
                self._parseLine(line)
            except Exception as e:
                self.program_errors[current_line] = e

    def _parseLine(self, line):
        # go into FSM mode
        tokens = line.split(' ')
        while len(tokens) > 0:
            token = tokens.pop(0)
            # print 'processing: %s' % (token)
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
                while tokens[0][0] in ['X', 'Y', 'Z']:
                    linear.append(token.pop(0))
                self.processLinear(linear)
                continue
            if token in ['G2', 'G3']:
                circular = [token]
                while tokens[0][0] in ['X', 'Y', 'Z', 'I', 'J', 'P']:
                    circular.append(token.pop(0))
                self.processcircular(circular)
                continue
            raise ValueError('token "%s" has no parser defined yet' % token)

