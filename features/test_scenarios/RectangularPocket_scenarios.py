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

rect_pocket_scenarios = {
    'rect_pocket_config_1': {
        'name': 'rect_pocket_config_1',
        'machine_config': machine_config,
        'work_piece_config': work_piece_config,
        'config': {
            ReferenceXQuery: 50,
            ReferenceYQuery: 45,
            SideXQuery: 14.185,
            SideYQuery: 33.25,
            CutPerPassQuery: 2,
            CutDepthQuery: 1
        },
        'description': 'Makes a single pass'
    },

    'rect_pocket_config_2': {
        'name': 'rect_pocket_config_2',
        'machine_config': machine_config,
        'work_piece_config': work_piece_config,
        'config': {
            ReferenceXQuery: 50,
            ReferenceYQuery: 45,
            SideXQuery: 14.185,
            SideYQuery: 33.25,
            CutPerPassQuery: 2,
            CutDepthQuery: 3
        },
        'description': 'Makes two passes',
        'benchmark': {
            'program': 'F1000.0 \nG90 \nG0 Z80.0 \nG91 \nG0 X50.0 Y45.0 \nG0 X-3.9175 Y-13.45 \nG90 \nG0 Z15.0 \nG1 Z13.0 \nG4 P0.5 \n(# first)\nG91 \nG1 X0.0 Y26.9 \nG1 X7.835 Y0.0 \nG1 X0.0 Y-26.9 \nG1 X-7.835 Y0.0 \nG1 X1.2425 Y5.85 \nG1 X0.0 Y15.2 \nG1 X5.35 Y0.0 \nG1 X0.0 Y-15.2 \nG1 X-5.35 Y0.0 \nG0 X2.675 Y7.6 \nG0 X-3.9175 Y-13.45 \nG90 \nG1 Z12.0 \nG4 P0.5 \n(# last)\nG91 \nG1 X0.0 Y26.9 \nG1 X7.835 Y0.0 \nG1 X0.0 Y-26.9 \nG1 X-7.835 Y0.0 \nG1 X1.2425 Y5.85 \nG1 X0.0 Y15.2 \nG1 X5.35 Y0.0 \nG1 X0.0 Y-15.2 \nG1 X-5.35 Y0.0 \nG90 \nG0 Z80.0 \nG91 \nG0 X2.675 Y7.6 \nG0 X-50.0 Y-45.0 \nG90 \nM2 \n',
            'num_drawn_entities': {
                'XY': {
                    'arc': 4,
                    'line': 4,
                    'rectangle': 1  # includes workpiece
                },
                'YZ': {
                    'arc': 0,
                    'rectangle': 2  # includes workpiece
                },
                'XZ': {
                    'arc': 0,
                    'rectangle': 2  # includes workpiece
                }
            }
        }
    }
}
