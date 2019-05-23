from option_queries import *
from drawn_entities import Rectangle

class SimpleWorkpiece(object):
    name = 'Simple Workpiece'
    option_query_classes = [
        StockLengthQuery,
        StockWidthQuery,
        StockHeightQuery
    ]

    def __init__(self, feature_manager, view_space):
        self.option_queries = {}
        self.feature_manager = feature_manager
        self.view_space = view_space
        self.entities = []

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

    def drawGeometry(self):
        options = {"tag":"geometry","outline":"cyan","fill":None}
        params = self.getParams()
        height = params['stock_height']
        length = params['stock_length']
        width = params['stock_width']
        if length > 0 and width > 0:
            self.setExtents()
            if len(self.entities) == 0:
                self.entities.append(Rectangle(self.view_space).setParams((0, 0, length, width), options).draw())
            else:
                self.entities[0].setParams((0, 0, length, width), options).draw()

    def setExtents(self):
        params = self.getParams()
        height = params['stock_height']
        length = params['stock_length']
        width = params['stock_width']
        view_init = { "view_plane": "XY", \
                  "extents": {"width": length, "height": width, "center": (length / 2, width / 2)}}
        self.view_space.setExtents(view_init)
        self.feature_manager.reDrawAll()

