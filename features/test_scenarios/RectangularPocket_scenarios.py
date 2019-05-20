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
    }
}
