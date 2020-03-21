from EntryQuery_class import *

class StockWidthQuery(EntryQuery):
    """Stock width refers to the stock's Y-length when it is placed on the
    spoil-board."""
    name = 'StockWidthQuery'
    options = {
        'name': 'Stock Width - Y',
        'type': DoubleVar,
        'hint': 'How wide is the stock'
    }

    def validate(self):
        return self.var.get() >= 0
