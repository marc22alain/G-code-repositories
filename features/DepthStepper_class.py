import inspect
from geometric_feature_class import GeometricFeature
from option_queries import CutPerPassQuery, CutDepthQuery
from utilities import addDebugFrame, Glib as G

class DepthStepper(GeometricFeature):
    """For composition with features that are required to make repetitive machining
    operations to achieve the required depth of cut.
    ---
    TODO: consider the challenge of using the DepthStepper to cause the child feature
    to make a tabbed cut."""
    user_selectable = False
    option_query_classes = [
        CutPerPassQuery,
        CutDepthQuery
    ]

    child_feature_classes = []

    def getGCode(self, instruction_callback, to_start_callback, return_callback):
        file_text = addDebugFrame(inspect.currentframe())
        basic_params, cut_per_pass, cut_depth = self.getParams()
        stock_height = basic_params['stock_height']
        target_depth = stock_height - cut_depth
        multipass = cut_depth > cut_per_pass
        sequence = 'first'
        # pre-amble
        # Z-axis move to starting point from Z-safe
        file_text += self.machine.setMode('ABS')
        file_text += G.G0_Z(basic_params['safe_z'])
        file_text += to_start_callback()
        file_text += addDebugFrame(inspect.currentframe())
        file_text += self.machine.setMode('ABS')
        file_text += G.G0_Z(stock_height)

        if multipass:
            while stock_height > target_depth:
                stock_height -= cut_per_pass
                if stock_height <= target_depth:
                    stock_height = target_depth
                    sequence = 'last'
                # Z-axis move
                file_text += self.machine.setMode('ABS')
                file_text += G.G1_Z(stock_height)
                file_text += G.set_dwell(0.5)
                file_text += G.comment('# ' + sequence)
                file_text += instruction_callback(sequence)
                file_text += addDebugFrame(inspect.currentframe())
                sequence = 'next'
        else:
            sequence = 'only'
            file_text += G.G1_Z(target_depth)
            file_text += G.set_dwell(0.5)
            file_text += instruction_callback(sequence)
            file_text += addDebugFrame(inspect.currentframe())

        # post-amble
        file_text += self.machine.setMode('ABS')
        file_text += G.G0_Z(basic_params['safe_z'])
        file_text += return_callback()
        file_text += addDebugFrame(inspect.currentframe())
        file_text += self.machine.setMode('ABS')

        return file_text

    def getParams(self):
        basic_params = self.getBasicParams()
        cut_per_pass = self.option_queries[CutPerPassQuery].getValue()
        cut_depth = self.option_queries[CutDepthQuery].getValue()
        return (basic_params, cut_per_pass, cut_depth)

    def moveToStart(self):
        pass

    def returnToHome(self):
        pass

    def _makeDrawingClass(self):
        pass
