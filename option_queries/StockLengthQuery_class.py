from EntryQuery_class import *

class StockLengthQuery(EntryQuery):
    name = 'StockLengthQuery'
    options = {
        'name': 'Stock Length - X',
        'type': DoubleVar,
        'hint': 'How long is the stock'
    }

    def validate(self):
        return self.getValue() >= 0
