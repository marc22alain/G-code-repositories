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
        stock_Z = params['stock_height']
        stock_X = params['stock_length']
        stock_Y = params['stock_width']
        if stock_X > 0 and stock_Y > 0:
            if self.view_space.view_plane == 'XY':
                extent_X = stock_X
                extent_Y = stock_Y
            elif self.view_space.view_plane == 'YZ':
                extent_X = stock_Y
                extent_Y = stock_Z
            else:
                extent_X = stock_X
                extent_Y = stock_Z

            self.setExtents(extent_X, extent_Y)
            if len(self.entities) == 0:
                self.entities.append(Rectangle(self.view_space).setParams((0, 0, extent_X, extent_Y), options).draw())
            else:
                self.entities[0].setParams((0, 0, extent_X, extent_Y), options).draw()

    def setExtents(self, extent_X, extent_Y):
        view_init = { "view_plane": self.view_space.view_plane, \
                  "extents": {"width": extent_X, "height": extent_Y, "center": (extent_X / 2, extent_Y / 2)}}
        self.view_space.setExtents(view_init)

    def didUpdateQueries(self):
        self.drawGeometry()
        self.feature_manager.reDrawAll()

