
import abc

class Feature:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def generateCode(self):
        """ Generates g-code to cut the feature,
        leaving the machine in a state to move to the next position. """
        pass
