'''
 FeatureDistributor
 - takes a feature, a distribution function, and distributes the feature according to the function

 Need:
 - a visualizer
 - a function entry
 - a feature chooser
    . this seems to build on some of the previous simple generators, and perhaps more complex stuff too
    . this returns a function which will generate g-code with `yield` or similar

 In abstract, every generator could include the FeatureDistributor which produces an iteration of one.

 This could be considered an abstraction of the jig, or the jig is a special case, allowing mirroring.

 Q: what entity knows how many distributing steps to take ?
'''

class FeatureDistributor(object):
    def __init__(self, feature, distribution_function, num_steps):
        self.feature = feature      # an instance of Feature class
        self.distribution_function = distribution_function   # an instance of DistributionFunction class
        self.num_steps = num_steps

    def generateCode(self):
        g_code = ''
        for i in xrange(1, self.num_steps):
            g_code += self.feature.generateCode()
            g_code += self.distribution_function.generateCode()
        g_code += self.feature.generateCode()
        return g_code
