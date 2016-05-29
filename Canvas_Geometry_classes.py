#!/usr/bin/env python

from Tkinter import *




class CanvasGeometry(object):
    def __init__(self):
        self.name = joe


class Circle(object):
    def __init__(self, radius, center, line_type):
        self.radius = radius		# is a float
        self.center = center		# is a two-member tuple of floats
        self.line_type = line_type	# is a dict of options to pass in to the canvas

    def draw(self, canvas):
        x = self.center[0]
        y = self.center[1]
        r = self.radius
        canvas.create_oval(x - r, y - r, x + r, y + r, self.line_type)