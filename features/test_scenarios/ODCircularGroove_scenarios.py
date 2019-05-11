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
        'description': 'Makes two passes'
    }
}
