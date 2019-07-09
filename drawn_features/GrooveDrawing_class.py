from errors import PathReferenceError

class GrooveDrawing(object):
    """The drawing's path reference is one of ['center', 'od', 'id']
    'center' path reference is at the very center of bit's path.
    'od' path reference is the outer diameter of bit's path.
    'id' path reference is the inner diameter of bit's path."""

    def getAdjustments(self):
        """Produce adjustments for the various `path_reference` types."""
        path_reference = self.params['path_reference']
        bit_diameter = self.params['bit_diameter']
        bit_radius = bit_diameter / 2
        if path_reference == 'center':
            inner_adj = - bit_radius
            outer_adj = bit_radius
        elif path_reference == 'od':
            inner_adj = - bit_diameter
            outer_adj = 0
        elif path_reference == 'id':
            inner_adj = 0
            outer_adj = bit_diameter
        else:
            raise PathReferenceError(self, path_reference)
        return (inner_adj, outer_adj)
