#!/usr/bin/env python

import abc

class GeometricFeature:
    __metaclass__ = abc.ABCMeta

    def __init__(self, machine, work_piece):
        self.machine = machine
        self.work_piece = work_piece
        self.option_query_set = set()
        self.makeChildren()

    @abc.abstractmethod
    def getGCode(self):
        pass

    def getOptionQueries(self):
        # https://treyhunner.com/2016/02/how-to-merge-dictionaries-in-python/
        try:
            # TODO: resolve for multiple children, for composed features
            self.option_query_instances = self.children.values()[0].getOptionQueries().copy()
        except IndexError:
            self.option_query_instances = {}

        self.option_query_instances.update(self._getOwnOptionQueries())
        return self.option_query_instances

    def _getOwnOptionQueries(self):
        return { key: key() for key in self.option_queries}

    def setChildFeatures(self, feature_class):
        '''
        Used for composed features, where user creates the composition.
        '''
        # here, self.child_feature_classes is an instance property
        # ... oooh so dynamic !
        # to be really clever, would confirm that super_class is GeometricFeature
        assert type(feature_class) == type(GeometricFeature), 'Must be a class'
        try:
            self.child_feature_classes.append(feature_class)
        except AttributeError:
            self.child_feature_classes = [feature_class]

    def makeChildren(self):
        self.children = { key: key(self.machine, self.work_piece) for key in self.child_feature_classes}
