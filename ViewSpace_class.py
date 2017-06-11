"""
View init options look something like this:
    view_init = { "view_plane": "YZ", \
                  "quadrant":1, \
                  "extents": {"width": 50, "height": 50, "center": (25, 25)} }
"""

from Tkinter import *
from Line_class import Line


class ViewSpace(Frame):
    """docstring for ViewSpace"""
    canvas_options = {"width":500, "height":500, "bg":"black"}
    grid_options = {"grid_spacing": 50, "canW": canvas_options["width"], "canH": canvas_options["height"], "margin": 0}

    def __init__(self, master, init_options):
        Frame.__init__(self, master, bd=0)
        self.grid()
        # default start-up options
        self.view_scale = 1
        self.view_quadrant = 1
        self.x_conv = lambda x: (x * self.view_scale) + 50
        self.y_conv = lambda x: 450 - (x * self.view_scale)
        self.convertOptions(init_options)
        self._mapSystems()
        self.canvas = Canvas(self, self.canvas_options)
        self.canvas.grid(row=0, column=0)
        self.drawCanvasGrid()


    def drawCanvasGrid(self):
        margin = self.grid_options["margin"]
        width = self.grid_options["canW"]
        height = self.grid_options["canH"]
        grid_spacing = self.grid_options["grid_spacing"]
        for i in xrange(1, width / grid_spacing):
            self.canvas.create_line((i * grid_spacing) + margin, margin,  (i * grid_spacing) + margin, height + margin, fill="#333")
        for j in xrange(1, height / grid_spacing):
            self.canvas.create_line(margin, (j * grid_spacing) + margin, width + margin,  (j * grid_spacing) + margin, fill="#333")

        options = {"fill":"green","arrow":LAST,"dash":(16, 4, 4, 4)}

        x1 = self.view_center[0] - (self.view_width / 2.0)
        Line().setParams((self.view_center[0] - (self.view_width / 2.0)) - (self.view_width / 16.0), \
                        0, \
                        (self.view_center[0] + (self.view_width / 2.0)) + (self.view_width / 16.0), \
                        0 \
                        ).setOptions(options).draw(self.canvas, self.x_conv, self.y_conv)
        Line().setParams(0, \
                        (self.view_center[1] - (self.view_height / 2.0)) - (self.view_height / 16.0), \
                        0, \
                        (self.view_center[0] + (self.view_height / 2.0)) + (self.view_height / 16.0), \
                        ).setOptions(options).draw(self.canvas, self.x_conv, self.y_conv)


        self.canvas.create_text(self.x_conv((self.view_center[0] + (self.view_width / 2.0)) + (self.view_width / 12.0)), self.y_conv(0), text=self.view_plane[0], fill="green")
        self.canvas.create_text(self.x_conv(0), self.y_conv((self.view_center[0] + (self.view_height / 2.0)) + (self.view_height / 12.0)), text=self.view_plane[1], fill="green")


    def convertOptions(self, options):
        try:
            self.view_plane = (options["view_plane"][0], options["view_plane"][1])
            # TODO: determine what happens when a view plane gets selected ...
            #   - show right letters for the plane
        except:
            self.view_plane = ("U","V")
        try:
            # Defines the mapping between coordinate systems, if flipping is required
            # Also must relocate the axis lines
            self.view_quadrant = options["quadrant"]
        except:
            self.view_quadrant = 0
        try:
            self.view_width = options["extents"]["width"]
            self.view_height = options["extents"]["height"]
            self.view_center = options["extents"]["center"]
            self.view_scale = min((self.canvas_options["width"] - 100) / self.view_width, (self.canvas_options["height"] - 100) / self.view_height)
        except:
            self.view_scale = 1
        self._mapSystems()


    def _mapSystems(self):
        if self.view_quadrant == 1:
            self.x_conv = lambda x: 50 + (x * self.view_scale)
            # flip the vertical axis
            self.y_conv = lambda x: 450 - (x * self.view_scale)
        elif self.view_quadrant == 2:
            # flip both axes, but x is negative
            self.x_conv = lambda x: 450 + (x * self.view_scale)
            self.y_conv = lambda x: 450 - (x * self.view_scale)
        elif self.view_quadrant == 3:
            # flip the horizontal axis
            self.x_conv = lambda x: 450 + (x * self.view_scale)
            self.y_conv = lambda x: 50 - (x * self.view_scale)
        elif self.view_quadrant == 4:
            # no flipping required
            self.x_conv = lambda x: 50 + (x * self.view_scale)
            self.y_conv = lambda x: 50 - (x * self.view_scale)
        else:
            # make lambdas with defined center point
            x_offset = self.view_center[0] - (self.view_width / 2.0)
            y_offset = self.view_center[1] - (self.view_height / 2.0)
            self.x_conv = lambda x: 50 + ((x - x_offset) * self.view_scale)
            self.y_conv = lambda y: 450 - ((y - y_offset) * self.view_scale)


    def drawGeometry(self, *geometries):
        """
        Generic function to draw any kind of geometry.
        """
        for geometry in geometries:
            self.convertOptions(geometry)
        self.canvas.delete("geometry")
        for geometry in geometries:
            for entity in geometry["entities"]:
                entity.draw(self.canvas, self.x_conv, self.y_conv)
