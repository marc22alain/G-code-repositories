from GeometricFeature_class import GeometricFeature
from OptionQuery_class import OptionQuery

class Generic(GeometricFeature):
    name = 'Generic'
    user_selectable = False
    option_query_classes = []

    child_feature_classes = []

    # def __init__(self):
    #     super.__init__()
    #     pass

    def getGCode(self):
        pass

    def getOptionQueries(self):
        pass
