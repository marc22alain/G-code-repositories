#!/usr/bin/env python
from Tkinter import *
from OptionQueryDialog_class import OptionQueryDialog
from utilities import log

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

        # coloring of buttons not working :(
        self.edit_button = Button(self, text='Edit', command=self.openEditDialog, width=5, bg="#009", foreground="#333")
        self.edit_button.grid(row=row_num, column=1)
        self.edit_button.configure(bg="Red")

        if hasattr(self.item, 'delete'):
            self.delete_button = Button(self, text='Delete', command=self.deleteItem, width=5, bg="#900")
            self.delete_button.grid(row=row_num, column=2)

        if hasattr(self.item, 'is_composed'):
            for child in self.item.getChildren():
                row_num += 1
                self.sub_item = ListItem(self, child)
                self.sub_item.grid(row=row_num, column=0, columnspan=2)
                # self.sub_item['row_num'] = row_num

    def openEditDialog(self):
        if hasattr(self.item, 'getOptionQueriesForEdit'):
            OptionQueryDialog(self, self.item.getOptionQueriesForEdit(), self.item.name, self.okFunction)
        else:
            OptionQueryDialog(self, self.item.getOptionQueries(), self.item.name, self.okFunction)

    def okFunction(self):
        queries = self.item.getOptionQueries()
        log('confirming new value')
        for q in queries:
            log(q.var.get())
        if hasattr(self.item, 'is_composed'):
            log('ListItem row_num')
            # log(self.sub_item['row_num'])
            self.item.addChildByClass()
        self.item.didUpdateQueries()

    def deleteItem(self):
        self.item.delete()


