#!/usr/bin/env python
from Tkinter import *

from Application_class import runApp
from RoundBottomedDado_class import RoundBottomedDado

class AllApps(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.grid()
        # self.top=self.winfo_toplevel()
        self.createWidgets()

    def createWidgets(self):
        row_num = 0
        self.app1 = Button(self,text="Round Bottomed Dado",command=self.startRoundBottomedDado, width=30)
        self.app1.grid(row=row_num, column=0, pady=15)

        # row_num += 1
        # self.app2 = Button(self.entry_frame,text="Refresh_view",command=self.refreshView, width=30)
        # self.app2.grid(row=row_num, column=0, columnspan=2, pady=5)


    def startRoundBottomedDado(self):
        runApp(Toplevel(self), RoundBottomedDado)

allApp = AllApps()
allApp.master.title("Run All the Apps")
allApp.mainloop()
