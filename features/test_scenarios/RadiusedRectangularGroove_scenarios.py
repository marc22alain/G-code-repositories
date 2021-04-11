from option_queries import *

machine_config = {
    BitDiameterQuery: 6.35,
    SafeZQuery: 80,
    FeedRateQuery: 1000
}

work_piece_config = {
    StockLengthQuery: 100,
    StockWidthQuery: 100,
    StockHeightQuery: 15
}

rad_rect_scenarios = {
    'rad_rect_config_1': {
        'name': 'rad_rect_config_1',
        'machine_config': machine_config,
        'work_piece_config': work_piece_config,
        'config': {
            ReferenceXQuery: 50,
            ReferenceYQuery: 45,
            CutPerPassQuery: 2,
            CutDepthQuery: 1,
            PathReferenceQuery: 'center',
            SideXQuery: 20,
            SideYQuery: 30,
            CornerRadiusQuery: 7.35,
        },
        'description': 'Makes a single pass',
        'benchmark': {
            'program': 'F1000.0 \nG90 \nG0 Z80.0 \nG91 \nG0 X50.0 Y45.0 \nG0 X-10.0 Y-7.65 \nG90 \nG0 Z15.0 \nG1 Z14.0 \nG4 P0.5 \nG91 \nG1 X0.0 Y15.3 \nG17 G2 X7.35 Y7.35 I7.35 J0.0 P1 \nG1 X5.3 Y0.0 \nG17 G2 X7.35 Y-7.35 I0.0 J-7.35 P1 \nG1 X0.0 Y-15.3 \nG17 G2 X-7.35 Y-7.35 I-7.35 J0.0 P1 \nG1 X-5.3 Y0.0 \nG17 G2 X-7.35 Y7.35 I0.0 J7.35 P1 \nG90 \nG0 Z80.0 \nG91 \nG0 X10.0 Y7.65 \nG0 X-50.0 Y-45.0 \nG90 \nM2 \n',
            'num_drawn_entities': {
                'XY': {
                    'arc': 8,
                    'line': 8,
                    'rectangle': 1  # includes workpiece
                },
                'YZ': {
                    'oval': 0,
                    'rectangle': 3  # includes workpiece
                },
                'XZ': {
                    'oval': 0,
                    'rectangle': 3  # includes workpiece
                }
            }
        }
    },

    'rad_rect_config_2': {
        'name': 'rad_rect_config_2',
        'machine_config': machine_config,
        'work_piece_config': work_piece_config,
        'config': {
            ReferenceXQuery: 50,
            ReferenceYQuery: 45,
            CutPerPassQuery: 2,
            CutDepthQuery: 3,
            PathReferenceQuery: 'od',
            SideXQuery: 20,
            SideYQuery: 38,
            CornerRadiusQuery: 8,
        },
        'description': 'Makes two passes - with path ref `od`',
        'benchmark': {
            'program': 'F1000.0 \nG90 \nG0 Z80.0 \nG91 \nG0 X50.0 Y45.0 \nG0 X-6.825 Y-11.0 \nG90 \nG0 Z15.0 \nG1 Z13.0 \nG4 P0.5 \n(# first)\nG91 \nG1 X0.0 Y22.0 \nG17 G2 X4.825 Y4.825 I4.825 J0.0 P1 \nG1 X4.0 Y0.0 \nG17 G2 X4.825 Y-4.825 I0.0 J-4.825 P1 \nG1 X0.0 Y-22.0 \nG17 G2 X-4.825 Y-4.825 I-4.825 J0.0 P1 \nG1 X-4.0 Y0.0 \nG17 G2 X-4.825 Y4.825 I0.0 J4.825 P1 \nG90 \nG1 Z12.0 \nG4 P0.5 \n(# last)\nG91 \nG1 X0.0 Y22.0 \nG17 G2 X4.825 Y4.825 I4.825 J0.0 P1 \nG1 X4.0 Y0.0 \nG17 G2 X4.825 Y-4.825 I0.0 J-4.825 P1 \nG1 X0.0 Y-22.0 \nG17 G2 X-4.825 Y-4.825 I-4.825 J0.0 P1 \nG1 X-4.0 Y0.0 \nG17 G2 X-4.825 Y4.825 I0.0 J4.825 P1 \nG90 \nG0 Z80.0 \nG91 \nG0 X6.825 Y11.0 \nG0 X-50.0 Y-45.0 \nG90 \nM2 \n',
            'num_drawn_entities': {
                'XY': {
                    'arc': 8,
                    'line': 8,
                    'rectangle': 1  # includes workpiece
                },
                'YZ': {
                    'oval': 0,
                    'rectangle': 3  # includes workpiece
                },
                'XZ': {
                    'oval': 0,
                    'rectangle': 3  # includes workpiece
                }
            }
        }
    },

    'rad_rect_config_3': {
        'name': 'rad_rect_config_3',
        'machine_config': machine_config,
        'work_piece_config': work_piece_config,
        'config': {
            ReferenceXQuery: 50,
            ReferenceYQuery: 45,
            CutPerPassQuery: 2,
            CutDepthQuery: 3,
            PathReferenceQuery: 'id',
            SideXQuery: 20 - (2 * machine_config[BitDiameterQuery]),    #  7.3
            SideYQuery: 38 - (2 * machine_config[BitDiameterQuery]),    # 25.3
            CornerRadiusQuery: 8 - machine_config[BitDiameterQuery],    #  1.65
        },
        'description': 'Makes two passes - with path ref `id`',
        'benchmark': {
            'program': 'F1000.0 \nG90 \nG0 Z80.0 \nG91 \nG0 X50.0 Y45.0 \nG0 X-6.825 Y-11.0 \nG90 \nG0 Z15.0 \nG1 Z13.0 \nG4 P0.5 \n(# first)\nG91 \nG1 X0.0 Y22.0 \nG17 G2 X4.825 Y4.825 I4.825 J0.0 P1 \nG1 X4.0 Y0.0 \nG17 G2 X4.825 Y-4.825 I0.0 J-4.825 P1 \nG1 X0.0 Y-22.0 \nG17 G2 X-4.825 Y-4.825 I-4.825 J0.0 P1 \nG1 X-4.0 Y0.0 \nG17 G2 X-4.825 Y4.825 I0.0 J4.825 P1 \nG90 \nG1 Z12.0 \nG4 P0.5 \n(# last)\nG91 \nG1 X0.0 Y22.0 \nG17 G2 X4.825 Y4.825 I4.825 J0.0 P1 \nG1 X4.0 Y0.0 \nG17 G2 X4.825 Y-4.825 I0.0 J-4.825 P1 \nG1 X0.0 Y-22.0 \nG17 G2 X-4.825 Y-4.825 I-4.825 J0.0 P1 \nG1 X-4.0 Y0.0 \nG17 G2 X-4.825 Y4.825 I0.0 J4.825 P1 \nG90 \nG0 Z80.0 \nG91 \nG0 X6.825 Y11.0 \nG0 X-50.0 Y-45.0 \nG90 \nM2 \n',
            'num_drawn_entities': {
                'XY': {
                    'arc': 8,
                    'line': 8,
                    'rectangle': 1  # includes workpiece
                },
                'YZ': {
                    'oval': 0,
                    'rectangle': 3  # includes workpiece
                },
                'XZ': {
                    'oval': 0,
                    'rectangle': 3  # includes workpiece
                }
            }
        }
    }
}
