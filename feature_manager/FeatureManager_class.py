from AbstractFeatureManager_class import AbstractFeatureManager
from machines import SimpleMachine
from workpieces import SimpleWorkpiece
import json


class FeatureManager(AbstractFeatureManager):
    """Feature manager for the app."""
    def __init__(self, view_space=None):
        self.machine = SimpleMachine(self)
        self.work_piece = SimpleWorkpiece(self, view_space)
        self.view_space = view_space
        self.g_code = None
        AbstractFeatureManager.__init__(self)

    def deleteChild(self, feature):
        """Delete child from app's list and from own list."""
        self.features.remove(feature)

    def getGCode(self):
        """Get gcode from all app's features."""
        # wrapping the features' gcode:
        self.g_code = self.machine.setUpProgram()
        for feature in self.features:
            self.g_code += feature.getGCode()
        self.g_code += self.machine.endProgram()
        return self.g_code

    def changeViewPlane(self):
        """Change view plane in response to user's selection."""
        self.work_piece.drawGeometry()
        for feature in self.features:
            feature.changeViewPlane()

    def reDrawAll(self):
        """Generic trigger for redrawing all feature geometry."""
        for feature in self.features:
            feature.drawGeometry()

    def saveFeatureConfigs(self, file_name):
        """Saves the composition of the Feature Manager to disk.
        Current format is JSON."""
        collection = self.genFeatureCollection()
        file = open(file_name + '.json', 'w')
        json.dump(collection, file)

    def genFeatureCollection(self):
        """Creates a dict representation of the FeatureManager's composition."""
        collection = { 'machine': {}, 'work_piece': {}, 'features': [] }
        collection['machine'] = self.machine.getRepresentationForCollection()
        collection['work_piece'] = self.work_piece.getRepresentationForCollection()
        for feat in self.features:
            collection['features'].append(feat.getRepresentationForCollection())
        return collection
