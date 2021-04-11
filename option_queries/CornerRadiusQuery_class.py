from EntryQuery_class import *

class CornerRadiusQuery(EntryQuery):
    name = 'CornerRadiusQuery'
    options = {
        'name': 'Corner Radius',
        'type': DoubleVar,
        'hint': 'What radius for corners'
    }

    def validate(self):
        return self.var.get() > 0
