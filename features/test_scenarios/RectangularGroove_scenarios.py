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

rect_scenarios = {
    'rect_config_1': {
        'name': 'rect_config_1',
        'machine_config': machine_config,
        'work_piece_config': work_piece_config,
        'config': {
            ReferenceXQuery: 50,
            ReferenceYQuery: 45,
            SideXQuery: 4.185,
            SideYQuery: 3.25,
            CutPerPassQuery: 2,
            CutDepthQuery: 1,
            PathReferenceQuery: 'center',
        },
        'description': 'Makes a single pass'
    },

    'rect_config_2': {
        'name': 'rect_config_2',
        'machine_config': machine_config,
        'work_piece_config': work_piece_config,
        'config': {
            ReferenceXQuery: 50,
            ReferenceYQuery: 45,
            SideXQuery: 4.185,
            SideYQuery: 3.25,
            CutPerPassQuery: 2,
            CutDepthQuery: 3,
            PathReferenceQuery: 'center',
        },
        'description': 'Makes two passes',
        'benchmark': {
            'num_drawn_entities': {
                'XY': {
                    'arc': 4,
                    'line': 4,
                    'rectangle': 2  # includes workpiece
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

    'rect_config_3': {
        'name': 'rect_config_3',
        'machine_config': machine_config,
        'work_piece_config': work_piece_config,
        'config': {
            ReferenceXQuery: 50,
            ReferenceYQuery: 45,
            SideXQuery: 7.185,
            SideYQuery: 9.25,
            CutPerPassQuery: 2,
            CutDepthQuery: 3,
            PathReferenceQuery: 'od',
        },
        'description': 'Makes two passes - with path reference `od`',
        'benchmark': {
            'program': 'F1000.0 \nG90 \nG0 Z80.0 \nG91 \nG0 X50.0 Y45.0 \nG0 X-0.4175 Y-1.45 \nG90 \nG0 Z15.0 \nG1 Z13.0 \nG4 P0.5 \n(# first)\nG91 \nG1 X0.0 Y2.9 \nG1 X0.835 Y0.0 \nG1 X0.0 Y-2.9 \nG1 X-0.835 Y0.0 \nG90 \nG1 Z12.0 \nG4 P0.5 \n(# last)\nG91 \nG1 X0.0 Y2.9 \nG1 X0.835 Y0.0 \nG1 X0.0 Y-2.9 \nG1 X-0.835 Y0.0 \nG90 \nG0 Z80.0 \nG91 \nG0 X0.4175 Y1.45 \nG0 X-50.0 Y-45.0 \nG90 \nM2 \n',
            'num_drawn_entities': {
                'XY': {
                    'arc': 4,
                    'line': 4,
                    'rectangle': 2  # includes workpiece
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
