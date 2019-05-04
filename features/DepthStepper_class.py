from GeometricFeature_class import GeometricFeature
from option_queries import *
from utilities import Glib as G

class DepthStepper(GeometricFeature):
    '''
    Conceived as a class that will automatically wrap <any> user-specified
    feature. Does this break the pattern by presenting a different
    initialization interface ?
    Alternatively, could satisfy the requirement by adding an OptionQuery.
    ---
    Consider the challenge of using the DepthStepper to cause the child feature
    to make a tabbed cut.
    '''
    # Consider if this might get over-written by the child feature's name
    # name = 'Depth Stepper'
    user_selectable = False
    option_query_classes = [
        CutPerPassQuery,
        CutDepthQuery
    ]

    child_feature_classes = []

    def getGCode(self, instruction_callback, to_start_callback, return_callback):
        basic_params, cut_per_pass, cut_depth = self.getParams()
        stock_height = basic_params['stock_height']
        target_depth = stock_height - cut_depth
        multipass = cut_depth > cut_per_pass
        sequence = 'first'
        # pre-amble
        # Z-axis move to starting point from Z-safe
        file_text = G.set_ABS_mode()
        file_text += G.G0_Z(basic_params['safe_z'])
        file_text += to_start_callback()
        file_text += G.set_ABS_mode()
        file_text += G.G0_Z(basic_params['stock_height'])

        if multipass:
            while stock_height > target_depth:
                stock_height -= cut_per_pass
                if stock_height <= target_depth:
                    stock_height = target_depth
                    sequence = 'last'
                # Z-axis move
                file_text += G.set_ABS_mode()
                file_text += G.G1_Z(stock_height)
                file_text += ('# ' + sequence + '\n')
                file_text += instruction_callback(sequence)
                sequence = 'next'
        else:
            sequence = 'only'
            file_text += G.G1_Z(target_depth)
            file_text += instruction_callback(sequence)

        # post-amble
        file_text += G.set_ABS_mode()
        file_text += G.G0_Z(basic_params['safe_z'])
        file_text += return_callback()
        file_text += G.set_ABS_mode()

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

    def getInstructions(self):
        pass