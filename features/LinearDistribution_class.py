from GeometricFeature_class import GeometricFeature
from option_queries import *


class LinearDistribution(GeometricFeature):
    name = 'Linear Distribution'
    user_selectable = True
    option_query_classes = [
        GeometricFeatureQuery,
        DeltaXQuery,
        DeltaYQuery,
        NumRepeatQuery
    ]

    is_composed = True

    child_feature_classes = []

    def getGCode(self):
        return self.child_features.values()[0].getGCode(sequence)

    def getInstructions(self):
        pass

    def moveToStart(self):
        pass

    def returnToHome(self):
        pass

    def manageChild(self):
        print 'managing child'
        # open a dialog for this task

    def getChild(self):
        return self.child_features.values()[0]

    def update(self):
        child_class = self.option_queries[GeometricFeatureQuery].getValue()
        if child_class not in self.child_features.keys():
            # LinearDistribution standing in as FeatureManager
            self.child_features = { child_class: child_class(self) }

    def deleteFeature(self, feature):
        print 'LinearDistribution deleteFeature !!!'
