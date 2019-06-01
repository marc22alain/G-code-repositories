import abc

class FeatureDrawing:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.transform_funcs = []
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
        self.executeTransforms()

    def addTransform(self, func):
        self.transform_funcs.append(func)

    def executeTransforms(self):
        # chain execution of the transforms
        return self

    def remove(self):
        def add(x,y): return x+y
        for entity in reduce(add, self.entities.values()):
            entity.remove()

    @abc.abstractmethod
    def move(self, params):
        pass

    @abc.abstractmethod
    def rotate(self, params):
        pass

    @abc.abstractmethod
    def _drawXYentities(self):
        pass

    @abc.abstractmethod
    def _drawYZentities(self):
        pass

    @abc.abstractmethod
    def _drawXZentities(self):
        pass
