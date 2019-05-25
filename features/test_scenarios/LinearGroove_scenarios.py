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

lg_scenarios = {
    'lg_config_1': {
        'name': 'lg_config_1',
        'machine_config': machine_config,
        'work_piece_config': work_piece_config,
        'config': {
            DeltaXQuery: 13.75,
            DeltaYQuery: 0,
            ReferenceXQuery: 50,
            ReferenceYQuery: 45,
            CutPerPassQuery: 2,
            CutDepthQuery: 1
        },
        'description': 'Makes a single pass'
    },

    'lg_config_2': {
        'name': 'lg_config_2',
        'machine_config': machine_config,
        'work_piece_config': work_piece_config,
        'config': {
            DeltaXQuery: 3.75,
            DeltaYQuery: 2.1,
            ReferenceXQuery: 50,
            ReferenceYQuery: 45,
            CutPerPassQuery: 2,
            CutDepthQuery: 3
        },
        'description': 'Makes two passes'
    },

    'lg_config_3': {
        'name': 'lg_config_3',
        'machine_config': machine_config,
        'work_piece_config': work_piece_config,
        'config': {
            DeltaXQuery: 5.175,
            DeltaYQuery: -23.1,
            ReferenceXQuery: 50,
            ReferenceYQuery: 45,
            CutPerPassQuery: 2,
            CutDepthQuery: 6
        },
        'description': 'Makes three passes, with negative delta Y'
    }
}
