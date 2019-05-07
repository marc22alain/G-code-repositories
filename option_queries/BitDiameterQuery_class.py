from SpinboxQuery_class import *
from utilities import MC

class BitDiameterQuery(SpinboxQuery):
    name = 'BitDiameterQuery'
    options = {
        'name': 'Bit diameter',
        'type': DoubleVar,
        'values': MC.bits,
        'hint': 'What diameter for bit',
        'default': 6.35
    }

    def insertQuery(self, master, row_num):
        stored = self.getValue()
        SpinboxQuery.insertQuery(self, master, row_num)
        self.setValue(stored)
