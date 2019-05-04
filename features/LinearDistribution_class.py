from GeometricFeature_class import GeometricFeature
# from option_queries import *
from option_queries import *


class LinearDistribution(GeometricFeature):
    name = 'Linear Distribution'
    user_selectable = True
    option_query_classes = [
        GeometricFeatureQuery,
    ]

    child_feature_classes = []

    def getGCode(self):
        return self.child_features.values()[0].getInstructions(sequence)

    def getInstructions(self):
        pass

    def moveToStart(self):
        pass

    def returnToHome(self):
        pass
