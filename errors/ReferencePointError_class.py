class ReferencePointError(TypeError):
    def __init__(self, drawing_entity, reference_point):
        TypeError.__init__(self, '%s does not implement %s' % (drawing_entity.__class__, reference_point))
