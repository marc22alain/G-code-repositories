#!/usr/bin/env python
import abc
from option_queries import *
from utilities import Glib as G
import inspect
import os

class GeometricFeature:
    __metaclass__ = abc.ABCMeta

    common_query_classes = [
        ReferenceXQuery,
        ReferenceYQuery
    ]

    def __init__(self, feature_manager, view_space):
        self.entities = {
            'XY': [],
            'YZ': [],
            'XZ': []
        }
        self.current_plane = view_space.view_plane
        self.feature_manager = feature_manager
        self.view_space = view_space
        self.machine = feature_manager.machine
        self.work_piece = feature_manager.work_piece
        self.option_queries = { key: None for key in self.option_query_classes }
        self.option_queries.update({ key: None for key in self.common_query_classes })
        self.child_features = { key: None for key in self.child_feature_classes }
        self.makeChildren()

    @abc.abstractmethod
    def getGCode(self):
        pass

    @abc.abstractmethod
    def moveToStart(self):
        pass

    @abc.abstractmethod
    def returnToHome(self):
        pass

    def drawGeometry(self):
        view_plane = self.view_space.view_plane
        if view_plane == 'XY':
            self._drawXYentities()
        elif view_plane == 'YZ':
            self._drawYZentities()
        else:
            self._drawXZentities()

    @abc.abstractmethod
    def _drawXYentities(self):
        pass

    @abc.abstractmethod
    def _drawYZentities(self):
        pass

    @abc.abstractmethod
    def _drawXZentities(self):
        pass

    def validateParams(self):
        pass

    def getOptionQueries(self):
        '''
        Core interface
        '''
        # To prevent overwriting instantiated queries
        if None in self.option_queries.values():
            # https://treyhunner.com/2016/02/how-to-merge-dictionaries-in-python/
            child_query_instances = self._getChildOptionQueries()
            child_query_instances.update(self._getOwnOptionQueries())
            self.option_queries.update(child_query_instances)
        return self.option_queries

    def _getOwnOptionQueries(self):
        '''
        Core interface
        '''
        return { key: key() for key in self.option_queries }

    def _getChildOptionQueries(self):
        '''
        May be spun out to other interface
        '''
        try:
            child_query_instances = {}
            for child in self.child_features.values():
                child_query_instances.update(child.getOptionQueries().copy())
        except IndexError:
            child_query_instances = {}
        return child_query_instances

    def setChildFeatures(self, feature_class):
        '''
        Used for composed features, where user creates the composition.
        May spin out to other interface
        '''
        # here, self.child_feature_classes is an instance property
        # ... oooh so dynamic !
        # to be really clever, would confirm that super_class is GeometricFeature
        assert type(feature_class) == type(GeometricFeature), 'Must be a class'
        self.child_features[feature_class] = feature_class

    def makeChildren(self):
        '''
        May be spun out to other interface
        '''
        children = { key: key(self.feature_manager, self.view_space) for key in self.child_features}
        self.child_features.update(children)

    def getBasicParams(self):
        '''
        Core interface
        '''
        params = {}
        params.update(self.machine.getParams().copy())
        params.update(self.work_piece.getParams().copy())
        return params

    def delete(self):
        '''
        Core interface
        '''
        for entity in self.entities[self.current_plane]:
            entity.remove()
        self.feature_manager.deleteChild(self)

    def moveToReference(self):
        '''
        Core interface
        '''
        file_text = self.addDebug(inspect.currentframe())
        refX = self.option_queries[ReferenceXQuery].getValue()
        refY = self.option_queries[ReferenceYQuery].getValue()
        file_text += self.machine.setMode('INCR')
        file_text += G.G0_XY((refX, refY))
        file_text += self.moveToStart()
        return file_text

    def returnFromReference(self):
        '''
        Core interface
        '''
        file_text = self.addDebug(inspect.currentframe())
        refX = self.option_queries[ReferenceXQuery].getValue()
        refY = self.option_queries[ReferenceYQuery].getValue()
        file_text += self.returnToHome()
        file_text += self.machine.setMode('INCR')
        file_text += G.G0_XY((- refX, - refY))
        return file_text

    def addDebug(self, frame):
        if 'DEBUG_GCODE' in os.environ.keys():
            trace = inspect.getframeinfo(frame)
            class_file = trace.filename.split('/')[-1].split('_class')[0]
            return '# %s \n' % (class_file + '.' + trace.function + ' - line:' + str(trace.lineno))
        else:
            return ''

    def didUpdateQueries(self):
        '''
        Maybe trigger notifications instead.
        self.continuation.trigger()
        '''
        self.drawGeometry()

    def changeViewPlane(self):
        for entity in self.entities[self.current_plane]:
            entity.remove()
        self.current_plane = self.view_space.view_plane
        self.drawGeometry()

