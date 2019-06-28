from FeatureDrawing_class import FeatureDrawing
from observeder import AutoObserver
from drawn_entities import Circle, Rectangle
from utilities import log

# used by Peck and CircularPocket
class HoleDrawing(FeatureDrawing, AutoObserver):

    def __init__(self):
        AutoObserver.__init__(self)
        FeatureDrawing.__init__(self)
        log('HoleDrawing __init__')

    def _drawXYentities(self):
        plane = 'XY'
        options = {"tag":"geometry","outline":"yellow","fill":None}
        cut_depth = self.params['cut_depth']
        refX = self.params['refX']
        refY = self.params['refY']
        radius = self.params['diameter'] /2
        if len(self.entities[plane]) == 0:
            self.entities[plane].append(Circle(self.view_space))
        self.entities[plane][0].setAllByCenterRadius((refX, refY, radius), options).draw()

    def _drawYZentities(self):
        plane = 'YZ'
        options = {"tag":"geometry","outline":"yellow","fill":None}
        cut_depth = self.params['cut_depth']
        refY = self.params['refY']
        radius = self.params['diameter'] /2
        stock_height = self.params['stock_height']
        if len(self.entities[plane]) == 0:
            self.entities[plane].append(Rectangle(self.view_space))
        self.entities[plane][0].setAll(
            (refY - radius, stock_height - cut_depth, refY + radius, stock_height),
            options
        ).draw()

    def _drawXZentities(self):
        plane = 'XZ'
        options = {"tag":"geometry","outline":"yellow","fill":None}
        cut_depth = self.params['cut_depth']
        refX = self.params['refX']
        radius = self.params['diameter'] /2
        stock_height = self.params['stock_height']
        if len(self.entities[plane]) == 0:
            self.entities[plane].append(Rectangle(self.view_space))
        self.entities[plane][0].setAll(
            (refX - radius, stock_height - cut_depth, refX + radius, stock_height),
            options
        ).draw()
