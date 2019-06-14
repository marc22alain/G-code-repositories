from FeatureDrawing_class import FeatureDrawing

class DistributedFeatureDrawing(FeatureDrawing):

    def draw(self):
        view_plane = self.view_space.view_plane
        if view_plane == 'XY':
            self._drawXYentities()
        elif view_plane == 'YZ':
            self._drawYZentities()
        else:
            self._drawXZentities()
        return self
