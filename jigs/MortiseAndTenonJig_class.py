# from feature_manager import AbstractFeatureManager
from features import ComposedFeature, LinearDistribution
from machines import SimpleMachine
from option_queries import GeometricFeatureQuery, DeltaXQuery, DeltaYQuery, NumRepeatQuery, \
    ReferenceXQuery, ReferenceYQuery, StockWidthQuery, CutPerPassQuery, StockLengthQuery
# MC.mortisingJig
from utilities import log, Glib as G, MC
from workpieces import SimpleWorkpiece


class MortiseAndTenonJig(ComposedFeature):
    """Is composed of a two features."""
    name = 'Mortise and Tenon Jig'
    user_selectable = True
    option_query_classes = [
        GeometricFeatureQuery,
        DeltaXQuery,
        DeltaYQuery,
        NumRepeatQuery
    ]

    child_feature_classes = []

    def __init__(self, view_space=None):
        self.root = True
        # KLUDGE: work_piece exists only to conform to the class interface
        self.work_piece = None
        self.stile_work_piece = None
        self.mortise_feature = None
        self.rail_work_piece = None
        self.tenon_feature = None
        self.machine = SimpleMachine(self)
        self.view_space = view_space
        self.g_code = None
        ComposedFeature.__init__(self, self, view_space)
        self.mortise_distribution = None
        self.tenon_distribution = None

    def moveToStart(self):
        # Assumes that the machine is set up at the jig's centerline (for Y)
        # and some X to be determined.
        return ''

    def _instantiateMortiseDistribution(self):
        # here we decide whether to implement a LinearDistribution of MirroredDistribution
        jig_width = MC.mortisingJig['jigWidth']
        stile_face_width = self.stile_work_piece.option_queries[StockWidthQuery].getValue()
        rail_face_width = self.rail_work_piece.option_queries[StockLengthQuery].getValue()
        self.mortise_distribution = LinearDistribution(self, self.view_space)
        self.mortise_distribution.getOptionQueries()
        # starting reference point is the center of the mortise/RectangularPocket
        # distance from jig reference point to stile stop - (rail_face_width / 2)
        # when ReferencePointQuery is implemented, use 'center'
        self.mortise_distribution.option_queries[ReferenceXQuery].setValue(
            MC.mortisingJig['stileEndReference'] - (rail_face_width / 2)
        )
        self.mortise_distribution.option_queries[ReferenceYQuery].setValue(
            - ((jig_width + stile_face_width) / 2)
        )
        self.mortise_distribution.option_queries[DeltaXQuery].setValue(0)
        self.mortise_distribution.option_queries[DeltaYQuery].setValue(
            jig_width + stile_face_width
        )
        self.mortise_distribution.option_queries[NumRepeatQuery].setValue(2)
        self.mortise_distribution.addChild(self.mortise_feature)

    def _instantiateTenonDistribution(self):
        rail_face_width = self.rail_work_piece.option_queries[StockLengthQuery].getValue()
        rail_edge_width = self.rail_work_piece.option_queries[StockWidthQuery].getValue()
        jig_width = MC.mortisingJig['jigWidth']
        # here we decide whether to implement a LinearDistribution of MirroredDistribution
        self.tenon_distribution = LinearDistribution(self, self.view_space)
        self.tenon_distribution.getOptionQueries()
        # where the tenon's reference point is the lower-left corner of the work-piece
        # and the jig's first tenon location is at the upper-left corner of the work-piece
        self.tenon_distribution.option_queries[ReferenceXQuery].setValue(
            MC.mortisingJig['railEndReference']
        )
        self.tenon_distribution.option_queries[ReferenceYQuery].setValue(
            - ((jig_width / 2) + rail_edge_width)
        )
        self.tenon_distribution.option_queries[DeltaXQuery].setValue(0)
        self.tenon_distribution.option_queries[DeltaYQuery].setValue(
            jig_width + rail_edge_width
        )
        self.tenon_distribution.option_queries[NumRepeatQuery].setValue(2)
        self.tenon_distribution.addChild(self.tenon_feature)

    def returnToHome(self):
        return ''

    def getParams(self):
        raise TypeError('method `getParams` not implemented yet')
        basic_params = self.getBasicParams()
        basic_params.update({
    #         'ref_X': self.option_queries[ReferenceXQuery].getValue(),
    #         'ref_Y': self.option_queries[ReferenceYQuery].getValue(),
    #         'delta_X': self.option_queries[DeltaXQuery].getValue(),
    #         'delta_Y': self.option_queries[DeltaYQuery].getValue(),
    #         'num_repeats': self.option_queries[NumRepeatQuery].getValue()
        })
        return basic_params

    def _makeDrawingClass(self):
        log('MortiseAndTenonJig makeDrawingClass: %s' % (self.__repr__()))
        class Anon(MortiseAndTenonJigDrawing):
            params = self.getParams()
            observable = self
            child_object_function = self.getChild().makeDrawingClass()
            view_space = self.view_space
        return Anon

    def getGCode(self):
        file_text = self.machine.setUpProgram()
        file_text += self.moveToReference()
        file_text += self.mortise_distribution.getGCode()
        file_text += self.tenon_distribution.getGCode()
        file_text += self.returnFromReference()
        file_text += self.machine.endProgram()
        return file_text

    def addEntities(self, update):
        print update
        self.stile_work_piece = update['stile']
        self.mortise_feature = update['mortise']
        self.rail_work_piece = update['rail']
        self.tenon_feature = update['tenon']
        # now create the distributions for the jig's locations
        self._instantiateMortiseDistribution()
        self._instantiateTenonDistribution()
        self.setCutPerPass()

    def reDrawAll(self):
        pass

    def setCutPerPass(self):
        self.tenon_feature.option_queries[CutPerPassQuery].setValue(3)
        self.mortise_feature.option_queries[CutPerPassQuery].setValue(3)
