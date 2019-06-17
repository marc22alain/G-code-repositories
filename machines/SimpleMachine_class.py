from option_queries import *
from utilities import Glib as G

class SimpleMachine(object):
    name = 'Simple Machine'
    option_query_classes = [
        BitDiameterQuery,
        SafeZQuery,
        FeedRateQuery
    ]

    def __init__(self, feature_manager):
        self.option_queries = {}
        self.feature_manager = feature_manager
        self.mode = None
        # to auto-initialize itself to default values
        # ... all of its option queries have defaults
        self.getOptionQueries()

    def getOptionQueries(self):
        if len(self.option_queries.keys()) == 0:
            self.option_queries = { key: key() for key in self.option_query_classes }
        return self.option_queries

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

    def didUpdateQueries(self):
        for query in self.option_queries.values():
            query.updateValue()
        self.feature_manager.reDrawAll()

