import inspect
from DepthSteppingFeature_class import DepthSteppingFeature
from ODCircularGroove_class import ODCircularGroove
from option_queries import PathDiameterQuery, CutDepthQuery, ReferenceXQuery, ReferenceYQuery
from drawn_features import HoleDrawing
from utilities import addDebug, log, Glib as G


class CircularPocket(DepthSteppingFeature):
    """The CircularPocket reference point is the center of the circle."""
    name = 'Circular Pocket'
    user_selectable = True
    option_query_classes = [
        PathDiameterQuery
    ]

    child_feature_classes = [
        ODCircularGroove,
    ]

    def _getInstructions(self, sequence):
        file_text = addDebug(inspect.currentframe())
        params = self.getParams()
        diameter = params['diameter']
        current_od = params['bit_diameter']
        od_feature = self.child_features[ODCircularGroove]
        while current_od < diameter:
            # increase current_od
            starting_od = current_od
            current_od = min(
                current_od + (2 * (params['bit_diameter'] - self.getOverlap())),
                diameter
            )
            file_text += self.machine.setMode('INCR')
            file_text += G.G1_XY((- (current_od - starting_od) / 2, 0))
            self.setUpODcircularGroove(current_od)
            file_text += od_feature.getGCode()
            file_text += addDebug(inspect.currentframe())
        if sequence not in ['last', 'only']:
            # returns to center of pocket
            file_text += od_feature.returnToHome()
        return file_text


    def moveToStart(self):
        return ''

    def returnToHome(self):
        """Called after the last depth step in the pocket has been cut."""
        od_feature = self.child_features[ODCircularGroove]
        file_text = addDebug(inspect.currentframe())
        file_text += od_feature.returnToHome()
        return file_text

    def setUpODcircularGroove(self, od):
        """Sets up the ODCircularGroove to perform the cutting operations."""
        circ_groove_child = self.child_features[ODCircularGroove]
        circ_groove_child.option_queries[PathDiameterQuery].setValue(od)
        circ_groove_child.self_managed_depth = False


    def getParams(self):
        basic_params = self.getBasicParams()
        basic_params.update({
            'cut_depth': self.option_queries[CutDepthQuery].getValue(),
            'diameter': self.option_queries[PathDiameterQuery].getValue(),
            'ref_X': self.option_queries[ReferenceXQuery].getValue(),
            'ref_Y': self.option_queries[ReferenceYQuery].getValue()
        })
        return basic_params

    def getOverlap(self):
        """Returns a figure that determines the overlap between adjacent cuts that
        form the pocket.
        TBD, but probably based on a constant to begin with.
        Unit is mm of course."""
        return 0.5

    def _makeDrawingClass(self):
        log('CircularPocket makeDrawingClass')
        class Anon(HoleDrawing):
            params = self.getParams()
            observable = self
            view_space = self.view_space
        return Anon
