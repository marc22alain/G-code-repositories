from EntryQuery_class import *

class TenonShoulderQuery(EntryQuery):
    name = 'TenonShoulderQuery'
    options = {
        'name': 'Tenon shoulder',
        'type': DoubleVar,
        'hint': 'What dimension for tenon shoulder'
    }

    def validate(self):
        return self.var.get() > 0
