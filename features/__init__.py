from CircularGroove_class import CircularGroove
from ODCircularGroove_class import ODCircularGroove
from LinearDistribution_class import LinearDistribution
from Peck_class import Peck
from DepthStepper_class import DepthStepper

classes_dict = {
    'CircularGroove': CircularGroove,
    'ODCircularGroove': ODCircularGroove,
    'LinearDistribution': LinearDistribution,
    'DepthStepper': DepthStepper,
    # 'Peck': Peck,  ... doesn't conform to meta class
}
