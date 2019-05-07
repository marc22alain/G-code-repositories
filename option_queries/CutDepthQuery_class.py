from EntryQuery_class import *

class CutDepthQuery(EntryQuery):
    name = 'CutDepthQuery'
    options = {
        'name': 'Cut depth',
        'type': DoubleVar,
        'hint': 'What depth to cut'
    }

    def validate(self):
        return self.getValue() > 0
