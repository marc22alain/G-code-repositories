from FeatureDrawing_class import FeatureDrawing
from GrooveDrawing_class import GrooveDrawing
from observeder import AutoObserver
from drawn_entities import Circle, Rectangle

# used by CircularGroove
class CircularGrooveDrawing(FeatureDrawing, GrooveDrawing, AutoObserver):
    """Draws circular grooves."""
    def __init__(self):
        AutoObserver.__init__(self)
        FeatureDrawing.__init__(self)

    def _drawXYentities(self):
        plane = 'XY'
        options = {"tag":"geometry", "outline":"yellow", "fill":None}
        ref_X = self.params['ref_X']
        ref_Y = self.params['ref_Y']
        radius = self.params['diameter'] /2
        inner_adj, outer_adj = self.getAdjustments()
        if not self.entities[plane]:
            self.entities[plane].append(Circle(self.view_space))
            self.entities[plane].append(Circle(self.view_space))
        self.entities[plane][0].setAllByCenterRadius(
            (ref_X, ref_Y, radius + inner_adj),
            options
        ).draw()
        self.entities[plane][1].setAllByCenterRadius(
            (ref_X, ref_Y, radius + outer_adj),
            options
        ).draw()

    def _drawYZentities(self):
        plane = 'YZ'
        options = {"tag":"geometry", "outline":"yellow", "fill":None}
        cut_depth = self.params['cut_depth']
        ref_Y = self.params['ref_Y']
        radius = self.params['diameter'] /2
        stock_height = self.params['stock_height']
        inner_adj, outer_adj = self.getAdjustments()
        if not self.entities[plane]:
            self.entities[plane].append(Rectangle(self.view_space))
            self.entities[plane].append(Rectangle(self.view_space))
        self.entities[plane][0].setAll(
            (
                ref_Y - radius - inner_adj,
                stock_height - cut_depth,
                ref_Y + radius + inner_adj,
                stock_height
            ),
            options
        ).draw()
        self.entities[plane][1].setAll(
            (
                ref_Y - radius - outer_adj,
                stock_height - cut_depth,
                ref_Y + radius + outer_adj,
                stock_height
            ),
            options
        ).draw()

    def _drawXZentities(self):
        plane = 'XZ'
        options = {"tag":"geometry", "outline":"yellow", "fill":None}
        cut_depth = self.params['cut_depth']
        ref_X = self.params['ref_X']
        radius = self.params['diameter'] /2
        stock_height = self.params['stock_height']
        inner_adj, outer_adj = self.getAdjustments()
        if not self.entities[plane]:
            self.entities[plane].append(Rectangle(self.view_space))
            self.entities[plane].append(Rectangle(self.view_space))
        self.entities[plane][0].setAll(
            (
                ref_X - radius - inner_adj,
                stock_height - cut_depth,
                ref_X + radius + inner_adj,
                stock_height
            ),
            options
        ).draw()
        self.entities[plane][1].setAll(
            (
                ref_X - radius - outer_adj,
                stock_height - cut_depth,
                ref_X + radius + outer_adj,
                stock_height
            ),
            options
        ).draw()
