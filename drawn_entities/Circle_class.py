from Tkinter import *
from GeometricEntity_class import GeometricEntity


class Circle(GeometricEntity):
    """Draws circles in the Tkinter canvas."""
    def __init__(self, view_space):
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        self.center_x = None
        self.center_y = None
        self.radius = None
        self.options = None
        GeometricEntity.__init__(self, view_space)

    def assertValid(self):
        pass

    def _setParams(self, params):
        """ Takes in the standard bounding box parameters. """
        if len(params) != 4:
            raise ValueError("Incorrect number of params submitted!")
        self.x1 = params[0]
        self.y1 = params[1]
        self.x2 = params[2]
        self.y2 = params[3]

    def _draw(self):
        canvas = self.view_space.canvas
        mapping_x = self.view_space.x_conv
        mapping_y = self.view_space.y_conv
        return [canvas.create_oval(
            mapping_x(self.x1),
            mapping_y(self.y1),
            mapping_x(self.x2),
            mapping_y(self.y2)
        )]

    def setAllByCenterRadius(self, params, options):
        """ Expects: params to be a tuple: (center_x, center_y, radius); options to be a dict.
        Supports chaining after instantiation. """
        self.center_x = params[0]
        self.center_y = params[1]
        self.radius = params[2]
        # Convert to the bounding box representation
        self.x1 = self.center_x - self.radius
        self.y1 = self.center_y - self.radius
        self.x2 = self.center_x + self.radius
        self.y2 = self.center_y + self.radius
        self.options = options
        return self

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
