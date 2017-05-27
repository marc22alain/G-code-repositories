"""
View init options look something like this:
    view_init = { "view_plane": "YZ", \
                  "quadrant":1, \
                  "extents": {"width": 50, "height": 50, "center": (25, 25)} }
"""

from Tkinter import *


# self.canvas_options = {"width":500, "height":500, "bg":"black"}
# Note that scale is currently 1:1


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
        self._mapSystems()
        self.canvas = Canvas(self, self.canvas_options)
        self.canvas.grid(row=0, column=0)
        self.drawCanvasGrid()


    def drawCanvasGrid(self):
        # self.canvas.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
        margin = self.grid_options["margin"]
        width = self.grid_options["canW"]
        height = self.grid_options["canH"]
        grid_spacing = self.grid_options["grid_spacing"]
        for i in xrange(1, width / grid_spacing):
            self.canvas.create_line((i * grid_spacing) + margin, margin,  (i * grid_spacing) + margin, height + margin, fill="#333")
        for j in xrange(1, height / grid_spacing):
            self.canvas.create_line(margin, (j * grid_spacing) + margin, width + margin,  (j * grid_spacing) + margin, fill="#333")

        self.canvas.create_line(self.x_conv(- 25), self.y_conv(0), self.x_conv(425), self.y_conv(0), fill="green", arrow=LAST, dash=(16, 4, 4, 4))
        self.canvas.create_line(self.x_conv(0), self.y_conv(-25), self.x_conv(0), self.y_conv(425), fill="green", arrow=LAST, dash=(16, 4, 4, 4))
        # TODO: generalize the axis lines per quadrant.
        self.canvas.create_text(self.x_conv(440), self.y_conv(0), text="X", fill="green")
        self.canvas.create_text(self.x_conv(0), self.y_conv(435), text="Y", fill="green")


    def convertOptions(self, options):
        try:
            self.view_plane = options["view_plane"]
            # TODO: determine what happens when a view plane gets selected ...
            #   - show right letters for the plane
        except:
            pass
        try:
            # Defines the mapping between coordinate systems, if flipping is required
            # Also must relocate the axis lines
            self.view_quadrant = options["quadrant"]
        except:
            pass
        try:
            self.view_width = options["extents"]["width"]
            self.view_height = options["extents"]["height"]
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
        else:
            # no flipping required
            self.x_conv = lambda x: 50 + (x * self.view_scale)
            self.y_conv = lambda x: 50 - (x * self.view_scale)


    def drawGeometry(self, *geometries):
        for geometry in geometries:
            self.convertOptions(geometry)
        self.canvas.delete("geometry")
        for geometry in geometries:
            for arc in geometry["arc"]:
                self.canvas.create_arc(self.x_conv(arc[0]), self.y_conv(arc[1]), \
                    self.x_conv(arc[2]), self.y_conv(arc[3]), start=arc[4], \
                    extent=arc[5], outline=arc[6]["outline"], tag=arc[6]["tag"], fill=arc[6]["fill"])
            for arc in geometry["circle"]:
                self.canvas.create_oval(self.x_conv(arc[0]), self.y_conv(arc[1]), \
                    self.x_conv(arc[2]), self.y_conv(arc[3]), \
                    outline=arc[4]["outline"], tag=arc[4]["tag"], fill=arc[4]["fill"])
            for rect in geometry["rectangle"]:
                self.canvas.create_rectangle(self.x_conv(rect[0]), self.y_conv(rect[1]), \
                    self.x_conv(rect[2]), self.y_conv(rect[3]),\
                    outline=rect[4]["outline"], tag=rect[4]["tag"], fill=rect[4]["fill"])
