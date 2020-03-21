from EntryQuery_class import *

class StockLengthQuery(EntryQuery):
    """Stock length refers to the stock's X-length when it is placed on the
    spoil-board."""
    name = 'StockLengthQuery'
    options = {
        'name': 'Stock Length - X',
        'type': DoubleVar,
        'hint': 'How long is the stock'
    }

    def validate(self):
        return self.var.get() >= 0
