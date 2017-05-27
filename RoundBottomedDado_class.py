"""
The default view of the Round Bottomed Dado is looking at the Y-Z plane of machine coordinate system.
The default origin of the Y-Z machine plane coincides with bottom left-hand corner of the stock.

The default view puts the origin at the lower left hand corner of the window.
"""
from MachinedGeometry_class import MachinedGeometry
from Tkinter import *
from SpinboxQuery_class import SpinboxQuery
from EntryQuery_class import EntryQuery
from default_query_sets import setup_queries
import math



class RoundBottomedDado(MachinedGeometry):
    # static class variables:
    data_query_defs =  [{"name":"Stock Width - Y", "type":DoubleVar, "input_type": EntryQuery}, \
                        {"name":"Stock Height - Z", "type":DoubleVar, "input_type": EntryQuery}, \
                        {"name":"Stock Length - X", "type":DoubleVar, "input_type": EntryQuery}, \
                        {"name":"Bottom Radius", "type":DoubleVar, "input_type": EntryQuery}]

    name = "Round Bottomed Dado"
    version = "0.9"
    implements_toolpass_view = True

    def __init__(self):
        self.entry_queries = self._makeEntryQueries()

    def getViewSpaceInit(self):
        # Quadrants:
        #   1 @ radians 0 -> pi/2
        #   2 @ radians pi/2 -> pi
        #   3 @ radians pi -> pi * 3/2
        #   4 @ radians pi * 3/2 -> pi * 2
        # Machine plane description:
        #   example: 'YZ' means Y is horizontal axis and Z is vertical axis
        # Note that the 'center' point of 'extents' also states the quadrant.
        view_init = { "view_plane": "YZ", \
                      "quadrant":1, \
                      "extents": {"width": 50, "height": 50, "center": (25, 25)} }
        return view_init

    def getDataQueries(self):
        return self.entry_queries

    def getGeometry(self, data):
        self.assertValid(data)
        # Define a rectangle for the end of the stock (width and height).
        # Define an arc with center point at the midpoint of the top width line of the rectangle.
        stock_w = data["Stock Width - Y"]
        stock_h = data["Stock Height - Z"]
        radius = data["Bottom Radius"]
        mid_stock_w = stock_w / 2.0
        mid_stock_h = stock_h / 2.0
        return {"rectangle":[(0,0,stock_w,stock_h, {"tag":"geometry","outline":"yellow","fill":None})], \
                "arc":[(mid_stock_w - radius,stock_h - radius, mid_stock_w + radius, stock_h + radius, 180, 180, {"tag":"geometry","outline":"yellow","fill":None})],
                "circle":[], "extents": {"width": stock_w, "height": stock_h, "center": (mid_stock_w, mid_stock_h)}}

    def getToolPasses(self, data):
        tool_passes = {"rectangle":[], "arc":[], "circle":[]}
        """
        {'Bottom Radius': 35.0, 'Stock Width - Y': 100.0, 'Maximum cut per pass': 0.0,
        'Stock Height - Z': 50.0, 'Cutter diameter': 3.175, 'Stock Length - X': 1000.0,
        'Safe Z travel height': 100.0, 'Feed rate': 1000.0}
        """
        stock_w = data["Stock Width - Y"]
        stock_h = data["Stock Height - Z"]
        radius = data["Bottom Radius"]
        mid_stock_w = stock_w / 2.0
        mid_stock_h = stock_h / 2.0
        rad_center = { "x": mid_stock_w, "y": stock_h }
        max_cut_per_pass = data["Maximum cut per pass"]
        bit_radius = data["Cutter diameter"] / 2.0
        bit_center_Y = stock_h - max_cut_per_pass + bit_radius

        while (bit_center_Y > rad_center["y"] - radius + bit_radius):
            if bit_center_Y > rad_center["y"]:
                bit_center_from_middle = radius - bit_radius
            else:
                bit_center_from_middle = math.sqrt( ((radius - bit_radius)**2) - ((rad_center["y"] - bit_center_Y)**2) )
            tool_passes["circle"].append((mid_stock_w - bit_center_from_middle - bit_radius, bit_center_Y - bit_radius, mid_stock_w - bit_center_from_middle + bit_radius, bit_center_Y + bit_radius, {"tag":"geometry","outline":"white","fill":"white"}))
            tool_passes["circle"].append((mid_stock_w + bit_center_from_middle - bit_radius, bit_center_Y - bit_radius, mid_stock_w + bit_center_from_middle + bit_radius, bit_center_Y + bit_radius, {"tag":"geometry","outline":"white","fill":"white"}))
            bit_center_Y -= max_cut_per_pass

        return tool_passes

    def assertValid(self, data):
        pass

    def _makeEntryQueries(self):
        entry_queries = []

        for query in setup_queries:
            entry_queries.append(query["input_type"](query))

        for query in self.data_query_defs:
            entry_queries.append(query["input_type"](query))
        return entry_queries

    def mutateStaticClassVar(self):
        self.implements_toolpass_view = False
