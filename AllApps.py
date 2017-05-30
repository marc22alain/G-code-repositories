#!/usr/bin/env python

"""
How to add additional generator apps to the Mother Of All Apps:
- import the new generator
- write a new method to call Application(<new generator>)
- add a button that calls the new method
"""

from Tkinter import *

from Application_class import runApp
from RoundBottomedDado_class import RoundBottomedDado
from TkUiFactory_class import TkUIFactory

class AllApps(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.grid()
        # self.top=self.winfo_toplevel()
        self.createWidgets()
        self.ui_factory = TkUIFactory()

    def createWidgets(self):
        row_num = 0
        self.app1 = Button(self,text="Round Bottomed Dado",command=self.startRoundBottomedDado, width=30)
        self.app1.grid(row=row_num, column=0, pady=15)

        # row_num += 1
        # self.app2 = Button(self.entry_frame,text="Refresh_view",command=self.refreshView, width=30)
        # self.app2.grid(row=row_num, column=0, columnspan=2, pady=5)


    def startRoundBottomedDado(self):
        RBD = self.ui_factory.makeMachinedGeometryEngine(RoundBottomedDado)
        runApp(Toplevel(self), RBD)



allApp = AllApps()
allApp.master.title("Run All the Apps")
allApp.mainloop()
