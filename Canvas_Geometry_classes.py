#!/usr/bin/env python

from Tkinter import *



class GeometricEntity(object):
    """
    Super-class to underpin all geometric entities.
    """
    def __init__(self, line_type):
        self.line_type = line_type    # is a dict of options to pass in to the canvas

    def draw(self):
        """
        Use the standard TKinter Canvas methods.
        This method MUST return the item's unique ID.
        """
        pass


class Circle(GeometricEntity):
    def __init__(self, radius, center, line_type):
        GeometricEntity.__init__(self, line_type)
        self.radius = radius		# is a float
        self.center = center		# is a two-member tuple of floats

    def draw(self, canvas):
        x = self.center[0]
        y = self.center[1]
        r = self.radius
        return canvas.create_oval(x - r, y - r, x + r, y + r, self.line_type, tag="circle")