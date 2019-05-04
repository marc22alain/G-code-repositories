#!/usr/bin/env python
from Tkinter import *
from ListItem_class import ListItem

class FeatureList(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.featureItems = []

    def insertFeature(self, feature):
        item = ListItem(self, feature)
        self.featureItems.append(item)
        item.grid(row=len(self.featureItems), column=0, columnspan=2, pady=5)
