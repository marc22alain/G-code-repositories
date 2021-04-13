from GCodeParser_class import GCodeParser


class PostProcessor(object):
    def __init__(self):
        self.parser = GCodeParser()

    def setProgram(self, program):
        self.parser.resetProgram(program)

    def parseProgram(self):
        self.parser.parseProgram()

    def getProgramData(self):
        results = {}
        results.update(self.parser.getProgramData())
        return results

