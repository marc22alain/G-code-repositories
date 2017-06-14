"""
The default view of the Rectangular pocket is looking at the X-Y plane of machine coordinate system.
The default origin of the X-Y machine plane coincides with bottom left-hand corner of the pocket.

The default view puts the origin at the lower left hand corner of the window.
"""
from MachinedGeometry_class import MachinedGeometry
from Line_class import Line
from Arc_class import Arc
from Circle_class import Circle
from default_query_sets import makeSetupQueries, makeSquareStockQueries
import simple_generators as G
import math


class RectangularPocket(MachinedGeometry):
    # class variables:
    name = "Rectangular Pocket"
    version = "0.9"
    implements_toolpass_view = False

    def __init__(self):
        pass

    def makeQueries(self, data_types, query_types):
        EntryQuery = query_types["entry"]
        double_type = data_types["double"]
        self.pocket_length_param = EntryQuery({"name":"Pocket Length - X", "type":double_type})
        self.pocket_width_param = EntryQuery({"name":"Pocket Width - Y", "type":double_type})
        self.target_depth_param = EntryQuery({"name":"Target Depth - Z", "type":double_type})

        self.machine_params = makeSetupQueries(data_types, query_types)
        stock_params = makeSquareStockQueries(data_types, query_types)
        self.stock_height_param = stock_params["Stock Height - Z"]
        self.params = [self.stock_height_param, self.pocket_length_param, self.pocket_width_param, self.target_depth_param]
        self.entry_queries = self.machine_params.values() + self.params

    def getViewSpaceInit(self):
        # Quadrants:
        #   1 @ radians 0 -> pi/2
        #   2 @ radians pi/2 -> pi
        #   3 @ radians pi -> pi * 3/2
        #   4 @ radians pi * 3/2 -> pi * 2
        # Machine plane description:
        #   example: 'YZ' means Y is horizontal axis and Z is vertical axis
        # Note that the 'center' point of 'extents' also states the quadrant.
        view_init = { "view_plane": "XY", \
                      "extents": {"width": 50, "height": 50, "center": (25, 25)} }
        return view_init

    def getDataQueries(self):
        return self.entry_queries

    def getGeometry(self):
        self.assertValid()
        # Define a rectangle for the end of the stock (width and height).
        # Define an arc with center point at the midpoint of the top width line of the rectangle.
        pocket_w = self.pocket_width_param.getValue()
        pocket_l = self.pocket_length_param.getValue()
        bit_radius = self.machine_params["Cutter diameter"].getValue() / 2.0

        line_options = {"tag":"geometry","fill":"yellow"}
        arc_options = {"tag":"geometry","outline":"yellow"}

        entities = []
        entities.append(Line().setAll((0, bit_radius, 0, pocket_w - bit_radius), line_options))
        entities.append(Line().setAll((pocket_l, bit_radius, pocket_l, pocket_w - bit_radius), line_options))
        entities.append(Line().setAll((bit_radius, 0, pocket_l - bit_radius, 0), line_options))
        entities.append(Line().setAll((bit_radius, pocket_w, pocket_l - bit_radius, pocket_w), line_options))

        entities.append(Arc().setAllByCenterRadius((bit_radius, bit_radius, bit_radius, 180, 90), arc_options))
        entities.append(Arc().setAllByCenterRadius((bit_radius, pocket_w - bit_radius, bit_radius, 90, 90), arc_options))
        entities.append(Arc().setAllByCenterRadius((pocket_l - bit_radius, bit_radius, bit_radius, 270, 90), arc_options))
        entities.append(Arc().setAllByCenterRadius((pocket_l - bit_radius, pocket_w - bit_radius, bit_radius, 0, 90), arc_options))

        # showing the bit in place
        entities.append(Circle().setAllByCenterRadius((bit_radius, bit_radius, bit_radius), {"tag":"geometry","outline":"red","fill":"red"}))


        options = {"tag":"geometry","outline":"yellow","fill":None}
        return {"entities":entities,
                "extents": {"width": pocket_l, "height": pocket_w, "center": (pocket_l / 2.0, pocket_w / 2.0)}}

    def getToolPasses(self):
        pass

    def assertValid(self):
        if self.machine_params["Maximum cut per pass"].getValue() <= 0:
            raise ValueError("Cut per pass must be greater than zero!")

    def generateGcode(self):
        self.assertValid()
        feed_rate = self.machine_params["Feed rate"].getValue()
        safe_Z = self.machine_params["Safe Z travel height"].getValue()
        max_cut_per_pass = self.machine_params["Maximum cut per pass"].getValue()
        bit_diameter = self.machine_params["Cutter diameter"].getValue()
        stock_thickness = self.stock_height_param.getValue()
        pocket_w = self.pocket_width_param.getValue()
        pocket_l = self.pocket_length_param.getValue()
        target_d = self.target_depth_param.getValue()
        bit_radius = bit_diameter / 2.0

        # STOCK POSITIONING ASSUMPTIONS:
        #   - bit is at the lower-left hand corner of pocket
        #   - no assumptions made about the actual machine position
        self.g_code = G.startProgram(feed_rate)
        self.g_code += G.rectangularPocket((pocket_l, pocket_w), target_d, stock_thickness, safe_Z, max_cut_per_pass, bit_diameter, True)
        self.g_code += G.endProgram()
        return self.g_code
