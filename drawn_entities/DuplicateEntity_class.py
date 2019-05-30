from GeometricEntity_class import GeometricEntity
from Tkinter import *


class DuplicateEntity(GeometricEntity):

    def __init__(self, view_space, subject):
        self.subject = subject
        GeometricEntity.__init__(self, view_space)
        self.duplicate_entity = self.duplicate(subject)

    def assertValid(self):
        pass

    def _setParams(self, params):
        pass

    def _draw(self):
        self.duplicate_entity.draw()

    def _update():
        pass

    def move(self, delta_x, delta_y):
        self.duplicate_entity.move(delta_x, delta_y)
        return self

    def duplicate(self, subject):
        params, options = subject.getParams()
        return subject.__class__(self.view_space).setParams(params, options)

    def applyOptions(self):
        self.duplicate_entity.applyOptions()

    def remove(self):
        self.duplicate_entity.remove()
