from DistributedFeature_class import DistributedFeature
from option_queries import *


class LinearDistribution(DistributedFeature):
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
        return self.child_features.values()[0].getGCode()

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

    # TODO: decide whether this should be explicitly `updateFeature`
    def updateFeatures(self):
        child_class = self.option_queries[GeometricFeatureQuery].getValue()
        if child_class not in self.child_features.keys():
            # LinearDistribution standing in as FeatureManager
            self.child_features = { child_class: child_class(self) }

    # TODO: determine whether this can go into the GeometricFeature class
    # ... it seems applicable to structures that hold many features
    def deleteFeature(self, feature):
        self.child_features = { k:v for k,v in self.child_features.iteritems() if v != feature }

    def distributeChildFeature(self):
        pass
