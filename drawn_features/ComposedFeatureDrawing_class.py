from FeatureDrawing_class import FeatureDrawing
from observeder import AutoObserver
from utilities import log

class ComposedFeatureDrawing(FeatureDrawing, AutoObserver):
    """For drawn feature classes implementing distribution functions.
    May also work for more general composed features ?"""
    child_object_functions = None

    def __init__(self):
        AutoObserver.__init__(self)
        FeatureDrawing.__init__(self)

    def draw(self):
        """Overrides FeatureDrawing.draw, omitting the call to
        executeTransforms()."""
        view_plane = self.view_space.view_plane
        if view_plane == 'XY':
            self._drawXYentities()
        elif view_plane == 'YZ':
            self._drawYZentities()
        else:
            self._drawXZentities()
        return self

    def _drawXYentities(self):
        self._clearEntities('XY')
        log('ComposedFeatureDrawing _drawXYentities: %s' % (self.__repr__()))
        ref_X = self.params['ref_X']
        ref_Y = self.params['ref_Y']
        move_params = {
            'move': {
                'delta_X': ref_X,
                'delta_Y': ref_Y,
            }
        }
        for child in self.child_object_functions:
            self.entities['XY'].append(
                child().addTransform(self.transforms + [move_params]).draw()
            )


    def _drawXZentities(self):
        self._clearEntities('XZ')
        pass

    def _drawYZentities(self):
        self._clearEntities('YZ')
        pass

    def _clearEntities(self, plane):
        for entity in self.entities[plane]:
            entity.remove()
