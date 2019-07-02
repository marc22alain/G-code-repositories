from DistributedFeature_class import DistributedFeature
from drawn_features import LinearDistributionDrawing
from option_queries import GeometricFeatureQuery, DeltaXQuery, DeltaYQuery, NumRepeatQuery, \
    ReferenceXQuery, ReferenceYQuery
from utilities import log, Glib as G


class LinearDistribution(DistributedFeature):
    """Is composed of a single feature."""
    name = 'Linear Distribution'
    user_selectable = True
    option_query_classes = [
        GeometricFeatureQuery,
        DeltaXQuery,
        DeltaYQuery,
        NumRepeatQuery
    ]

    child_feature_classes = []

    def moveToStart(self):
        return ''

    def returnToHome(self):
        delta_X = self.option_queries[DeltaXQuery].getValue()
        delta_Y = self.option_queries[DeltaYQuery].getValue()
        num_repeats = self.option_queries[NumRepeatQuery].getValue() - 1
        file_text = self.machine.setMode('INCR')
        file_text += G.G0_XY((- (delta_X * num_repeats), - (delta_Y * num_repeats)))
        return file_text

    def getChild(self):
        """Get the single child instance."""
        log(self.features)
        return self.features[0]

    def distributeChildFeature(self):
        file_text = self.features[0].getGCode()
        delta_X = self.option_queries[DeltaXQuery].getValue()
        delta_Y = self.option_queries[DeltaYQuery].getValue()
        for _ in xrange(self.option_queries[NumRepeatQuery].getValue() - 1):
            file_text += self.machine.setMode('INCR')
            file_text += G.G0_XY((delta_X, delta_Y))
            file_text += self.features[0].getGCode()
        return file_text

    def getParams(self):
        basic_params = self.getBasicParams()
        basic_params.update({
            'refX': self.option_queries[ReferenceXQuery].getValue(),
            'ref_Y': self.option_queries[ReferenceYQuery].getValue(),
            'delta_X': self.option_queries[DeltaXQuery].getValue(),
            'delta_Y': self.option_queries[DeltaYQuery].getValue(),
            'num_repeats': self.option_queries[NumRepeatQuery].getValue()
        })
        return basic_params

    def _makeDrawingClass(self):
        log('LinearDistribution makeDrawingClass: %s' % (self.__repr__()))
        class Anon(LinearDistributionDrawing):
            params = self.getParams()
            observable = self
            child_object_function = self.getChild().makeDrawingClass()
            view_space = self.view_space
        return Anon
