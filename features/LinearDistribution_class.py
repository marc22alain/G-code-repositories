from GeometricFeature_class import GeometricFeature
# from option_queries import *
from option_queries import *


class LinearDistribution(GeometricFeature):
    name = 'Linear Distribution'
    user_selectable = True
    option_queries = [
        GeometricFeatureQuery,
    ]

    child_feature_classes = []

    def getGCode(self):
        return ''
