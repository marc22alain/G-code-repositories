
import abc

class DistributionFunction:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def generateCode(self):
        """ Generates the g-code to move the machine to the next position.
        Alternatively, only produces the new coordinates for the next position. """
        pass
