from MC_defaults import mortisingJig, machineLocations
from simple_generators import mortise, tenon, translateXYabs

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


    Loose end: how the machine -> jig offset is performed.
    How about a third method that generates the start positioning in absolute (x,y) ?

    Mirroring of coordinate systems would be an ideal way to work with this jig,
    but it is not implemented in LinuxCNC (though it does exist in other programs).
    """

    jig_constants = mortisingJig

    def __init__(self, machineMountLocation, mortiseLocationFeature=mortise, tenonLocationFeature=tenon):
        """
        Parameters:
        - machineMountLocation: some Y coordinate that locates the jig in the machine
            ... assuming that moving in X-axis is not an option
        - mortiseLocationFeature: a feature method to later be called
        - tenonLocationFeature: a feature method to later be called
        """
        self.machineMountLocation = machineLocations[machineMountLocation]      # is a tuple (x,y)
        self.mortiseLocationFeature = mortiseLocationFeature                    # is a feature function
        self.tenonLocationFeature = tenonLocationFeature                        # is a feature function
        # Order of offsets is [mortise:False, mortise:True, tenon:False, tenon:True]
        self.offsets = self.makeOffsets()

    def getFeaturesOffsets(self):
        """
        Returns an iterator, that yields tuples of (offsets, closure).
        Each closure decribes the operations that are required for a feature in
        a specific jig location:
        - the offset to perform before initiating running of the feature,
           it is a closure requiring a single argument: safe_Z
        - the feature with all required argument pre-populated
        The closure is populated with the single argument:
        - isMirrored: Boolean
        All variables specific to cutting the feature are collected by the UI
        and added later in the code generation sequence.
        """
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
        """
        Returns an array of (x,y) vectors describing offsets, one for each
        feature location and in the following order:
        - mortise regular
        - mortise mirrored (reversed Y-axis)
        - tenon regular
        - tenon mirrored (reversed Y-axis)
        Offsets could be initially hard-coded (then why bother with a method?),
        but should be generalized as user-specified parameters.

        The result of applying an offset is that the machine is then placed with
        bit center at the intersection of the reference planes for that holding
        location, at the safe Z-height.
        """
        start_x, start_y = self._findStart()

        def makeMove(x, y):
            def move(safe_Z):
                if safe_Z >= self.jig_constants['minimumSafeZ']:
                    return translateXYabs(x, y, safe_Z)
                else:
                    raise ValueError('Safe Z too short for Mortising Jig')
            return move

        closures = []

        # mortise regular
        closures.append(makeMove(start_x, start_y + mortisingJig['stileFaceReference']))
        # mortise mirrored
        closures.append(makeMove(start_x, start_y - mortisingJig['stileFaceReference']))
        # tenon regular
        closures.append(makeMove(start_x + mortisingJig['railEndReference'], start_y + mortisingJig['railFaceReference']))
        # tenon mirrored
        closures.append(makeMove(start_x + mortisingJig['railEndReference'], start_y - mortisingJig['railFaceReference']))
        return closures

    def moveToStart(self):
        """
        Provides a method to get the machine to move to the jig's reference starting point.
        Returns:
        - a closure that takes a single parameter: safe_Z provided by the user
        """
        start_x, start_y = self._findStart()

        def move(safe_Z):
            if safe_Z >= self.jig_constants['minimumSafeZ']:
                return translateXYabs(start_x, start_y, safe_Z)
            else:
                raise ValueError('Safe Z too short for Mortising Jig')

        return move


    def moveAside(self):
        """
        Provides a method to get the machine to move aside, permitting changeover
        of stock in the holding locations.
        Returns:
        - a closure that takes a single parameter: safe_Z provided by the user
        """
        start_x, start_y = self._findStart()

        def move(safe_Z):
            if safe_Z >= self.jig_constants['minimumSafeZ']:
                return translateXYabs(start_x - 200, start_y + 200, safe_Z)
            else:
                raise ValueError('Safe Z too short for Mortising Jig')

        return move


    def _findStart(self):
        """
        Calculates the jig's start coordinates.
        Returns:
        - a tuple (x,y) of absolute coordinates
        """
        x = self.machineMountLocation[0] + mortisingJig['offsetXfromMachineLocation']
        y = self.machineMountLocation[1] + mortisingJig['jigCenterlineOffset']
        return (x, y)
