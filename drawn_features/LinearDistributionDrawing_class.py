from DistributedFeatureDrawing_class import DistributedFeatureDrawing
from observeder import AutoObserver
from utilities import log

# used by LinearDistribution
class LinearDistributionDrawing(DistributedFeatureDrawing, AutoObserver):

    child_object_function = None

    def __init__(self):
        AutoObserver.__init__(self)
        DistributedFeatureDrawing.__init__(self)

    def _drawXYentities(self):
        self._clearEntities('XY')
        log('LinearDistributionDrawing _drawXYentities: %s' % (self.__repr__()))
        delta_X = self.params['delta_X']
        delta_Y = self.params['delta_Y']
        refX = self.params['refX']
        refY = self.params['refY']
        for i in xrange(self.params['num_repeats']):
            # for example, instantiate HoleDrawing
            move_params = {
                'move': {
                    'delta_X': refX + (i * delta_X),
                    'delta_Y': refY + (i * delta_Y),
                }
            }
            self.entities['XY'].append(self.child_object_function().addTransform(self.transforms + [move_params]).draw())

    def _drawYZentities(self):
        self._clearEntities('YZ')
        log('LinearDistributionDrawing _drawXYentities: %s' % (self.__repr__()))
        delta_X = self.params['delta_X']
        delta_Y = self.params['delta_Y']
        refX = self.params['refX']
        refY = self.params['refY']
        for i in xrange(self.params['num_repeats']):
            # for example, instantiate HoleDrawing
            move_params = {
                'move': {
                    'delta_X': refX + (i * delta_X),
                    'delta_Y': refY + (i * delta_Y),
                }
            }
            self.entities['YZ'].append(self.child_object_function().addTransform(self.transforms + [move_params]).draw())

    def _drawXZentities(self):
        self._clearEntities('XZ')
        log('LinearDistributionDrawing _drawXYentities: %s' % (self.__repr__()))
        delta_X = self.params['delta_X']
        delta_Y = self.params['delta_Y']
        refX = self.params['refX']
        refY = self.params['refY']
        for i in xrange(self.params['num_repeats']):
            # for example, instantiate HoleDrawing
            move_params = {
                'move': {
                    'delta_X': refX + (i * delta_X),
                    'delta_Y': refY + (i * delta_Y),
                }
            }
            self.entities['XZ'].append(self.child_object_function().addTransform(self.transforms + [move_params]).draw())

    def _clearEntities(self, plane):
        for entity in self.entities[plane]:
            entity.remove()