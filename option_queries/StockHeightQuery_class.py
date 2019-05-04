from EntryQuery_class import EntryQuery
from Tkinter import *

class StockHeightQuery(EntryQuery):
    name = 'StockHeightQuery'
    options = {
        'name': 'Stock Height',
        'type': DoubleVar,
        'hint': 'How tall is the stock'
    }

    def validate(self):
        return self.getValue() > 0
