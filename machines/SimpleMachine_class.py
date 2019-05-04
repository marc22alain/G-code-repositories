from option_queries import *

class SimpleMachine(object):
    name = 'Simple Machine'
    option_query_classes = [
        BitDiameterQuery,
        SafeZQuery,
        FeedRateQuery
    ]

    def __init__(self):
        self.option_queries = {}

    def getOptionQueries(self):
        if len(self.option_queries.keys()) == 0:
            print 'instantiating new Query objects'
            self.option_queries = { key: key() for key in self.option_query_classes }
        return self.option_queries

    def getParams(self):
        params = {
            'bit_diameter': self.option_queries[BitDiameterQuery].getValue(),
            'safe_z': self.option_queries[SafeZQuery].getValue(),
            'feed_rate': self.option_queries[FeedRateQuery].getValue()
        }
        return params
