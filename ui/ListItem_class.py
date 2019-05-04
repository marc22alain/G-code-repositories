#!/usr/bin/env python
from Tkinter import *
from OptionQueryDialog_class import OptionQueryDialog

class ListItem(Frame):
    def __init__(self, master, item):
        Frame.__init__(self, master)
        self.grid()
        self.item = item
        self.createEntry()

    def createEntry(self):
        row_num = 1
        self.label = Label(self, text=self.item.name)
        self.label.grid(row=row_num, column=0)

        self.edit_button = Button(self, text='Edit', command=self.openEditDialog, width=10)
        self.edit_button.grid(row=row_num, column=1)

    def openEditDialog(self):
        OptionQueryDialog(self, self.item.getOptionQueries(), self.item.name, self.okFunction)

    def okFunction(self):
        queries = self.item.getOptionQueries().values()
        print 'confirming new value'
        for q in queries:
            print q.getValue()