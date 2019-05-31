import abc

class AbstractFeatureManager:
    __metaclass__ = abc.ABCMeta


    @abc.abstractmethod
    def addChild(self, feature_class):
        '''
        Use to interactively add feature instances to be managed.
        '''
        pass

    @abc.abstractmethod
    def deleteChild(self, feature_instance):
        '''
        Delete the feature instance
        '''
        pass

    @abc.abstractmethod
    def childDidUpdate(self, feature_instance):
        pass
