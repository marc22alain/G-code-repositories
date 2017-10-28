"""
Machine standard inputs:
    - standard Y dimension for central reference axis
    - standard X dimension for end of mortised pieces
    - standard X dimension for reference edge of tenoned pieces
    - width between clamped reference faces, a standard determined by the holding jigs

Interface must provide the following inputs:
    - mortise top face from table Z=0; from frame face width
    - mortise/tenon width, length, depth
    - mortise/tenon distance from reference face
    - mortise distance from stock end, which is same as tenon distance from outer edge
    - stock thickness for a reality check
    - stock bit diameters and lengths
    - feed speed
"""

from MachinedGeometry_class import MachinedGeometry
from default_query_sets import makeSetupQueries


class FrameMortiseAndTenon(MachinedGeometry):
    # class variables:
    name = "Frame by Mortise and Tenon"
    version = "0.1"
    implements_toolpass_view = False

    def __init__(self):
        pass

    def makeQueries(self, data_types, query_types):
        EntryQuery = query_types["entry"]
        double_type = data_types["double"]

        self.mortise_width_param = EntryQuery({"name":"Mortise Width", "type":double_type})
        self.mortise_length_param = EntryQuery({"name":"Mortise Length", "type":double_type})
        self.mortise_depth_param = EntryQuery({"name":"Mortise Depth", "type":double_type})

        self.mortise_offest_from_face_param = EntryQuery({"name":"Mortise Offset From Face", "type":double_type})
        self.mortise_offest_from_end_param = EntryQuery({"name":"Mortise Offset From End", "type":double_type})

        self.frame_face_width = EntryQuery({"name":"Frame Face Width", "type":double_type})
        self.frame_edge_width = EntryQuery({"name":"Frame Edge Width", "type":double_type})

        self.params = [self.mortise_width_param, self.mortise_length_param, \
                        self.mortise_depth_param, self.mortise_offest_from_face_param, self.mortise_offest_from_end_param, \
                        self.frame_face_width, self.frame_edge_width]

        self.machine_params = makeSetupQueries(data_types, query_types)
        self.entry_queries = self.machine_params.values() + self.params


    def getViewSpaceInit(self):
        """
        Thinking that the view should show the mortise and tenon and the stock outline.
        """
        view_init = { "view_plane": "XZ", \
                      "extents": {"width": 50, "height": 50, "center": (0, 0)} }
        return view_init


    def assertValid(self):
        pass

    def getDataQueries(self):
        """
        Returns a list of instantiated Query objects.
        These are part of the data model, even if they get passed back and
        forth with the controller.
        """
        return self.entry_queries

    def getToolPasses(self):
        """
        Since implements_toolpass_view = False.
        """
        pass

    def getGeometry(self, data):
        pass

    def generateGcode(self, data):
        pass
