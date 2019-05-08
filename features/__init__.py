from CircularGroove_class import CircularGroove
from ODCircularGroove_class import ODCircularGroove
from LinearDistribution_class import LinearDistribution
# from Peck_class import Peck
from DepthStepper_class import DepthStepper
from LinearGroove_class import LinearGroove

classes_dict = {
    'CircularGroove': CircularGroove,
    'ODCircularGroove': ODCircularGroove,
    'LinearDistribution': LinearDistribution,
    'DepthStepper': DepthStepper,
    'LinearGroove': LinearGroove,
    # 'Peck': Peck,  ... doesn't conform to meta class
}
