from EntryQuery_class import *

class PathDiameterQuery(EntryQuery):
    name = 'PathDiameterQuery'
    options = {
        'name': 'Circle diameter',
        'type': DoubleVar,
        'hint': 'What diameter for path'
    }

    def validate(self):
        # TODO: consider whether == 0 is acceptable, for Peck ?
        return self.var.get() > 0
