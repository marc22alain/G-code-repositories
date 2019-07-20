from option_queries import *
from features import RectangularPocket, Tenon
from workpieces import SimpleWorkpiece

class MortiseAndTenonJoint(QueryManager):
    """Is a joint designer.
    Rail and stile have same edge width."""
    name = 'Mortise and Tenon Joint Designer'
    option_query_classes = [
        MortiseDepthQuery,
        RailFaceWidthQuery,
        StileFaceWidthQuery,
        StileEdgeWidthQuery,
        TenonShoulderQuery
    ]

    # allow space for glue to pool at the bottom of the mortise; unit is mm
    glue_well = 2

    def __init__(self, machine):
        QueryManager.__init__(self)
        self.stile = None
        self.rail = None
        self.mortise = None
        self.tenon = None
        self.machine = machine

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
        rail_face_width = self.option_queries[RailFaceWidthQuery].getValue()
        stile_face_width = self.option_queries[StileFaceWidthQuery].getValue()
        stile_edge_width = self.option_queries[StileEdgeWidthQuery].getValue()
        mortise_depth = self.option_queries[MortiseDepthQuery].getValue()
        tenon_shoulder = self.option_queries[TenonShoulderQuery].getValue()
        bit_radius = self.machine.option_queries[BitDiameterQuery].getValue() / 2

        # adjust the stile
        if self.stile is None:
            # note that critical arguments must be later supplied
            self.stile = SimpleWorkpiece(None, None)
            self.stile.getOptionQueries()
        # adding some arbitrary extra to suggest length, visual effect
        self.stile.option_queries[StockLengthQuery].setValue(rail_face_width + 30)
        self.stile.option_queries[StockWidthQuery].setValue(stile_edge_width)
        self.stile.option_queries[StockHeightQuery].setValue(stile_face_width)

        # adjust the mortise
        if self.mortise is None:
            # note that critical arguments must be later supplied
            self.mortise = RectangularPocket(None, None)
            self.mortise.work_piece = self.stile
            self.mortise.machine = self.machine
            self.mortise.getOptionQueries()
        self.mortise.option_queries[SideXQuery].setValue(rail_face_width - (2 * tenon_shoulder))
        # assuming that StileEdgeWidthQuery would be same as RailEdgeWidthQuery
        self.mortise.option_queries[SideYQuery].setValue(stile_edge_width - (2 * tenon_shoulder))
        self.mortise.option_queries[ReferenceXQuery].setValue(rail_face_width / 2)
        self.mortise.option_queries[ReferenceYQuery].setValue(stile_edge_width / 2)
        self.mortise.option_queries[CutDepthQuery].setValue(mortise_depth)

        # adjust the rail
        if self.rail is None:
            # note that critical arguments must be later supplied
            self.rail = SimpleWorkpiece(None, None)
            self.rail.getOptionQueries()
        self.rail.option_queries[StockLengthQuery].setValue(rail_face_width)
        self.rail.option_queries[StockWidthQuery].setValue(stile_edge_width)
        # adds some length for visual effect
        # TODO: will probably set to the jig reference height
        self.rail.option_queries[StockHeightQuery].setValue(mortise_depth + 30)

        # adjust the tenon
        if self.tenon is None:
            # note that critical arguments must be later supplied
            self.tenon = Tenon(None, None)
            self.tenon.work_piece = self.rail
            self.tenon.machine = self.machine
            self.tenon.getOptionQueries()
        self.tenon.option_queries[ShoulderOffsetQuery].setValue(tenon_shoulder)
        self.tenon.option_queries[CornerRadiusQuery].setValue(bit_radius)
        # putting in the glue_well
        self.tenon.option_queries[CutDepthQuery].setValue(mortise_depth - self.glue_well)
        # the Tenon self-updates ReferenceXYQueries to be contentric to work_piece
        self.tenon.didUpdateQueries()
