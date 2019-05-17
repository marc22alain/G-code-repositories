from option_queries import *
from utilities import Glib as G

class SimpleMachine(object):
    name = 'Simple Machine'
    option_query_classes = [
        BitDiameterQuery,
        SafeZQuery,
        FeedRateQuery
    ]

    def __init__(self):
        self.option_queries = {}
        self.mode = None

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
