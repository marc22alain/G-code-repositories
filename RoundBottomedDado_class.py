"""
The default view of the Round Bottomed Dado is looking at the Y-Z plane of machine coordinate system.
The default origin of the Y-Z machine plane coincides with bottom left-hand corner of the stock.

The default view puts the origin at the lower left hand corner of the window.
"""
from MachinedGeometry_class import MachinedGeometry
from Tkinter import *
from SpinboxQuery_class import SpinboxQuery
from EntryQuery_class import EntryQuery
from Rectangle_class import Rectangle
from Circle_class import Circle
from Arc_class import Arc
from default_query_sets import machine_params
import simple_generators as G
import math



class RoundBottomedDado(MachinedGeometry):
    # class variables:
    name = "Round Bottomed Dado"
    version = "0.9"
    implements_toolpass_view = True

    def __init__(self):
        self.stock_length_param = EntryQuery({"name":"Stock Length - X", "type":DoubleVar})
        self.stock_width_param = EntryQuery({"name":"Stock Width - Y", "type":DoubleVar})
        self.stock_height_param = EntryQuery({"name":"Stock Height - Z", "type":DoubleVar})
        self.bottom_radius_param = EntryQuery({"name":"Bottom Radius", "type":DoubleVar})
        self.params = [self.stock_length_param, self.stock_width_param, self.stock_height_param, self.bottom_radius_param]
        self.machine_params = machine_params
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
        view_init = { "view_plane": "YZ", \
                      "quadrant":1, \
                      "extents": {"width": 50, "height": 50, "center": (25, 25)} }
        return view_init

    def getDataQueries(self):
        return self.entry_queries

    def getGeometry(self):
        self.assertValid()
        # Define a rectangle for the end of the stock (width and height).
        # Define an arc with center point at the midpoint of the top width line of the rectangle.
        stock_w = self.stock_width_param.getValue()
        stock_h = self.stock_height_param.getValue()
        radius = self.bottom_radius_param.getValue()
        mid_stock_w = stock_w / 2.0
        mid_stock_h = stock_h / 2.0

        options = {"tag":"geometry","outline":"yellow","fill":None}
        return {"entities":[Rectangle().setAll((0,0,stock_w,stock_h), options),
                            Arc().setAllByCenterRadius((mid_stock_w, stock_h, radius, 180, 180), options)],
                "extents": {"width": stock_w, "height": stock_h, "center": (mid_stock_w, mid_stock_h)}}

    def getToolPasses(self):
        self.assertValid()
        tool_passes = {"entities":[]}

        stock_w = self.stock_width_param.getValue()
        stock_h = self.stock_height_param.getValue()
        radius = self.bottom_radius_param.getValue()
        mid_stock_w = stock_w / 2.0
        rad_center = { "x": mid_stock_w, "y": stock_h }
        max_cut_per_pass = self.machine_params["Maximum cut per pass"].getValue()
        bit_radius = self.machine_params["Cutter diameter"].getValue() / 2.0
        bit_center_Y = stock_h - max_cut_per_pass + bit_radius

        while (bit_center_Y > rad_center["y"] - radius + bit_radius):
            if bit_center_Y > rad_center["y"]:
                bit_center_from_middle = radius - bit_radius
            else:
                bit_center_from_middle = math.sqrt( ((radius - bit_radius)**2) - ((rad_center["y"] - bit_center_Y)**2) )
                options = {"tag":"geometry","outline":"white","fill":"white"}

                tool_passes["entities"].append(Circle().setAllByCenterRadius((mid_stock_w - bit_center_from_middle, bit_center_Y, bit_radius), options))
                tool_passes["entities"].append(Circle().setAllByCenterRadius((mid_stock_w + bit_center_from_middle, bit_center_Y, bit_radius), options))
            bit_center_Y -= max_cut_per_pass

        return tool_passes

    def assertValid(self):
        # TODO: consider progressive checking as impacts can arise.
        # Ensure that the program terminates, during G-code generation.
        # Only critical during G-code generation.
        if self.machine_params["Maximum cut per pass"].getValue() <= 0:
            raise ValueError("Cut per pass must be greater than zero!")
        # Prevent the tool from crashing into the spoil board.
        # Only critical during G-code generation.
        if self.bottom_radius_param.getValue() >= self.stock_height_param.getValue():
            raise ValueError("Radius is too large for stock height!")
        # Prevent the tool from crashing into the stock during G0 moves.
        # Only critical during G-code generation.
        if self.stock_height_param.getValue() >= self.machine_params["Safe Z travel height"].getValue():
            raise ValueError("Stock height is above Safe Z!")
        # Is it NOT OK if the bottom diameter exceeds the stock width ?

    def generateGcode(self):
        self.assertValid()
        feed_rate = self.machine_params["Feed rate"].getValue()
        safe_Z = self.machine_params["Safe Z travel height"].getValue()
        max_cut_per_pass = self.machine_params["Maximum cut per pass"].getValue()
        bit_diameter = self.machine_params["Cutter diameter"].getValue()
        stock_length = self.stock_length_param.getValue()
        stock_width = self.stock_width_param.getValue()
        stock_thickness = self.stock_height_param.getValue()
        bottom_radius = self.bottom_radius_param.getValue()

        bit_radius = bit_diameter / 2.0
        mid_stock_w = stock_width / 2.0
        rad_center = { "x": mid_stock_w, "y": stock_thickness }

        self.g_code = G.startProgram(feed_rate)

        # POSITIONING ASSUMPTIONS:
        #   - y-coord location of bit is at centerline of the dado
        #   - x-coord location of bit is adjacent to the stock
        #   - z-coord location is at or around Z-safe
        self.g_code += G.G.G0_Z(stock_thickness)

        # Putting the tip of the bit on the top surface of the stock.
        bit_center_Y = stock_thickness + bit_radius
        length = stock_length + (2 * bit_diameter)
        # The guard will always leave the center cut left to make.
        while (bit_center_Y - bit_radius - max_cut_per_pass > stock_thickness - bottom_radius ):
            bit_center_Y -= max_cut_per_pass
            if bit_center_Y > stock_thickness:
                bit_center_from_middle = bottom_radius - bit_radius
            else:
                # Applying Pythagoras:
                #    - (bottom_radius - bit_radius) is the hypotenuse
                #    - (stock_thickness - bit_center_Y) is the
                bit_center_from_middle = math.sqrt( ((bottom_radius - bit_radius)**2) - ((stock_thickness - bit_center_Y)**2) )
            # Move the bit to start of x-coord, then z-coord
            self.g_code += G.G.set_INCR_mode()
            self.g_code += G.G.G0_Y(- bit_center_from_middle)
            self.g_code += G.G.G1_Z(- max_cut_per_pass)
            self.g_code += G.G.set_ABS_mode()

            width = (bit_center_from_middle * 2) + bit_diameter
            self.g_code += G.rectArea((length, width), bit_diameter)

            # Wastes time, but moves the bit back to dado centerline.
            self.g_code += G.G.set_INCR_mode()
            self.g_code += G.G.G0_Y(bit_center_from_middle)
            self.g_code += G.G.set_ABS_mode()

        self.g_code += G.G.G1_Z(stock_thickness - bottom_radius)
        self.g_code += G.G.set_INCR_mode()
        self.g_code += G.G.G1_X(length)
        self.g_code += G.G.set_ABS_mode()

        self.g_code += G.G.G0_Z(safe_Z)
        self.g_code += G.endProgram()
        return self.g_code
