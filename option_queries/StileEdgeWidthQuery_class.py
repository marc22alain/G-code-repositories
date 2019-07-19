from EntryQuery_class import *

class StileEdgeWidthQuery(EntryQuery):
    name = 'StileEdgeWidthQuery'
    options = {
        'name': 'Stile Edge width',
        'type': DoubleVar,
        'hint': 'What dimension for stile edge width'
    }

    def validate(self):
        return self.var.get() > 0
