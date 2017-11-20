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
from Rectangle_class import Rectangle
from MC_defaults import mortisingBits, mortisingJig
import simple_generators as G


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

        self.stile_face_width_param = EntryQuery({"name":"Stile Face Width", "type":double_type})
        self.stile_edge_width_param = EntryQuery({"name":"Stile Edge Width", "type":double_type})
        # Input will not be required; the generator will use self.stile_face_width_param if self.rail_face_width_param is not defined.
        self.rail_face_width_param = EntryQuery({"name":"Rail Face Width", "type":double_type})

        self.params = [self.mortise_width_param, self.mortise_length_param, \
                        self.mortise_depth_param, self.mortise_offest_from_face_param, self.mortise_offest_from_end_param, \
                        self.stile_face_width_param, self.stile_edge_width_param, self.rail_face_width_param]

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
        # Check required params
        if self.machine_params["Maximum cut per pass"].getValue() <= 0:
            raise ValueError("Cut per pass must be greater than zero!")

        # Check that the mortising bit exists ?
        bit_diameter = self.machine_params["Cutter diameter"].getValue()
        try:
            bit_length = mortisingBits[str(bit_diameter)]['length']
        except Exception as e:
            raise ValueError("Mortising bit %d does not exist!" % bit_diameter)

        # Check that mortise can be cut with this bit
        mortise_d = self.mortise_depth_param.getValue()
        if bit_length < mortise_d:
            raise ValueError("Mortise depth %d is greater than bit length %d!" % (mortise_d, bit_length))

        # Check that mortise depth is within X=3 of stile face width
        stile_face_width = self.stile_face_width_param.getValue()
        if mortise_d + 3 > stile_face_width:
            raise ValueError("Mortise depth %d is too deep for stile face width %d!" % (mortise_d, stile_face_width))

        # Check that mortise width offset is within Y=1
        mortise_offest_from_face = self.mortise_offest_from_face_param.getValue()
        if mortise_offest_from_face < 1:
            raise ValueError("Mortise offset from face %d is too small!" % (mortise_offest_from_face))

        # Check that mortise width (with offset) is within Y=1 of stile edge width
        mortise_w = self.mortise_width_param.getValue()
        stile_edge_width = self.stile_edge_width_param.getValue()
        if mortise_w + mortise_offest_from_face + 1 > stile_edge_width:
            raise ValueError('Mortise width %d is too great!' % mortise_w)

        # Check that mortise length offset is within Z=1
        mortise_offest_from_end = self.mortise_offest_from_end_param.getValue()
        if mortise_offest_from_end < 1:
            raise ValueError("Mortise offset from end %d is too small!" % (mortise_offest_from_end))

        # Check that mortise length (with offset) is within Z=1 of rail face width
        mortise_l = self.mortise_length_param.getValue()
        rail_face_width = self.rail_face_width_param.getValue()
        if rail_face_width == 0:
            if mortise_l + mortise_offest_from_end + 1 > stile_face_width:
                raise ValueError("Mortise length %d is too long for stile face width %d!" % (mortise_l, stile_face_width))
        else:
            if mortise_l + mortise_offest_from_end + 1 > rail_face_width:
                raise ValueError("Mortise length %d is too long for rail face width %d!" % (mortise_l, rail_face_width))


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

    def getGeometry(self):
        return self._getFaceView()

    def generateGcode(self):
        """
        Four cutting operations to program:
        - 2 mortises (uses the rectangular pocket)
            . rectangularPocket(area, target_depth, stock_thickness, safe_Z, cut_per_pass, bit_diameter, debug=False)
        - 2 tenons   (requires new machining pattern)

        Variable reference points, hold in MC_defaults.py:
        - machine's Y-axis coordinate of centers of location holes
        - width of holding jig
        - offset of machine location holes (centers) and centerline of holding jig
        - offset from machine's X-axis reference point and mortise reference faces
        - offset from machine's X-axis reference point and tenon reference faces

        Expanded bit definitions:
        - depth of cut, use in assertValid()
        """
        self.assertValid()
        feed_rate = self.machine_params["Feed rate"].getValue()
        safe_Z = self.machine_params["Safe Z travel height"].getValue()
        max_cut_per_pass = self.machine_params["Maximum cut per pass"].getValue()
        bit_diameter = self.machine_params["Cutter diameter"].getValue()
        bit_radius = bit_diameter / 2.0

        mortise_w = self.mortise_width_param.getValue()
        mortise_l = self.mortise_length_param.getValue()
        mortise_d = self.mortise_depth_param.getValue()
        mortise_offest_from_face = self.mortise_offest_from_face_param.getValue()
        mortise_offest_from_end = self.mortise_offest_from_end_param.getValue()
        stile_face_width = self.stile_face_width_param.getValue()
        stile_edge_width = self.stile_edge_width_param.getValue()

        if self.rail_face_width_param != 0:
            rail_face_width = self.rail_face_width_param.getValue()
        else:
            rail_face_width = stile_face_width

        # BIT POSITIONING ASSUMPTIONS:
        #   - bit position is assumed to be calibrated to the machine's jig locating holes
        #   - no other assumptions required
        self.g_code = G.startProgram(feed_rate)
        # Find the first corner pocket
        originABX = mortisingJig['stileEndReference'] - mortise_offest_from_end - mortise_l + bit_radius

        stileReferenceFaceA = mortisingJig['locationHoleYcoord'] - (mortisingJig['jigWidth'] / 2.0) + mortisingJig['jigCenterlineOffset']
        stileReferenceFaceB = mortisingJig['locationHoleYcoord'] + (mortisingJig['jigWidth'] / 2.0) + mortisingJig['jigCenterlineOffset']
        originAY = stileReferenceFaceA - mortise_offest_from_face - mortise_w + bit_radius
        originBY = stileReferenceFaceB + mortise_offest_from_face + bit_radius

        self.g_code += G.G.set_ABS_mode()
        self.g_code += G.G.G0_Z(safe_Z)

        self.g_code += G.G.G0_XY((originABX, originAY))
        self.g_code += G.rectangularPocket((mortise_l, mortise_w), stile_face_width - mortise_d, stile_face_width, safe_Z, max_cut_per_pass, bit_diameter, True)

        self.g_code += G.G.G0_XY((originABX, originBY))
        self.g_code += G.rectangularPocket((mortise_l, mortise_w), stile_face_width - mortise_d, stile_face_width, safe_Z, max_cut_per_pass, bit_diameter, True)

        # Pause now to mount the rails in the holding jig for the first set of tenon cuts
        self.g_code += G.G.pause()

        originABX = mortisingJig['railEndReference'] + mortise_offest_from_end
        originAY = stileReferenceFaceA - mortisingJig['railFaceReferenceOffset'] - stile_edge_width
        originBY = stileReferenceFaceB + mortisingJig['railFaceReferenceOffset']

        self.g_code += G.G.G0_XY((originABX, originAY))
        self.g_code += G.tenon((rail_face_width, stile_edge_width), (stile_face_width, stile_edge_width), \
                                (mortise_offest_from_face, mortise_offest_from_end), (mortise_l, mortise_w, mortise_d), \
                                bit_diameter, bit_diameter, safe_Z, max_cut_per_pass)

        alt_face_offset = stile_edge_width - mortise_offest_from_face - mortise_w
        self.g_code += G.G.G0_XY((originABX, originBY))
        self.g_code += G.tenon((rail_face_width, stile_edge_width), (stile_face_width, stile_edge_width), \
                                (alt_face_offset, mortise_offest_from_end), (mortise_l, mortise_w, mortise_d), \
                                bit_diameter, bit_diameter, safe_Z, max_cut_per_pass)

        self.g_code += G.endProgram()
        return self.g_code


    def _getFaceView(self):
        # mortise_width = self.mortise_width_param.getValue()
        mortise_length = self.mortise_length_param.getValue()
        mortise_depth = self.mortise_depth_param.getValue()
        # mortise_offest_from_face = self.mortise_offest_from_face_param.getValue()
        mortise_offest_from_end = self.mortise_offest_from_end_param.getValue()
        stile_face_width = self.stile_face_width_param.getValue()
        # stile_edge_width = self.stile_edge_width_param.getValue()
        rail_face_width = self.rail_face_width_param.getValue()

        if rail_face_width == 0:
            rail_face_width = stile_face_width

        stile_options = {"tag":"geometry","outline":"yellow","fill":None}
        rail_options = {"tag":"geometry","outline":"orange","fill":None}
        mortise_options = {"tag":"geometry","outline":"magenta","fill":None, "dash":10, "width":2}

        entities = []
        entities.append(Rectangle().setAll(( - rail_face_width, stile_face_width, rail_face_width, 0), stile_options))
        entities.append(Rectangle().setAll(( - rail_face_width, 0, 0, - stile_face_width), rail_options))
        entities.append(Rectangle().setAll(( - rail_face_width + mortise_offest_from_end, \
                                            mortise_depth, \
                                            - rail_face_width + mortise_offest_from_end + mortise_length, \
                                            0), mortise_options))

        return { "entities": entities,
                "extents": {"width": 2 * rail_face_width, "height": 2 * stile_face_width, "center": (0, 0)}}
