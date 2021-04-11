from FeatureDrawing_class import FeatureDrawing

class DistributedFeatureDrawing(FeatureDrawing):
    """For drawn feature classes implementing distribution functions.
    May also work for more general composed features ?"""

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
