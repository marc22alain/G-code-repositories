#!/usr/bin/env python
from Tkinter import *

class FeatureListItem(Frame):
    def __init__(self, master, feature):
        Frame.__init__(self, master)
        self.grid()
        self.feature = feature
        self.createEntry()

    def createEntry(self):
        self.label = Label(self, text=self.feature.name)
        self.label.grid(row=1, column=0)
