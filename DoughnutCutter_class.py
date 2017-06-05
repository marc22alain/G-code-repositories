"""
The default view of the Doughnut Cutter is looking at the X-Y plane of machine coordinate system.
The default origin of the X-Y machine plane coincides with center of the stock.

The default view puts the origin at the center of the window.
"""
from MachinedGeometry_class import MachinedGeometry
from Rectangle_class import Rectangle
from Circle_class import Circle
from Arc_class import Arc
from default_query_sets import makeSetupQueries, makeSquareStockQueries
import simple_generators as G
import math

class DoughnutCutter(MachinedGeometry):
    # class variables:
    name = "Doughnut Cutter"
    version = "0.9"
    implements_toolpass_view = False

    def __init__(self):
        pass

    def makeQueries(self, data_types, query_types):
        EntryQuery = query_types["entry"]
        double_type = data_types["double"]

        self.tab_thickness_param = EntryQuery({"name":"Tab Thickness", "type":double_type})
        self.tab_width_param = EntryQuery({"name":"Tab Width", "type":double_type})
        self.doughnut_OD_param = EntryQuery({"name":"Doughnut OD", "type":double_type})
        self.doughnut_ID_param = EntryQuery({"name":"Doughnut ID", "type":double_type})

        self.machine_params = makeSetupQueries(data_types, query_types)
        stock_params = makeSquareStockQueries(data_types, query_types)
        # self.stock_length_param = stock_params["Stock Length - X"]
        # self.stock_width_param = stock_params["Stock Width - Y"]
        self.stock_height_param = stock_params["Stock Height - Z"]
        self.params = [self.stock_height_param, self.tab_thickness_param, \
                        self.tab_width_param, self.doughnut_OD_param, self.doughnut_ID_param]
        self.entry_queries = self.machine_params.values() + self.params

    def getDataQueries(self):
        return self.entry_queries

    def getViewSpaceInit(self):
        # TODO: use this to set the origin in the middle of the view.
        #       .must elaborate ViewSpace_class to handle moving the origin and the axis lines
        pass

    def getGeometry(self):
        self.assertValid()
        entities = []
        options = {"tag":"geometry","outline":"yellow","fill":None}
        # Define two circles each for doughnut_OD and doughnut_ID.
        doughnut_OD = self.doughnut_OD_param.getValue()
        doughnut_ID = self.doughnut_ID_param.getValue()
        bit_diameter = self.machine_params["Cutter diameter"].getValue()

        entities.append(Circle().setAllByCenterRadius((0,0, doughnut_OD / 2.0), options))
        entities.append(Circle().setAllByCenterRadius((0,0, (doughnut_OD / 2.0) + bit_diameter), options))
        entities.append(Circle().setAllByCenterRadius((0,0, doughnut_ID / 2.0), options))
        entities.append(Circle().setAllByCenterRadius((0,0, (doughnut_ID / 2.0) - bit_diameter), options))

        # Because implementations will change.
        entities += self._makeTabs(options)

        stock_est = doughnut_OD + (2 * bit_diameter)

        stock_h = self.stock_height_param.getValue()
        return {"entities":entities,
                "extents": {"width": stock_est, "height": stock_est, "center": (0, 0)}}


    def _makeTabs(self, options):
        # TODO: Define the tabs @180, 60, and -60 degrees
        # BUG ALERT: while this mimics bore_tabbed_ID(), the algorithms are not shared
        entities = []
        doughnut_OD = self.doughnut_OD_param.getValue()
        doughnut_ID = self.doughnut_ID_param.getValue()
        tab_width = self.tab_width_param.getValue()
        bit_diameter = self.machine_params["Cutter diameter"].getValue()
        off_set_OD = (doughnut_OD  + bit_diameter) / 2.0
        off_set_ID = (doughnut_ID  - bit_diameter) / 2.0
        gap_radians_OD = (bit_diameter + tab_width) / 2 / off_set_OD
        gap_radians_ID = (bit_diameter + tab_width) / 2 / off_set_ID

        # At pi radians
        entities += self._mirroredArcs(math.pi, gap_radians_OD, bit_diameter, off_set_OD, options)
        entities += self._mirroredArcs(math.pi, gap_radians_ID, bit_diameter, off_set_ID, options)

        # At 1/3 pi radians
        entities += self._mirroredArcs((math.pi / 3.0), gap_radians_OD, bit_diameter, off_set_OD, options)
        entities += self._mirroredArcs((math.pi / 3.0), gap_radians_ID, bit_diameter, off_set_ID, options)

        # At - 1/3 pi radians
        entities += self._mirroredArcs(- (math.pi / 3.0), gap_radians_OD, bit_diameter, off_set_OD, options)
        entities += self._mirroredArcs(- (math.pi / 3.0), gap_radians_ID, bit_diameter, off_set_ID, options)

        return entities

    def _mirroredArcs(self, arc_radians, gap_radians, bit_diameter, off_set, options):
        arcs = []
        bit_radius = bit_diameter / 2.0
        arcs.append(Arc().setAllByCenterRadius((\
            math.cos(arc_radians + gap_radians) * off_set, \
            math.sin(arc_radians + gap_radians) * off_set, \
            bit_radius, \
            math.degrees(arc_radians + gap_radians + math.pi), \
            180), options))
        arcs.append(Arc().setAllByCenterRadius((\
            math.cos(arc_radians - gap_radians) * off_set, \
            math.sin(arc_radians - gap_radians) * off_set, \
            bit_radius, \
            math.degrees(arc_radians - gap_radians), \
            180), options))

        return arcs

    def assertValid(self):
        pass

    def generateGcode(self):
        feed_rate = self.machine_params["Feed rate"].getValue()
        safe_Z = self.machine_params["Safe Z travel height"].getValue()
        max_cut_per_pass = self.machine_params["Maximum cut per pass"].getValue()
        bit_diameter = self.machine_params["Cutter diameter"].getValue()
        stock_thickness = self.stock_height_param.getValue()

        self.g_code = G.startProgram(feed_rate)
        self.g_code += G.bore_circle_ID(safe_Z,
                          stock_thickness,
                          max_cut_per_pass,
                          self.tab_thickness_param.getValue(),
                          bit_diameter,
                          self.doughnut_ID_param.getValue())
        self.g_code += G.bore_tabbed_ID(safe_Z,
                          stock_thickness,
                          max_cut_per_pass,
                          self.tab_thickness_param.getValue(),
                          bit_diameter,
                          self.doughnut_ID_param.getValue(),
                          # TODO: confirm whether float() is required
                          float(self.tab_width_param.getValue()))
        self.g_code += G.bore_circle_OD(safe_Z,
                          stock_thickness,
                          max_cut_per_pass,
                          self.tab_thickness_param.getValue(),
                          bit_diameter,
                          self.doughnut_OD_param.getValue())
        self.g_code += G.bore_tabbed_OD(safe_Z,
                          self.tab_thickness_param.getValue(),
                          max_cut_per_pass,
                          self.tab_thickness_param.getValue(),
                          bit_diameter,
                          self.doughnut_OD_param.getValue(),
                          # TODO: confirm whether float() is required
                          float(self.tab_width_param.getValue()))
        self.g_code += G.endProgram()

        return self.g_code

    def getToolPasses(self):
        pass
