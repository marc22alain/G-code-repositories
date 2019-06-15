import abc
from utilities import log

class FeatureDrawing:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.transforms = []
        self.entities = {
            'XY': [],
            'YZ': [],
            'XZ': []
        }

    def draw(self):
        view_plane = self.view_space.view_plane
        if view_plane == 'XY':
            self._drawXYentities()
        elif view_plane == 'YZ':
            self._drawYZentities()
        else:
            self._drawXZentities()
        # Separating out the execution of transforms only makes sense at the leaf feature.
        self.executeTransforms()
        return self

    def addTransform(self, transforms):
        log('FeatureDrawing addTransform: %s' % (self.__repr__()))
        self.transforms = transforms
        return self

    def executeTransforms(self):
        '''
        This method only runs in leaf features.
        '''
        log('FeatureDrawing executeTransforms: %s' % (self.__repr__()))
        # Chain execution of the transforms
        for transform in self.transforms:
            print transform
            log(transform)
            if 'move' in transform.keys():
                self.move(transform['move'])
            if 'rotate' in transform.keys():
                self.rotate(transform['rotate'])
        return self

    def remove(self):
        def add(x,y): return x+y
        for entity in reduce(add, self.entities.values()):
            entity.remove()

    def move(self, params = None):
        '''
        This method only runs in leaf features.
        '''
        log('******* FeatureDrawing called move(): %s' % (self.__repr__()))
        if params:
            for entity in self.entities[self.view_space.view_plane]:
                entity.move(params)

    def rotate(self, params = None):
        '''
        This method only runs in leaf features.
        '''
        log('******* FeatureDrawing called rotate(): %s' % (self.__repr__()))
        if params:
            for entity in self.entities[self.view_space.view_plane]:
                entity.rotate(params)

    @abc.abstractmethod
    def _drawXYentities(self):
        pass

    @abc.abstractmethod
    def _drawYZentities(self):
        pass

    @abc.abstractmethod
    def _drawXZentities(self):
        pass
