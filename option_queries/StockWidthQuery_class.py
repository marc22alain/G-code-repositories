from EntryQuery_class import *

class StockWidthQuery(EntryQuery):
    name = 'StockWidthQuery'
    options = {
        'name': 'Stock Width - Y',
        'type': DoubleVar,
        'hint': 'How wide is the stock'
    }

    def validate(self):
        return self.var.get() >= 0
