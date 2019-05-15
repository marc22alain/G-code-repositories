from option_queries import *

machine_config = {
    BitDiameterQuery: 5.0,
    SafeZQuery: 80,
    FeedRateQuery: 1000
}

work_piece_config = {
    StockLengthQuery: 100,
    StockWidthQuery: 100,
    StockHeightQuery: 15
}

circ_pock_scenarios = {
    'circ_pock_config_1': {
        'name': 'circ_pock_config_1',
        'machine_config': machine_config,
        'work_piece_config': work_piece_config,
        'config': {
            PathDiameterQuery: 26.175,
            ReferenceXQuery: -50,
            ReferenceYQuery: 45,
            CutPerPassQuery: 2,
            CutDepthQuery: 1
        },
        'description': 'Makes a single pass'
    },

    'circ_pock_config_2': {
        'name': 'circ_pock_config_2',
        'machine_config': machine_config,
        'work_piece_config': work_piece_config,
        'config': {
            PathDiameterQuery: 26.175,
            ReferenceXQuery: 10,
            ReferenceYQuery: 14.5,
            CutPerPassQuery: 2,
            CutDepthQuery: 3
        },
        'description': 'Makes two passes'
    },
}
