class MockViewSpace(object):
    def __init__(self, canvas = None):
        self.view_plane = 'XY'
        self.canvas = canvas
        self.x_conv = lambda x: x
        self.y_conv = lambda x: x
        self.view_scale = 1

    def setExtents(self, *args, **kwds):
        pass
