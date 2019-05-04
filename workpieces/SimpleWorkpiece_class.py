from option_queries import *

class SimpleWorkpiece(object):
    name = 'Simple Workpiece'
    option_query_classes = [
        StockLengthQuery,
        StockWidthQuery,
        StockHeightQuery
    ]

    def __init__(self):
        self.option_queries = {}

    def getOptionQueries(self):
        if len(self.option_queries.keys()) == 0:
            self.option_queries = { key: key() for key in self.option_query_classes }
        return self.option_queries

    def getParams(self):
        params = {
            'stock_length': self.option_queries[StockLengthQuery].getValue(),
            'stock_width': self.option_queries[StockWidthQuery].getValue(),
            'stock_height': self.option_queries[StockHeightQuery].getValue()
        }
        return params
