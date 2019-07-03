from DepthSteppingFeature_class import DepthSteppingFeature
from utilities import log, Glib as G
from option_queries import CutDepthQuery, ReferenceXQuery, ReferenceYQuery, \
    DeltaXQuery, DeltaYQuery
from drawn_features import RoundEndedRectangleDrawing


class LinearGroove(DepthSteppingFeature):
    """A straight cut, defined by deltas in X, Y, (and later Z), with reference
    point at the starting point.
    Radius of the cutter at the ends of the cut is outside of the defined deltas."""
    name = 'Linear Groove'
    user_selectable = True
    option_query_classes = [
        DeltaXQuery,
        DeltaYQuery
    ]

    child_feature_classes = []

    def __init__(self, feature_manager, view_space, manages_depth=True):
        self.at_start = None
        DepthSteppingFeature.__init__(self, feature_manager, view_space, manages_depth)

    def _getInstructions(self, sequence):
        assert self.at_start is not None, 'moveToStart not yet called'
        params = self.getParams()
        delta_X = params['delta_X']
        delta_Y = params['delta_Y']
        file_text = self.machine.setMode('INCR')
        if self.at_start:
            file_text += G.G1_XY((delta_X, delta_Y))
        else:
            file_text += G.G1_XY((- delta_X, - delta_Y))
        self.at_start = not self.at_start
        return file_text

    def moveToStart(self):
        self.at_start = True
        # for starting point reference point
        file_text = ''
        return file_text

    def returnToHome(self):
        # for starting point reference point
        params = self.getParams()
        delta_X = params['delta_X']
        delta_Y = params['delta_Y']
        file_text = ''
        if not self.at_start:
            file_text = self.machine.setMode('INCR')
            file_text += G.G0_XY((- delta_X, - delta_Y))
            self.at_start = True
        return file_text

    def getParams(self):
        basic_params = self.getBasicParams()
        basic_params.update({
            'cut_depth': self.option_queries[CutDepthQuery].getValue(),
            'ref_X': self.option_queries[ReferenceXQuery].getValue(),
            'ref_Y': self.option_queries[ReferenceYQuery].getValue(),
            'delta_X': self.option_queries[DeltaXQuery].getValue(),
            'delta_Y': self.option_queries[DeltaYQuery].getValue()
        })
        return basic_params

    def _makeDrawingClass(self):
        log('LinearGroove makeDrawingClass: %s' % (self.__repr__()))
        class Anon(RoundEndedRectangleDrawing):
            params = self.getParams()
            # options = self.getOptions()
            observable = self
            view_space = self.view_space
            reference_point = 'lower-left'
        return Anon
