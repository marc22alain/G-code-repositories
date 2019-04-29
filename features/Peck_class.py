from GeometricFeature_class import GeometricFeature
from OptionQuery_class import OptionQuery

class Peck(GeometricFeature):
    name = 'Peck'
    user_selectable = True
    '''
    This does not require wrapping with DepthStepper.
    '''
    def __init__(self):
        pass

    def getGCode(self):
        return ''

    def getOptionQueries(self):
        return [OptionQuery(float, 'What depth of cut')]

# p = Peck()

# print p.getOptionQueries()[0].variable_type
