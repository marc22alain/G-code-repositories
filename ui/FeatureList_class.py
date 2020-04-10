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

    def removeFeature(self, feature):
        for_removal = None
        for item in self.featureItems:
            if item.item == feature:
                for_removal = item
                break
        self.featureItems.remove(for_removal)
        for_removal.destroy()
