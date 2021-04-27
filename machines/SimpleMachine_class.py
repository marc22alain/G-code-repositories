from option_queries import BitDiameterQuery, FeedRateQuery, QueryManager, SafeZQuery
from utilities import Glib as G
import re

class SimpleMachine(QueryManager):
    name = 'Simple Machine'
    option_query_classes = [
        BitDiameterQuery,
        SafeZQuery,
        FeedRateQuery
    ]

    int_p = re.compile(r'(-*\d+)')
    float_p = re.compile(r'(-*\d+\.\d+)')

    def __init__(self, feature_manager=None):
        QueryManager.__init__(self)
        self.params = None
        self.feature_manager = feature_manager
        self.mode = None
        self.z_pos = None
        # to auto-initialize itself to default values
        # ... all of its option queries have defaults
        self.getOptionQueries()

    def getParams(self):
        params = {
            'bit_diameter': self.option_queries[BitDiameterQuery].getValue(),
            'safe_z': self.option_queries[SafeZQuery].getValue(),
            'feed_rate': self.option_queries[FeedRateQuery].getValue()
        }
        return params

    def setMode(self, mode):
        file_text = ''
        if mode.lower() == 'abs':
            if self.mode != 'abs':
                self.mode = 'abs'
                file_text = G.set_ABS_mode()
        elif mode.lower() == 'incr':
            if self.mode != 'incr':
                self.mode = 'incr'
                file_text = G.set_INCR_mode()
        else:
            raise ValueError('"%s" mode is not handled by SimpleMachine' % (mode))
        return file_text

    def setUpProgram(self):
        feed_rate = self.option_queries[FeedRateQuery].getValue()
        file_text = G.F_rate(feed_rate)
        return file_text

    def endProgram(self):
        file_text = self.setMode('ABS')
        file_text += G.end_program()
        return file_text

    def postQueryUpdateHook(self):
        if self.feature_manager:
            self.feature_manager.reDrawAll()
        self.params = self.getParams()

    def registerFeatureManager(self, feature_manager):
        """Add a feature manager as instance prop, and do other stuff as
        required."""
        self.feature_manager = feature_manager

    def getRepresentationForCollection(self):
        """Creates a dict representation of the FeatureManager's composition."""
        return self.getOptionQueryValues()

    def moveToSafeZ(self):
        if self.params is None:
            self.params = self.getParams()
        if self.z_pos == self.params['safe_z']:
            return ''
        self.z_pos = self.params['safe_z']
        file_text = self.setMode('ABS')
        file_text += G.G0_Z(self.params['safe_z'])
        return file_text

    def updateZ(self, gcode_line):
        # this must be a straight pass-through
        self._parseMoveLine(gcode_line[:])
        return gcode_line

    def _parseMoveLine(self, line):
        # go into FSM mode
        tokens = line.split(' ')
        while len(tokens) > 0:
            token = tokens.pop(0)
            # print 'processing: %s' % (token)
            if token == '':
                break
            if token in ['G0', 'G1']:
                linear = [token]
                while len(tokens) > 0 and tokens[0] != '' and tokens[0][0] in ['X', 'Y', 'Z']:
                    linear.append(tokens.pop(0))
                # TODO: raise an error if there are tokens left
                self._processLinear(linear)
                continue
            if token == '\n':
                continue
            raise ValueError('token "%s" is not expected to updateZ' % token)

    def _processLinear(self, tokens):
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
            if next_num[0] == 'Z':
                if self.mode == 'incr':
                    self.z_pos += num
                else:
                    self.z_pos = num
                if self.z_pos < 0:
                    self.negative_Z = True
                    raise ValueError('move to negative Z')
