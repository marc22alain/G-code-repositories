from EntryQuery_class import *

class StockHeightQuery(EntryQuery):
    """Stock height refers to the stock's Z-height when it is placed on the
    spoil-board."""
    name = 'StockHeightQuery'
    options = {
        'name': 'Stock Height - Z',
        'type': DoubleVar,
        'hint': 'How tall is the stock'
    }

    def validate(self):
        return self.var.get() > 0
