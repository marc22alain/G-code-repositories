#!/usr/bin/env python
from Tkinter import *
from BasicDialog_class import BasicDialog
from utilities import log

class OptionQueryDialog(BasicDialog):
    def __init__(self, parent, option_queries, feature_name, ok_callback=None, cancel_callback=None):
        self.option_queries = option_queries
        self.feature_name = feature_name
        BasicDialog.__init__(self, parent, 'Choose feature settings', ok_callback, cancel_callback)

    def body(self, master):
        # step: iterate through queries to form the Label():Entry() pairs
        #       associating the actual variables with the OptionQuery
        #       ? what data structure supports this ?
        row_num = 1
        self.label = Label(master, text=self.feature_name)
        self.label.grid(row=row_num, column=0)
        for query in self.option_queries.values():
            row_num += 1
            query.insertQuery(master, row_num)
        # need to get a better grip on returning the proper entry field
        return master

    def validate(self):
        '''
        Need to validate that user's input can be converted to the required.
        variable type.
        ? Any other validation ?
        ? Features must perform their own validation too, can we do it here ?

        Alternatively, can get the queries to validate themselves.
        They hold sufficient context to do so.

        Note that this is a short-circuiting validation: returns False on first
        failure.
        '''
        for query in self.option_queries.values():
            try:
                query.getValue()
                if not query.validate():
                    log(query.name)
                    log('query FAILED validation')
                    return False
            # for instance attempting to convert 'bogus' to a numerical type
            except ValueError:
                return False
        return True

    def apply(self):
        '''
        Override to set the OptionQuery values
        '''
        # for query in self.option_queries.values():
        #     log(query.name)
        #     log(query.getValue())
