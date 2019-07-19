from option_queries import *
from features import RectangularPocket, Tenon
from workpieces import SimpleWorkpiece

class MortiseAndTenonJoint(QueryManager):
    """The explanation. Rail and stile have same edge width."""
    name = 'Mortise and Tenon Joint Designer'
    option_query_classes = [
        MortiseDepthQuery,
        RailFaceWidthQuery,
        StileFaceWidthQuery,
        StileEdgeWidthQuery,
        TenonShoulderQuery
    ]

    def __init__(self):
        QueryManager.__init__(self)
        self.stile = None
        self.rail = None
        self.mortise = None
        self.tenon = None

    def getFeatures(self):
        if self.mortise is None or self.tenon is None:
            raise ValueError('leaf features are not yet defined')
        return {
            RectangularPocket: self.mortise,
            Tenon: self.tenon
        }

    def getAllStuff(self):
        return {
            'mortise': {
                'feature': self.mortise,
                'workpiece': self.stile
            },
            'tenon': {
                'feature': self.tenon,
                'workpiece': self.rail
            }
        }

    def cancelFunction(self):
        print 'cancelFunction passed'

    def postQueryUpdateHook(self):
        print 'postQueryUpdateHook passed'
        self.designJoint()

    def designJoint(self):
        # adjust the stile
        if self.stile is None:
            # note that critical arguments must be later supplied
            self.stile = SimpleWorkpiece(None, None)
            self.stile.getOptionQueries()
        # adding some arbitrary extra to suggest length
        self.stile.option_queries[StockLengthQuery]\
            .setValue(self.option_queries[RailFaceWidthQuery].getValue() + 30)
        self.stile.option_queries[StockWidthQuery]\
            .setValue(self.option_queries[StileEdgeWidthQuery].getValue())
        self.stile.option_queries[StockHeightQuery]\
            .setValue(self.option_queries[StileFaceWidthQuery].getValue())

        # adjust the mortise
        if self.mortise is None:
            # note that critical arguments must be later supplied
            self.mortise = RectangularPocket(None, None)
            self.mortise.getOptionQueries()
        self.mortise.option_queries[SideXQuery]\
            .setValue(self.option_queries[RailFaceWidthQuery].getValue()
                        - (2 * self.option_queries[TenonShoulderQuery]))
        # assuming that StileEdgeWidthQuery would be same as RailEdgeWidthQuery
        self.mortise.option_queries[SideYQuery]\
            .setValue(self.option_queries[StileEdgeWidthQuery].getValue()
                        - (2 * self.option_queries[TenonShoulderQuery]))
        # TODO: yet more stuff to set

        # adjust the rail
        if self.rail is None:
            # note that critical arguments must be later supplied
            self.rail = SimpleWorkpiece(None, None)
            self.rail.getOptionQueries()
        self.rail.option_queries[StockLengthQuery]\
            .setValue(self.option_queries[RailFaceWidthQuery].getValue())
        self.rail.option_queries[StockWidthQuery]\
            .setValue(self.option_queries[StileEdgeWidthQuery].getValue())
        self.rail.option_queries[StockHeightQuery]\
            .setValue(self.option_queries[MortiseDepthQuery].getValue() + 30)

        # adjust the tenon
        if self.tenon is None:
            # note that critical arguments must be later supplied
            self.tenon = Tenon(None, None)
            self.tenon.getOptionQueries()
        # adding some arbitrary extra to suggest length
        self.tenon.option_queries[ShoulderOffsetQuery]\
            .setValue(self.option_queries[RailFaceWidthQuery].getValue())
        self.tenon.option_queries[CornerRadiusQuery]\
            .setValue(self.option_queries[StileEdgeWidthQuery].getValue())
        self.tenon.option_queries[StockHeightQuery]\
            .setValue(self.option_queries[StileFaceWidthQuery].getValue())
