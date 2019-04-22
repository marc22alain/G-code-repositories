#!/usr/bin/env python

"""
How to add additional generator apps to the Mother Of All Apps:
- import the new generator's class name
- add the class name to self.apps
- done()
"""

from Tkinter import *

from Application_class import runApp
from RoundBottomedDado_class import RoundBottomedDado
from DoughnutCutter_class import DoughnutCutter
from RectangularPocket_class import RectangularPocket
from FrameMortiseAndTenon_class import FrameMortiseAndTenon
from FeatureCreature_class import FeatureCreature
from TkUiFactory_class import TkUIFactory

class AllApps(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.grid()
        self.ui_factory = TkUIFactory()
        self.apps = [RoundBottomedDado, DoughnutCutter, RectangularPocket, FrameMortiseAndTenon, FeatureCreature]
        self.addAppButtons()


    def addAppButtons(self):
        """
        Creates a button for every app; clicking on a button instantiates that app.
        """
        row_num = 0
        for app_class in self.apps:
            start_app = self.makeAppInit(app_class)
            appLink = Button(self,text=app_class.name,command=start_app, width=30)
            appLink.grid(row=row_num, column=0, pady=15)
            row_num += 1


    def makeAppInit(self, app_class):
        """
        Produces the closures that are triggered by clicking on an app button.
        """
        def startApp():
            app = self.ui_factory.makeMachinedGeometryEngine(app_class)
            runApp(Toplevel(self), app)
        return startApp


allApp = AllApps()
allApp.master.title("Run All the Apps")
allApp.mainloop()
