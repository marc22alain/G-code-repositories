from EntryQuery_class import *

class CutPerPassQuery(EntryQuery):
    name = 'CutPerPassQuery'
    options = {
        'name': 'Cut per pass',
        'type': DoubleVar,
        'hint': 'What depth to cut per pass'
    }

    def validate(self):
        return self.var.get() > 0
