import abc
from ui import OptionQueryDialog
from option_queries import *

class AbstractFeatureManager:
    __metaclass__ = abc.ABCMeta

    app = None

    def __init__(self):
        self.features = []
        self.root = False   # default value; set to True for root by app


    def addChild(self, feature_class = None):
        # for ComposedFeature
        if feature_class == None:
            query = self.option_queries[GeometricFeatureQuery]
            query.updateValue()
            feature_class = query.getValue()
        feature = feature_class(self, self.view_space)
        self.features.append(feature)
        # passed in as callback
        def addFunction():
            queries = feature.getOptionQueries().values()
            if hasattr(feature, 'is_composed'):
                feature.addChild()
            # makes the initial call to makeDrawingClass()
            feature.didUpdateQueries()
            # root FeatureManager has special responsibilities
            if self.root:
                feature.drawGeometry()
                self.app.feature_list.insertFeature(feature)
        # passed in as callback
        def cancelFunction():
            self.features.pop()
            print 'running CANCEL function'
        OptionQueryDialog(self.app, feature.getOptionQueries(), feature.name, addFunction, cancelFunction)

    @abc.abstractmethod
    def deleteChild(self, feature_instance):
        '''
        Delete the feature instance
        '''
        pass
