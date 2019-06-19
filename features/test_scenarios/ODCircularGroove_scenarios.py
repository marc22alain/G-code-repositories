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

odcg_scenarios = {
    'odcg_config_1': {
        'name': 'odcg_config_1',
        'machine_config': machine_config,
        'work_piece_config': work_piece_config,
        'config': {
            PathDiameterQuery: 6.175,
            ReferenceXQuery: -50,
            ReferenceYQuery: 45,
            CutPerPassQuery: 2,
            CutDepthQuery: 1
        },
        'description': 'Makes a single pass'
    },

    'odcg_config_2': {
        'name': 'odcg_config_2',
        'machine_config': machine_config,
        'work_piece_config': work_piece_config,
        'config': {
            PathDiameterQuery: 13.75,
            ReferenceXQuery: 50,
            ReferenceYQuery: 45,
            CutPerPassQuery: 2,
            CutDepthQuery: 3
        },
        'description': 'Makes two passes',
        'benchmark': {
            'program': 'F1000.0 \nG90 \nG0 Z80.0 \nG91 \nG0 X50.0 Y45.0 \nG0 X-3.7 Y0.0 \nG90 \nG0 Z15.0 \nG1 Z13.0 \nG4 P0.5 \n(# first)\nG91 \nG17 G2 X0.0 Y0.0 I3.7 J0.0 P1 \nG90 \nG1 Z12.0 \nG4 P0.5 \n(# last)\nG91 \nG17 G2 X0.0 Y0.0 I3.7 J0.0 P1 \nG90 \nG0 Z80.0 \nG91 \nG0 X3.7 Y0.0 \nG0 X-50.0 Y-45.0 \nG90 \nM2 \n'
        }
    }
}
