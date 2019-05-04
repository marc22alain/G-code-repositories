from EntryQuery_class import EntryQuery
from Tkinter import *

class StockLengthQuery(EntryQuery):
    name = 'StockLengthQuery'
    options = {
        'name': 'Stock length',
        'type': DoubleVar,
        'hint': 'How long is the stock'
    }

    def validate(self):
        return self.getValue() >= 0
