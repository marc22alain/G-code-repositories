from Tkinter import *
from GeometricEntity_class import GeometricEntity


class RoundedRectangle(GeometricEntity):
    """Draws rectangles with radii in the Tkinter canvas."""
    def __init__(self, view_space):
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        self.radius = None
        GeometricEntity.__init__(self, view_space)

    def assertValid(self):
        pass

    def _setParams(self, params):
        if len(params) != 5:
            raise ValueError("Incorrect number of params submitted!")
        self.x1 = params[0]
        self.y1 = params[1]
        self.x2 = params[2]
        self.y2 = params[3]
        self.radius = params[4]


    def setAll(self, params, options):
        """ Expects params to be a tuple and options to be a dict.
        Supports chaining after instantiation. """
        if len(params) != 5:
            raise ValueError("Incorrect number of params submitted!")
        self.x1 = params[0]
        self.y1 = params[1]
        self.x2 = params[2]
        self.y2 = params[3]
        self.radius = params[4]
        self.options = options
        self.options["style"] = ARC
        # To allow chaining of operations
        return self


    def _draw(self):
        canvas = self.view_space.canvas
        mapping_x = self.view_space.x_conv
        mapping_y = self.view_space.y_conv
        ids = []
        diameter = 2 * self.radius
        # left side line
        ids.append(canvas.create_line(
            mapping_x(self.x1),
            mapping_y(self.y1 + self.radius),
            mapping_x(self.x1),
            mapping_y(self.y2 - self.radius)
        ))
        # right side line
        ids.append(canvas.create_line(
            mapping_x(self.x2),
            mapping_y(self.y1 + self.radius),
            mapping_x(self.x2),
            mapping_y(self.y2 - self.radius)
        ))
        # bottom side line
        ids.append(canvas.create_line(
            mapping_x(self.x1 + self.radius),
            mapping_y(self.y1),
            mapping_x(self.x2 - self.radius),
            mapping_y(self.y1)
        ))
        # top side line
        ids.append(canvas.create_line(
            mapping_x(self.x1 + self.radius),
            mapping_y(self.y2),
            mapping_x(self.x2 - self.radius),
            mapping_y(self.y2)
        ))
        # lower left corner
        ids.append(canvas.create_arc(
            mapping_x(self.x1),
            mapping_y(self.y1),
            mapping_x(self.x1 + diameter),
            mapping_y(self.y1 + diameter),
            start=180,
            extent=90
        ))
        # lower right corner
        ids.append(canvas.create_arc(
            mapping_x(self.x2),
            mapping_y(self.y1),
            mapping_x(self.x2 - diameter),
            mapping_y(self.y1 + diameter),
            start=270,
            extent=90
        ))
        # upper left corner
        ids.append(canvas.create_arc(
            mapping_x(self.x1),
            mapping_y(self.y2),
            mapping_x(self.x1 + diameter),
            mapping_y(self.y2 - diameter),
            start=90,
            extent=90
        ))
        # upper right corner
        ids.append(canvas.create_arc(
            mapping_x(self.x2),
            mapping_y(self.y2),
            mapping_x(self.x2 - diameter),
            mapping_y(self.y2 - diameter),
            start=0,
            extent=90
        ))
        return ids

    def _update(self):
        canvas = self.view_space.canvas
        mapping_x = self.view_space.x_conv
        mapping_y = self.view_space.y_conv
        diameter = 2 * self.radius
        canvas.coords(
            self.ids[0],
            mapping_x(self.x1),
            mapping_y(self.y1 + self.radius),
            mapping_x(self.x1),
            mapping_y(self.y2 - self.radius)
        )
        canvas.coords(
            self.ids[1],
            mapping_x(self.x2),
            mapping_y(self.y1 + self.radius),
            mapping_x(self.x2),
            mapping_y(self.y2 - self.radius)
        )
        canvas.coords(
            self.ids[2],
            mapping_x(self.x1 + self.radius),
            mapping_y(self.y1),
            mapping_x(self.x2 - self.radius),
            mapping_y(self.y1)
        )
        canvas.coords(
            self.ids[3],
            mapping_x(self.x1 + self.radius),
            mapping_y(self.y2),
            mapping_x(self.x2 - self.radius),
            mapping_y(self.y2)
        )
        # arcs
        canvas.coords(
            self.ids[4],
            mapping_x(self.x1),
            mapping_y(self.y1),
            mapping_x(self.x1 + diameter),
            mapping_y(self.y1 + diameter)
        )
        canvas.coords(
            self.ids[5],
            mapping_x(self.x2),
            mapping_y(self.y1),
            mapping_x(self.x2 - diameter),
            mapping_y(self.y1 + diameter)
        )
        canvas.coords(
            self.ids[6],
            mapping_x(self.x1),
            mapping_y(self.y2),
            mapping_x(self.x1 + diameter),
            mapping_y(self.y2 - diameter)
        )
        canvas.coords(
            self.ids[7],
            mapping_x(self.x2),
            mapping_y(self.y2),
            mapping_x(self.x2 - diameter),
            mapping_y(self.y2 - diameter)
        )

    def getParams(self):
        return (
            [
                self.x1,
                self.y1,
                self.x2,
                self.y2,
                self.radius
            ],
            self.options
        )
