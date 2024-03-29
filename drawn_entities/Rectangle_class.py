from Tkinter import *
from GeometricEntity_class import GeometricEntity

class Rectangle(GeometricEntity):
    """Draws rectangles in the Tkinter canvas."""
    def __init__(self, view_space):
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        GeometricEntity.__init__(self, view_space)

    def assertValid(self):
        pass

    def _setParams(self, params):
        if len(params) != 4:
            raise ValueError("Incorrect number of params submitted!")
        self.x1 = params[0]
        self.y1 = params[1]
        self.x2 = params[2]
        self.y2 = params[3]


    def setAll(self, params, options):
        """ Expects params to be a tuple and options to be a dict.
        Supports chaining after instantiation. """
        if len(params) != 4:
            raise ValueError("Incorrect number of params submitted!")
        self.x1 = params[0]
        self.y1 = params[1]
        self.x2 = params[2]
        self.y2 = params[3]
        self.options = options
        # To allow chaining of operations
        return self


    def _draw(self):
        canvas = self.view_space.canvas
        mapping_x = self.view_space.x_conv
        mapping_y = self.view_space.y_conv
        # We need to return the returned element id.
        return [canvas.create_rectangle(
            mapping_x(self.x1),
            mapping_y(self.y1),
            mapping_x(self.x2),
            mapping_y(self.y2)
        )]

    def _update(self):
        canvas = self.view_space.canvas
        mapping_x = self.view_space.x_conv
        mapping_y = self.view_space.y_conv
        canvas.coords(
            self.ids[0],
            mapping_x(self.x1),
            mapping_y(self.y1),
            mapping_x(self.x2),
            mapping_y(self.y2)
        )

    def getParams(self):
        return (
            [
                self.x1,
                self.y1,
                self.x2,
                self.y2
            ],
            self.options
        )
