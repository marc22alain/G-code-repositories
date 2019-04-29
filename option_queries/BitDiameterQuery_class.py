from SpinboxQuery_class import SpinboxQuery
from Tkinter import *
from utilities import MC

class BitDiameterQuery(SpinboxQuery):
    name = 'BitDiameterQuery'
    options = {
        'name': 'Bit diameter',
        'type': DoubleVar,
        'values': MC.bits,
        'hint': 'What diameter for bit'
    }
