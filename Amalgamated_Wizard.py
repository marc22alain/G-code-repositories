#!/usr/bin/env python

from Tkinter import *
import os
from Canvas_Geometry_classes import *


IN_AXIS = os.environ.has_key("AXIS_PROGRESS_BAR")


class AmalgamWizard(Frame):
    def __init__(self, master=None):
        self.canvasOptions = {"width":500, "height":500, "bg":"black"}
        Frame.__init__(self, master)
        self.grid()		# TKinter call to arrange the elements
        self.createWidgets()
        self.wizards = []	# to hold wizards as the user selects them

    def createWidgets(self):
        self.CanvasFrame = Frame(self,bd=5)
        self.CanvasFrame.grid(row=0, column=0)

        self.canvas = Canvas(self.CanvasFrame, self.canvasOptions)
        self.canvas.grid(row=0, column=0)
        # self.drawCanvasGrid()

        self.plotButton = Button(self, text='Plot all geometry', command=self.plotGeometry)
        self.plotButton.grid(row=1, column=0, sticky=S, pady=10)

    def plotGeometry(self):
        c = Circle(57, (0, 0), {"outline":"white"})
        
        canvas_items = [c.draw(self.canvas)]
        for wiz in self.wizards:
        	geo_entities = wiz.makeGeometricEntities()
        	for element in geo_entities:
        		canvas_items.append(element.draw())
        print canvas_items
        print self.canvas.bbox(1)
        # self.canvas.yview_moveto(-250)
        # self.canvas.yview("moveto", 10000.5)
        self.canvas.move(1, 250, 250)






app = AmalgamWizard()
app.master.title("Amalgamated Wizard 0.9")
app.mainloop()
