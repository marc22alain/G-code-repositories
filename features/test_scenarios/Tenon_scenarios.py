from option_queries import *

machine_config = {
    BitDiameterQuery: 6.35,
    SafeZQuery: 80,
    FeedRateQuery: 1000
}

work_piece_config = {
    StockLengthQuery: 100,
    StockWidthQuery: 50,
    StockHeightQuery: 15
}

tenon_scenarios = {
    'tenon_config_1': {
        'name': 'tenon_config_1',
        'machine_config': machine_config,
        'work_piece_config': work_piece_config,
        'config': {
            ReferenceXQuery: work_piece_config[StockLengthQuery] / 2,
            ReferenceYQuery: work_piece_config[StockWidthQuery] / 2,
            ShoulderOffsetQuery: 5,
            CornerRadiusQuery: machine_config[BitDiameterQuery] / 2,
            CutPerPassQuery: 2,
            CutDepthQuery: 1
        },
        'description': 'Makes a single pass'
    },

    'tenon_config_2': {
        'name': 'tenon_config_2',
        'machine_config': machine_config,
        'work_piece_config': work_piece_config,
        'config': {
            ReferenceXQuery: work_piece_config[StockLengthQuery] / 2,
            ReferenceYQuery: work_piece_config[StockWidthQuery] / 2,
            ShoulderOffsetQuery: 5,
            CornerRadiusQuery: machine_config[BitDiameterQuery] / 2,
            CutPerPassQuery: 2,
            CutDepthQuery: 3
        },
        'description': 'Makes two passes',
        'benchmark': {
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
    },

    'tenon_config_3': {
        'name': 'tenon_config_3',
        'machine_config': machine_config,
        'work_piece_config': work_piece_config,
        'config': {
            ReferenceXQuery: work_piece_config[StockLengthQuery] / 2,
            ReferenceYQuery: work_piece_config[StockWidthQuery] / 2,
            ShoulderOffsetQuery: 10,
            CornerRadiusQuery: machine_config[BitDiameterQuery] / 2,
            CutPerPassQuery: 2,
            CutDepthQuery: 5
        },
        'description': 'Makes three passes',
        'benchmark': {
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
