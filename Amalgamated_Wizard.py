#!/usr/bin/env python

from Tkinter import *
import os
from Canvas_Geometry_classes import *


IN_AXIS = os.environ.has_key("AXIS_PROGRESS_BAR")


class AmalgamWizard(Frame):
    def __init__(self, master=None):
        self.canvasOptions = {"width":500, "height":500, "bg":"black"}
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.CanvasFrame = Frame(self,bd=5)
        self.CanvasFrame.grid(row=0, column=0)

        self.canvas = Canvas(self.CanvasFrame, self.canvasOptions)
        self.canvas.grid(row=0, column=0)
        # self.drawCanvasGrid()

        self.plotButton = Button(self, text='Plot all geometry', command=self.plotGeometry)
        self.plotButton.grid(row=1, column=0, sticky=S, pady=10)

    def plotGeometry(self):
        c = Circle(57, (250, 250), {"outline":"white"})
        c.draw(self.canvas)






app = AmalgamWizard()
app.master.title("Amalgamated Wizard 0.9")
app.mainloop()
