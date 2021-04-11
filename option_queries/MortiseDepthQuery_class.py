from EntryQuery_class import *

class MortiseDepthQuery(EntryQuery):
    name = 'MortiseDepthQuery'
    options = {
        'name': 'Mortise depth',
        'type': DoubleVar,
        'hint': 'What dimension for mortise depth'
    }

    def validate(self):
        return self.var.get() > 0
