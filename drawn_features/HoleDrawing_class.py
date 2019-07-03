from FeatureDrawing_class import FeatureDrawing
from observeder import AutoObserver
from drawn_entities import Circle, Rectangle
from utilities import log

# used by Peck and CircularPocket
class HoleDrawing(FeatureDrawing, AutoObserver):
    """Draws holes."""
    def __init__(self):
        AutoObserver.__init__(self)
        FeatureDrawing.__init__(self)
        log('HoleDrawing __init__')

    def _drawXYentities(self):
        plane = 'XY'
        options = {"tag":"geometry", "outline":"yellow", "fill":None}
        ref_X = self.params['ref_X']
        ref_Y = self.params['ref_Y']
        radius = self.params['diameter'] /2
        if not self.entities[plane]:
            self.entities[plane].append(Circle(self.view_space))
        self.entities[plane][0].setAllByCenterRadius((ref_X, ref_Y, radius), options).draw()

    def _drawYZentities(self):
        plane = 'YZ'
        options = {"tag":"geometry", "outline":"yellow", "fill":None}
        cut_depth = self.params['cut_depth']
        ref_Y = self.params['ref_Y']
        radius = self.params['diameter'] /2
        stock_height = self.params['stock_height']
        if not self.entities[plane]:
            self.entities[plane].append(Rectangle(self.view_space))
        self.entities[plane][0].setAll(
            (ref_Y - radius, stock_height - cut_depth, ref_Y + radius, stock_height),
            options
        ).draw()

    def _drawXZentities(self):
        plane = 'XZ'
        options = {"tag":"geometry", "outline":"yellow", "fill":None}
        cut_depth = self.params['cut_depth']
        ref_X = self.params['ref_X']
        radius = self.params['diameter'] /2
        stock_height = self.params['stock_height']
        if not self.entities[plane]:
            self.entities[plane].append(Rectangle(self.view_space))
        self.entities[plane][0].setAll(
            (ref_X - radius, stock_height - cut_depth, ref_X + radius, stock_height),
            options
        ).draw()
