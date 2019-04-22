from MachinedGeometry_class import MachinedGeometry

from RoundBottomedDado_class import RoundBottomedDado
from DoughnutCutter_class import DoughnutCutter
from RectangularPocket_class import RectangularPocket

class FeatureCreature(MachinedGeometry):
    # class variables:
    name = "Feature Creature"
    version = "0.1"
    implements_toolpass_view = False

    def __init__(self):
        pass

    def assertValid(self):
        pass

    def generateGcode(self):
        pass

    def getDataQueries(self):
        return self.entry_queries

    def getGeometry(self):
        pass

    def getToolPasses(self):
        pass

    def getViewSpaceInit(self):
        # Totally arbitrary, we should be able to modify as we add features.
        view_init = { "view_plane": "XY", \
                      "extents": {"width": 50, "height": 50, "center": (0, 0)} }
        return view_init

    def makeQueries(self, data_types, query_types):
        self.query_types = query_types
        self.data_types = data_types
        # Presents drop-down/spinbox for features to draw.
        features = [RoundBottomedDado, DoughnutCutter, RectangularPocket]
        SpinBoxQuery = query_types['spinbox']
        StringVar = data_types['string']
        queries = SpinBoxQuery({
            'name': 'Feature',
            'type': StringVar,
            'values': tuple([ x.name for x in features ])
            })
        print(queries)
        self.entry_queries = [queries]


