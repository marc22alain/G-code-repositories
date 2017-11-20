from MC_defaults import mortisingJig, machineLocations
from simple_generators import mortise, tenon

class MortisingJig(object):
    """
    This class relates to a particular jig for the CNC router.
    Diagrams would be ideal to explain the location of reference points and
    orientation of features.
    Constructor takes feature functions relevant to the work to be
    performed in the specified jig locations.
    If the desired work does not occupy both positions, pass in False for the
    unused position.

    Assumed: the first argument to the feature functions is the boolean: isMirrored
    """

    def __init__(self, machineMountLocation, mortiseLocationFeature=mortise, tenonLocationFeature=tenon):
        self.machineMountLocation = machineLocations[machineMountLocation]      # is a tuple (x,y)
        self.mortiseLocationFeature = mortiseLocationFeature                    # is a feature function
        self.tenonLocationFeature = tenonLocationFeature                        # is a feature function
        # Order of offsets is [mortise:False, mortise:True, tenon:False, tenon:True]
        self.offsets = self.makeOffsets()

    def getFeaturesOffsets(self):
        closures = []
        if self.mortiseLocationFeature:
            def mortise(*args):
                return self.mortiseLocationFeature(False, *args)
            def mortiseMirror(*args):
                return self.mortiseLocationFeature(True, *args)
            closures.append((self.offsets[0],mortise))
            closures.append((self.offsets[1], mortiseMirror))
        if self.tenonLocationFeature:
            def tenon(*args):
                return self.tenonLocationFeature(False, *args)
            def tenonMirror(*args):
                return self.tenonLocationFeature(True, *args)
            closures.append((self.offsets[2],tenon))
            closures.append((self.offsets[3], tenonMirror))
        for i in xrange(len(closures)):
            yield closures[i]

    def makeOffsets(self):
        return [1, 2, 3, 4]
