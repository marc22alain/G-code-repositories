from EntryQuery_class import EntryQuery
from Tkinter import *

class StockWidthQuery(EntryQuery):
    name = 'StockWidthQuery'
    options = {
        'name': 'Stock Width',
        'type': DoubleVar,
        'hint': 'How wide is the stock'
    }

    def validate(self):
        return self.getValue() >= 0
