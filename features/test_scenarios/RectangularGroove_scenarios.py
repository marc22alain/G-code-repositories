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
            CutDepthQuery: 1
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
            CutDepthQuery: 3
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
    }
}
