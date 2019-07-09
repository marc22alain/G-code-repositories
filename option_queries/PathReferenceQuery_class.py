from SpinboxQuery_class import *
from utilities import MC

class PathReferenceQuery(SpinboxQuery):
    name = 'PathReferenceQuery'
    options = {
        'name': 'Path reference',
        'type': StringVar,
        'values': (
            'center',
            'od',
            'id',
        ),
        'hint': 'What point or edge to relate the groove ',
        'default': 'center'
    }
