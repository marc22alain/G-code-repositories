from FeatureDrawing_class import FeatureDrawing
from GrooveDrawing_class import GrooveDrawing
from observeder import AutoObserver
from drawn_entities import Circle, Rectangle
from errors import *

# used by CircularGroove, ODCircularGroove
class CircularGrooveDrawing(FeatureDrawing, GrooveDrawing, AutoObserver):

    def __init__(self):
        AutoObserver.__init__(self)
        FeatureDrawing.__init__(self)

    def _drawXYentities(self):
        plane = 'XY'
        options = {"tag":"geometry","outline":"yellow","fill":None}
        refX = self.params['refX']
        refY = self.params['refY']
        radius = self.params['diameter'] /2
        inner_adj, outer_adj = self.getAdjustments()
        if len(self.entities[plane]) == 0:
            self.entities[plane].append(Circle(self.view_space))
            self.entities[plane].append(Circle(self.view_space))
        self.entities[plane][0].setAllByCenterRadius((refX, refY, radius + inner_adj), options).draw()
        self.entities[plane][1].setAllByCenterRadius((refX, refY, radius + outer_adj), options).draw()

    def _drawYZentities(self):
        plane = 'YZ'
        options = {"tag":"geometry","outline":"yellow","fill":None}
        cut_depth = self.params['cut_depth']
        refY = self.params['refY']
        radius = self.params['diameter'] /2
        stock_height = self.params['stock_height']
        inner_adj, outer_adj = self.getAdjustments()
        if len(self.entities[plane]) == 0:
            self.entities[plane].append(Rectangle(self.view_space))
            self.entities[plane].append(Rectangle(self.view_space))
        self.entities[plane][0].setAll(
            (refY - radius - inner_adj, stock_height - cut_depth, refY + radius + inner_adj, stock_height),
            options
        ).draw()
        self.entities[plane][1].setAll(
            (refY - radius - outer_adj, stock_height - cut_depth, refY + radius + outer_adj, stock_height),
            options
        ).draw()

    def _drawXZentities(self):
        plane = 'XZ'
        options = {"tag":"geometry","outline":"yellow","fill":None}
        cut_depth = self.params['cut_depth']
        refX = self.params['refX']
        radius = self.params['diameter'] /2
        stock_height = self.params['stock_height']
        inner_adj, outer_adj = self.getAdjustments()
        if len(self.entities[plane]) == 0:
            self.entities[plane].append(Rectangle(self.view_space))
            self.entities[plane].append(Rectangle(self.view_space))
        self.entities[plane][0].setAll(
            (refX - radius - inner_adj, stock_height - cut_depth, refX + radius + inner_adj, stock_height),
            options
        ).draw()
        self.entities[plane][1].setAll(
            (refX - radius - outer_adj, stock_height - cut_depth, refX + radius + outer_adj, stock_height),
            options
        ).draw()
