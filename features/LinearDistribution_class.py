from DistributedFeature_class import DistributedFeature
from option_queries import *
from utilities import Glib as G


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

    # defined in DistributedFeature class
    # def getGCode(self):

    def moveToStart(self):
        return ''

    def returnToHome(self):
        delta_X = self.option_queries[DeltaXQuery].getValue()
        delta_Y = self.option_queries[DeltaYQuery].getValue()
        num_repeats = self.option_queries[NumRepeatQuery].getValue() - 1
        file_text = self.machine.setMode('INCR')
        file_text += G.G0_XY((- (delta_X * num_repeats), - (delta_Y * num_repeats)))
        return file_text

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
        file_text = self.child_features.values()[0].getGCode()
        delta_X = self.option_queries[DeltaXQuery].getValue()
        delta_Y = self.option_queries[DeltaYQuery].getValue()
        for i in xrange(self.option_queries[NumRepeatQuery].getValue() - 1):
            file_text += self.machine.setMode('INCR')
            file_text += G.G0_XY((delta_X, delta_Y))
            file_text += self.child_features.values()[0].getGCode()
        return file_text

    def _drawXYentities(self):
        raise TypeError('LinearDistribution does not implement _drawXYentities')

    def _drawYZentities(self):
        raise TypeError('LinearDistribution does not implement _drawYZentities')

    def _drawXZentities(self):
        raise TypeError('LinearDistribution does not implement _drawXZentities')
