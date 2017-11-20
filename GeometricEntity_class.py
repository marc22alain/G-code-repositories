"""
GeometricEntity sets the pattern for wrapping TKinter canvas classes.
"""

import abc

class GeometricEntity:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def assertValid(self):
        """ Check data when setting the entity's parameters,
        or immediately in the call to draw(). """
        pass

    @abc.abstractmethod
    def setParams(self, *params):
        """ *params is simply a series of parameters as would be expected by the wrapped class. """
        pass

    @abc.abstractmethod
    def draw(self, canvas, mapping_x, mapping_y):
        pass

    def setOptions(self, options):
        """ options is an object. """
        self.options = options
        return self

    def applyOptions(self, canvas):
        """ Used as the last step in the draw() method.
        TODO: expand to cover all possible options. """
        keys = self.options.keys()
        if "fill" in keys:
            canvas.itemconfig(self.id, fill=self.options["fill"])
        if "outline" in keys:
            canvas.itemconfig(self.id, outline=self.options["outline"])
        if "tag" in keys:
            canvas.itemconfig(self.id, tag=self.options["tag"])
        if "arrow" in keys:
            canvas.itemconfig(self.id, arrow=self.options["arrow"])
        if "dash" in keys:
            canvas.itemconfig(self.id, dash=self.options["dash"])
        if "width" in keys:
            canvas.itemconfig(self.id, width=self.options["width"])
        # if "style" in keys:
        #     canvas.itemconfig(self.id, tag=self.options["style"])
        return self
